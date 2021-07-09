"""
snapshot connector file for aws type snapshot. When the 'type' is 'aws', the
resource objects have to be fetched from the AWS interface.
The connection could use python SDK libraries or https calls or other known methods
provided by the provider.
Here in case of AWS, have used boto python SDK released and maintained by AWS.
boto library provides different 'describe_' functions and using this functionality,
the snapshot mentions which describe function has to be called, so 'type' could
be 'security_groups' , 'instances', 'regions' and using python reflection capabilities
a callable from describe_security_groups gets callable for this function to return security groups.
The describe_ functions lots of methods to query AWS resources, since we know what resource we need
we always query by id, so AWS snapshots shall always have {"id": "123de23"} to uniquely
identify the resource object.
"""
import json
import hashlib
import re
import time
import copy
import pymongo
import os
from boto3 import client
from boto3 import Session
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import put_in_currentdata, get_dbtests, get_from_currentdata
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    collectiontypes, STRUCTURE, make_snapshots_dir, store_snapshot
from processor.connector.vault import get_vault_data
from processor.helper.config.config_utils import config_value, get_test_json_dir, CUSTOMER
from processor.database.database import insert_one_document, sort_field, get_documents,\
    COLLECTION, DATABASE, DBNAME, get_collection_size, create_indexes
from processor.helper.httpapi.restapi_azure import json_source
from processor.helper.httpapi.restapi_azure import get_client_secret
from processor.connector.snapshot_utils import validate_snapshot_nodes
from processor.connector.arn_parser import arnparse

logger = getlogger()
_valid_service_names = Session().get_available_services()


def _validate_client_name(client_name):
    """
    A private function to validate whether a given client provided
    in snapshot or aws connector is a valid service in Boto3
    """
    return client_name is not None and client_name.lower() in _valid_service_names


def get_aws_data(snapshot_source):
    """
    The AWS source object to be fetched from database or the filesystem
    The initial configuration for database is 'validator' and collection
    is 'structures', whereas for the filesystem the path to fetch the
    'structures' is  $SOLUTIONDIR/realm/<structure>.json
    """
    sub_data = {}
    if json_source():
        dbname = config_value(DATABASE, DBNAME)
        collection = config_value(DATABASE, collectiontypes[STRUCTURE])
        parts = snapshot_source.split('.')
        qry = {'name': parts[0]}
        sort = [sort_field('timestamp', False)]
        docs = get_documents(collection, dbname=dbname, sort=sort, query=qry, limit=1)
        logger.info('Number of AWS structure Documents: %d', len(docs))
        if docs and len(docs):
            sub_data = docs[0]['json']
    else:
        json_test_dir = get_test_json_dir()
        file_name = '%s.json' % snapshot_source if snapshot_source and not \
            snapshot_source.endswith('.json') else snapshot_source
        aws_source = '%s/../%s' % (json_test_dir, file_name)
        logger.info('AWS source: %s', aws_source)
        if exists_file(aws_source):
            sub_data = json_from_file(aws_source)
    return sub_data


def _get_aws_function(awsclient, node):
    """ 
    A private function to get the function which has to be called by the
    boto3 client object to get snapshot data.
    """
    describe_function_str = get_aws_describe_function(node)
    if describe_function_str:
        describe_function = getattr(awsclient, describe_function_str, None)
        if describe_function and callable(describe_function):
            return describe_function
    
    function_str = _get_callable_method_from_node(node)
    if function_str:
        callable_function = getattr(awsclient, function_str, None)
        if callable_function and callable(callable_function):
            return callable_function

    
def _get_callable_method_from_node(node):
    """Callable Method from node using python reflection mechanism"""
    _fn_str = None
    if node and 'type' in node and node['type']:
        _fn_str = node['type']
    return _fn_str
    

def get_aws_describe_function(node):
    """Describe function for the node using python reflection mechanism"""
    describe_fn_str = None
    if node and 'type' in node and node['type']:
        describe_fn_str = 'describe_%s' % node['type']
    return describe_fn_str


def get_node(awsclient, node, snapshot_source, snapshot):
    """
    Fetch node from aws using connection. In this case using boto API's
    describe functions.
    """

    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    function_to_call = None
    db_record = {
        "structure": "aws",
        "error": None,
        "reference": "",
        "source": parts[0],
        "path": '',
        "timestamp": int(time.time() * 1000),
        "queryuser": get_field_value(snapshot, 'testUser'),
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "region" : "",
        "snapshotId": node['snapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": {}  # Refactor when node is absent it should None, when empty object put it as {}
    }
    detail_methods = get_field_value(node, "detailMethods")
    if detail_methods is None:
        function_to_call = _get_aws_function(awsclient, node)
        if function_to_call and callable(function_to_call):
            queryval = get_field_value(node, 'id')
            try:
                data = function_to_call(**queryval)
                if data:
                    db_record['json'] = data
                    checksum = get_checksum(data)
                    if checksum:
                        db_record['checksum'] = checksum
                    else:
                        put_in_currentdata('errors', data)
                        logger.info("Describe function does not exist: %s", str(function_to_call))
                        db_record['error'] = "Describe function does not exist: %s" % str(function_to_call)
            except Exception as ex:
                logger.info('Describe function exception: %s', ex)
                db_record['error'] = 'Describe function exception: %s' % ex
        else:
            logger.info('Invalid function exception: %s', str(function_to_call))
            db_record['error'] = 'Invalid function exception: %s' % str(function_to_call)
    else:
        json_to_put = {}
        arn_str = get_field_value(node, "arn")
        db_record["path"] = arn_str if arn_str else ""

        if arn_str:
            zone = re.findall(r"arn:aws:[A-Za-z0-9\-]*:([a-zA-Z0-9\-]*):.*", arn_str)
            if zone:
                db_record["region"] = zone[0]
        
        arn_obj = arnparse(arn_str)
        client_str = arn_obj.service
        resourceid = arn_obj.resource
        for each_method_str in detail_methods:
            function_to_call = getattr(awsclient, each_method_str, None)
            if function_to_call and callable(function_to_call):
                params = _get_function_kwargs(arn_str, each_method_str, json_to_put)
                try:
                    data = function_to_call(**params)
                    if data:
                        json_to_put.update(data) 
                except Exception as ex:
                    logger.info('Describe function exception: %s', ex)
                    db_record['error'] = 'Describe function exception: %s' % ex
            else:
                logger.info('Invalid function exception: %s', str(function_to_call))
                db_record['error'] = 'Invalid function exception: %s' % str(function_to_call)
        db_record['json'] = json_to_put
    return db_record


def _get_resources_from_list_function(response, method):
    """
    Fetches the resources id from different responses
    and returns a list of responses.
    """
    if method == 'list_buckets':
        return [x['Name'] for x in response['Buckets']]
    elif method == 'describe_instances':
        final_list = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                final_list.append(instance['InstanceId'])
        return final_list
    elif method == 'describe_db_instances':
        return [x['DBInstanceIdentifier'] for x in response['DBInstances']]
    elif method == 'describe_load_balancers':
        return [x['LoadBalancerName'] for x in response['LoadBalancerDescriptions']]
    elif method == 'list_certificates':
        return [x['CertificateArn'] for x in response['CertificateSummaryList']]        
    elif method == 'list_stacks':
        return [x['StackName'] for x in response['StackSummaries']]        
    elif method == 'list_trails':
        return [x['Name'] for x in response['Trails']]        
    elif method in ['describe_stacks', 'list_trails']:
        return [x['StackName'] for x in response['Stacks']]        
    elif method == 'get_rest_apis':
        return [x['id'] for x in response['items']]   
    elif method == 'list_users':
        return [x['UserName'] for x in response['Users']]
    elif method == 'list_roles':
        return [x['RoleName'] for x in response['Roles']]     
    elif method == 'list_hosted_zones':
        return [x['Id'] for x in response['HostedZones']]
    elif method == 'list_keys':
        return [x.get('KeyId') for x in response['Keys']]
    elif method == 'list_tables':
        return response.get("TableNames")
    elif method == 'list_backups':
        return [x.get('BackupArn',"") for x in response['BackupSummaries']]
        return response.get("TableNames")
    elif method == 'list_task_definitions':
        return response.get('taskDefinitionArns')
    elif method == 'list_clusters':
        return response.get("clusters")
    elif method == 'describe_replication_groups':
        return [x.get('ReplicationGroupId') for x in response['ReplicationGroups']]
    elif method == 'list_streams':
        return response.get("StreamNames")
    elif method == 'list_functions':
        return [x.get('FunctionName',"") for x in response['Functions']]
    elif method == 'describe_clusters':
        return [x.get('ClusterIdentifier',"") for x in response['Clusters']]
    elif method == 'list_topics':
        return [x.get('TopicArn',"") for x in response['Topics']]
    elif method == 'list_queues':
        return response.get("QueueUrls")  
    elif method == 'list_domain_names':
        return [x.get('DomainName') for x in response['DomainNames']] 
    elif method == 'describe_configuration_recorders':
        return [x.get('name') for x in response['ConfigurationRecorders']] 
    elif method == 'list_distributions':
        return [x.get('Id') for x in response['DistributionList']['Items']]
    elif method == 'describe_vpn_gateways':
        return [x.get('VpnGatewayId') for x in response['VpnGateways']]
    elif method == 'describe_file_systems':
        return [x.get('FileSystemId') for x in response['FileSystems']]
    elif method == 'describe_parameters':
        return [x.get('Name') for x in response['Parameters']]
    elif method == 'describe_cache_subnet_groups':
        return [x.get('CacheSubnetGroupName') for x in response['CacheSubnetGroups']]
    elif method == 'describe_route_tables':
        return [x.get('RouteTableId') for x in response['RouteTables']]
    elif method == 'describe_network_acls':
        return [x.get('NetworkAclId') for x in response['NetworkAcls']]
    elif method == 'describe_event_subscriptions':
        return [x.get('EventSubscriptionArn').split(':')[-1] for x in response['EventSubscriptionsList']]
    elif method == 'describe_db_snapshots':
        return [x.get('DBSnapshotIdentifier') for x in response['DBSnapshots']]
    else:
        return []

def get_all_nodes(awsclient, node, snapshot, connector):
    """ Fetch all the nodes from the cloned git repository in the given path."""
    db_records = []
    arn_string = "arn:aws:%s:%s::%s"
    collection = node['collection'] if 'collection' in node else COLLECTION
    snapshot_source = get_field_value(snapshot, 'source')
    parts = snapshot_source.split('.')
    d_record = {
        "structure": "aws",
        "reference": "",
        "source": parts[0],
        "path": '',
        "timestamp": int(time.time() * 1000),
        "queryuser": get_field_value(snapshot, 'testUser'),
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": None,
        "masterSnapshotId": node['masterSnapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": {}
    }
    list_function_name = get_field_value(node, 'listMethod')
    if list_function_name:
        list_function = getattr(awsclient, list_function_name, None)
        if list_function and callable(list_function):
            try:
                list_kwargs = _get_list_function_kwargs(awsclient.meta._service_model.service_name, list_function_name)
                response = list_function(**list_kwargs)
                list_of_resources = _get_resources_from_list_function(response, list_function_name)
            except Exception as ex:
                list_of_resources = []
            detail_methods = get_field_value(node, 'detailMethods')
            for each_resource in list_of_resources:
                type_list = []
                if "arn:" in each_resource:
                    resource_arn = each_resource
                else:
                    resource_arn = arn_string %(awsclient.meta._service_model.service_name,
                        awsclient.meta.region_name, each_resource)
                for each_method_str in detail_methods:
                    each_method = getattr(awsclient, each_method_str, None)
                    if each_method and callable(each_method):
                        type_list.append(each_method_str)
                db_record = copy.deepcopy(d_record)
                db_record['detailMethods'] = type_list
                db_record['arn'] = resource_arn
                db_records.append(db_record)

    return db_records

def get_checksum(data):
    """ Get the checksum for the AWS data fetched."""
    checksum = None
    try:
        data_str = json.dumps(data, default=str)
        checksum = hashlib.md5(data_str.encode('utf-8')).hexdigest()
    except:
        pass
    return checksum

def _get_list_function_kwargs(service, function_name):
    if service == "cloudformation" and function_name == 'list_stacks':
        return {
            'StackStatusFilter' : ['CREATE_IN_PROGRESS', 'CREATE_COMPLETE', 'ROLLBACK_IN_PROGRESS',\
            'ROLLBACK_COMPLETE', 'UPDATE_IN_PROGRESS', 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS', \
            'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_IN_PROGRESS', 'UPDATE_ROLLBACK_FAILED', \
            'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS', 'UPDATE_ROLLBACK_COMPLETE', \
            'REVIEW_IN_PROGRESS', 'IMPORT_IN_PROGRESS', 'IMPORT_COMPLETE', 'IMPORT_ROLLBACK_IN_PROGRESS', \
            'IMPORT_ROLLBACK_FAILED', 'IMPORT_ROLLBACK_COMPLETE']
        }
    else:
        return {}

def _get_function_kwargs(arn_str, function_name, existing_json):
    """Fetches the correct keyword arguments for different detail functions"""
    arn = arnparse(arn_str)
    client_str = arn.service
    resource_id = arn.resource
    if client_str == "s3":
        return {'Bucket' : resource_id}
    elif client_str == "rds" and function_name in ["describe_db_instances",\
        "describe_db_snapshots"]:
        return {
            'DBInstanceIdentifier': resource_id
        }
    elif client_str == "ec2" and function_name == "describe_instance_attribute":
        return {
            'Attribute': 'instanceType',
            'InstanceId': resource_id
        }
    elif client_str == "ec2" and function_name in ["describe_instances", "monitor_instances"]:
        return {
            'InstanceIds': [resource_id]
        }
    elif client_str == "ec2" and function_name == "describe_images":
        try:
            imageid = existing_json['Reservations'][0]['Instances'][0]['ImageId']
        except:
            imageid = ""
        return {
            'ImageIds': [imageid]
        }
    elif client_str == "ec2" and function_name == "describe_volumes":
        try:
            volumeid = existing_json['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
        except:
            volumeid = ""
        return {
            'VolumeIds': [volumeid]
        }
    elif client_str == "ec2" and function_name == "describe_security_groups":
        try:
            groups = existing_json['Reservations'][0]['Instances'][0]['SecurityGroups']
            groupsidlist = [x['GroupId'] for x in groups]
        except:
            groupsidlist = []
        return {
            'GroupIds': groupsidlist
        }
    elif client_str == "ec2" and function_name == "describe_vpcs":
        try:
            vpicid = existing_json['Reservations'][0]['Instances'][0]['VpcId']
        except:
            vpicid = ""
        return {
            'VpcIds': [vpicid]
        }
    elif client_str == "ec2" and function_name == "describe_subnets":
        try:
            subnetid = existing_json['Reservations'][0]['Instances'][0]['SubnetId']
        except:
            subnetid = ""
        return {
            'SubnetIds': [subnetid]
        }
    elif client_str == "ec2" and function_name == "describe_snapshots":
        try:
            ownerid = existing_json['Reservations'][0]['OwnerId']
        except:
            ownerid = ""
        return {
            'OwnerIds': [ownerid]
        }
    elif client_str == "ec2" and function_name == "describe_snapshot_attribute":
        try:
            snapshot_id = existing_json['Snapshots'][0]['SnapshotId']
        except:
            snapshot_id = ""
        return {
            'SnapshotId': snapshot_id,
            'Attribute' : 'createVolumePermission'
        }
    elif client_str == "elb" and function_name == "describe_load_balancers":
        return {
            'LoadBalancerNames': [resource_id]
        }
    elif client_str == "elb" and function_name in ["describe_load_balancers", "describe_load_balancer_attributes",\
        "describe_load_balancer_policies"]:
        return {
            'LoadBalancerName': resource_id
        }
    elif client_str == "acm" and function_name == "describe_certificate":
        return {
            'CertificateArn': arn_str
        }
    elif client_str == "cloudformation" and function_name in ["describe_stack_resource",\
        "describe_stack_events", "describe_stacks", "describe_stack_resource_drifts", \
        "get_stack_policy"]:
        return {
            'StackName': resource_id
        }
    elif client_str == "cloudtrail" and function_name == "describe_trails":
        return {
            'trailNameList': [resource_id]
        }
    elif client_str == "cloudtrail" and function_name in ["get_event_selectors",\
        "get_insight_selectors"]:
        return {
            'TrailName': resource_id
        }
    elif client_str == "apigateway" and function_name in ["get_rest_api",\
        "get_documentation_parts", "get_documentation_versions",\
        "get_gateway_responses", "get_models", "get_request_validators",\
        "get_resources", "get_stages"]:
        return {
            'restApiId': resource_id
        }
    elif client_str == "route53" and function_name == "get_hosted_zone":
        return {
            'Id': resource_id
        }
    elif client_str == "route53" and function_name == "list_resource_record_sets":
        return {
            'HostedZoneId': resource_id
        }
    elif client_str == "iam" and function_name in ["get_user", "list_ssh_public_keys", \
        "get_account_summary", "get_account_password_policy", "list_attached_user_policies"]:
        return {
            'UserName': resource_id
        }
    elif client_str == "iam" and function_name == "get_role":
        return {
            'RoleName': resource_id
        }
    elif client_str == "kms" and function_name in ["get_key_rotation_status", "describe_key",]:
        return {
            'KeyId': resource_id
        }
    elif client_str == "dynamodb" and function_name == "describe_table":
        return {
            'TableName': resource_id
        }
    elif client_str == "dynamodb" and function_name == "describe_backup":
        return {
            'BackupArn': arn_str
        }
    elif client_str == "ecs" and function_name == "describe_task_definition":
        return {
            'taskDefinition': resource_id
        }
    elif client_str == "eks" and function_name == "describe_cluster":
        return {
            'name': resource_id
        }
    elif client_str == "elasticache" and function_name == "describe_replication_groups":
        return {
            'ReplicationGroupId': resource_id
        }
    elif client_str == "elasticache" and function_name == "describe_cache_subnet_groups":
        return {
            'CacheSubnetGroupName': resource_id
        }
    elif client_str == "kinesis" and function_name == "describe_stream":
        return {
            'StreamName': resource_id
        }
    elif client_str == "lambda" and function_name == "get_function":
        return {
            'FunctionName': resource_id
        }
    elif client_str == "redshift" and function_name == "describe_clusters":
        return {
            'ClusterIdentifier': resource_id
        }
    elif client_str == "sns" and function_name == "get_topic_attributes":
        return {
            'TopicArn': arn_str
        }
    elif client_str == "sqs" and function_name == "get_queue_attributes":
        return {
            'QueueUrl': 'https:{url}'.format(url=resource_id), 'AttributeNames': ['All']
        }
    elif client_str == "config" and function_name in ["describe_configuration_recorders", "describe_configuration_recorder_status"]:
        return {
            'ConfigurationRecorderNames': [resource_id]
        }
    elif client_str == "es" and function_name == "describe_elasticsearch_domain":
        return {
            'DomainName': resource_id
        }
    elif client_str == "cloudfront" and function_name == "get_distribution":
        return {
            'Id': resource_id
        }
    elif client_str == "ec2" and function_name == "describe_vpn_gateways":
        return {
            'VpnGatewayIds': [resource_id]
        }
    elif client_str == "efs" and function_name == "describe_file_systems":
        return {
            'FileSystemId': resource_id
        }
    elif client_str=='ec2'and function_name == 'describe_route_tables':
        return{
            'RouteTableIds': [resource_id]
        }
    elif client_str=='ec2'and function_name == 'describe_network_acls':
        return{
            'NetworkAclIds': [resource_id]
        }
    elif client_str=='rds'and function_name == 'describe_event_subscriptions':
        return{
            'SubscriptionName': resource_id
        }
    elif client_str=='rds'and function_name == 'describe_db_snapshot_attributes':
        return{
            'DBSnapshotIdentifier': resource_id
        }
    else:
        return {}

def _get_aws_client_data_from_node(node, default_client=None, default_region=None):
    """
    Fetches client name and region from ARN, then from the node, 
    then from the connector.
    """
    aws_region = client_str = None
    arn_str = get_field_value(node, 'arn')
    if arn_str:
        arn_obj = arnparse(arn_str)
        client_str = arn_obj.service
        aws_region = arn_obj.region
    if not client_str:
        client_str = get_field_value(node, 'client')
    if not client_str:
        logger.info("No client type provided in snapshot, using client type from connector")
        client_str = default_client
    if not aws_region: 
        aws_region = get_field_value(node, 'region')
    if not aws_region:
        logger.info("No region provided in snapshot, using region from connector")
        aws_region = default_region
    aws_region = aws_region or default_region
    client_str = client_str or default_client
    return client_str, aws_region


def populate_aws_snapshot(snapshot, container=None):
    """
    This is an entrypoint for populating a snapshot of type aws.
    All snapshot connectors should take snapshot object and based on
    'source' field create a method to connect to the service for the
    connector.
    The 'source' field could be used by more than one snapshot, so the
    'testuser' attribute should match to the user the 'source'
    """
    dbname = config_value('MONGODB', 'dbname')
    snapshot_source = get_field_value(snapshot, 'source')
    snapshot_user = get_field_value(snapshot, 'testUser')
    account_id = get_field_value(snapshot, 'accountId')
    sub_data = get_aws_data(snapshot_source)
    snapshot_nodes = get_field_value(snapshot, 'nodes')
    snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    # valid_snapshotids = True
    # if snapshot_nodes:
    #     for node in snapshot_nodes:
    #         snapshot_data[node['snapshotId']] = False
    #         if not isinstance(node['snapshotId'], str):
    #             valid_snapshotids = False
    # if not valid_snapshotids:
    #     logger.error('All snap')
    if valid_snapshotids and sub_data and snapshot_nodes:
        logger.debug(sub_data)
        access_key, secret_access, region, connector_client_str = \
            get_aws_client_data(sub_data, snapshot_user, account_id)
        if not access_key:
            logger.info("No access_key in the snapshot to access aws resource!...")
            raise Exception("No access_key in the snapshot to access aws resource!...")
            # return snapshot_data

        # Read the client secrets from envirnment variable
        if not secret_access:
            secret_access = os.getenv(snapshot_user, None)
            if secret_access:
                logger.info('Secret Access key from environment variable, Secret: %s', '*' * len(secret_access))
        
        # Read the client secrets from the vault
        if not secret_access:
            secret_access = get_vault_data(access_key)
            if secret_access:
                logger.info('Secret Access key from vault Secret: %s', '*' * len(secret_access))
            elif get_from_currentdata(CUSTOMER):
                logger.error("Secret Access key does not set in a vault")
                raise Exception("Secret Access key does not set in a vault")

        if not secret_access:
            raise Exception("No `secret-access` key in the connector file to access aws resource!...")

        if access_key and secret_access:
            # existing_aws_client = {}
            for node in snapshot['nodes']:
                validate = node['validate'] if 'validate' in node else True
                mastercode = False
                if 'snapshotId' in node and validate:
                    client_str, aws_region = _get_aws_client_data_from_node(node,
                        default_client=connector_client_str, default_region=region)
                    if not _validate_client_name(client_str):
                        logger.error("Invalid Client Name")
                        return snapshot_data
                    try:
                        awsclient = client(client_str.lower(), aws_access_key_id=access_key,
                                           aws_secret_access_key=secret_access, region_name=aws_region)
                    except Exception as ex:
                        logger.info('Unable to create AWS client: %s', ex)
                        awsclient = None
                    logger.info(awsclient)
                    if awsclient:
                        data = get_node(awsclient, node, snapshot_source, snapshot)
                        if data:
                            error_str = data.pop('error', None)
                            if get_dbtests():
                                if get_collection_size(data['collection']) == 0:
                                    #Creating indexes for collection
                                    create_indexes(data['collection'],
                                        config_value(DATABASE, DBNAME), 
                                        [('snapshotId', pymongo.ASCENDING),
                                        ('timestamp', pymongo.DESCENDING)])

                                    create_indexes(
                                        data['collection'],
                                        config_value(DATABASE, DBNAME), 
                                        [
                                            ('_id', pymongo.DESCENDING),
                                            ('timestamp', pymongo.DESCENDING),
                                            ('snapshotId', pymongo.ASCENDING)
                                        ])
                                check_key = is_check_keys_required(data)
                                insert_one_document(data, data['collection'], dbname, check_key)
                            else:
                                snapshot_dir = make_snapshots_dir(container)
                                if snapshot_dir:
                                    store_snapshot(snapshot_dir, data)
                            if 'masterSnapshotId' in node:
                                snapshot_data[node['snapshotId']] = node['masterSnapshotId']
                            else:
                                snapshot_data[node['snapshotId']] = False if error_str else True
                        else:
                            node['status'] = 'inactive'
                elif 'masterSnapshotId' in node:
                    mastercode = True
                    client_str, aws_region = _get_aws_client_data_from_node(node,
                        default_client=connector_client_str, default_region=region)
                    if not _validate_client_name(client_str):
                        logger.error("Invalid Client Name")
                        return snapshot_data
                    if aws_region:
                        all_regions = [aws_region]
                    else:
                        all_regions = Session().get_available_regions(client_str.lower())
                        if client_str.lower() in ['s3','cloudtrail']:
                            all_regions = ['us-west-1']
                    logger.info("Length of all regions is %s"%(str(len(all_regions))))
                    count = 0
                    snapshot_data[node['masterSnapshotId']] = []
                    for each_region in all_regions:
                        logger.info(each_region)
                        try:
                            awsclient = client(client_str.lower(), aws_access_key_id=access_key,
                                               aws_secret_access_key=secret_access, region_name=each_region)
                        except Exception as ex:
                            logger.info('Unable to create AWS client: %s', ex)
                        logger.info(awsclient)
                        if awsclient:
                            all_data = get_all_nodes(awsclient, node, snapshot, sub_data)
                            if all_data:
                                for data in all_data:
                                    snapshot_data[node['masterSnapshotId']].append(
                                        {
                                            'snapshotId': '%s%s' % (node['masterSnapshotId'], str(count)),
                                            'validate': validate,
                                            'detailMethods': data['detailMethods'],
                                            'structure': 'aws',
                                            'masterSnapshotId': node['masterSnapshotId'],
                                            'collection': data['collection'],
                                            'arn' : data['arn'],
                                            'status' : 'active'
                                        })
                                    count += 1
            if mastercode:
                snapshot_data = eliminate_duplicate_snapshots(snapshot_data)
    return snapshot_data

def is_check_keys_required(data):
    try:
        data = json.dumps(data)
        return True
    except Exception:
        return False

def eliminate_duplicate_snapshots(snapshot_data):
    data = {}
    is_updated = False
    for snapshot_id, value in snapshot_data.items():
        is_updated = False
        for count, snapshot in enumerate(value):
            for sid, sval in data.items():
                for cnt, val in enumerate(sval):
                    if sid == snapshot_id:
                        continue
                    if snapshot['arn'] == val['arn'] and snapshot['detailMethods'] == val['detailMethods']:
                        is_updated = True
                        s_id = snapshot_data[snapshot_id][count]['masterSnapshotId']
                        if isinstance(val['masterSnapshotId'], str):
                            data[sid][cnt]['masterSnapshotId'] = [s_id, val['masterSnapshotId']]
                        elif isinstance(val['masterSnapshotId'], list):
                            data[sid][cnt]['masterSnapshotId'].append(s_id)

        if not is_updated:
            data.update({snapshot_id:value})
    return data


def get_aws_client_data(aws_data, snapshot_user, account_id):
    """
    AWS client information as required by the Boto client, viz access_key
    access_secret, AWS command type like EC2, S3 etc and region
    The access_secret is either read from structure json or env variable or keyvault
    """
    accesskey = None
    secret_access = None
    region = None
    client_str = None
    if aws_data and snapshot_user:
        accounts = get_field_value(aws_data, "accounts")
        if accounts:
            found = False
            for account in accounts:
                if account_id == get_field_value(account, "account-id"):
                    users = get_field_value(account, "users")
                    if users:
                        for user in users:
                            if snapshot_user == get_field_value(user, "name"):
                                found = True
                                accesskey = get_field_value(user, 'access-key')
                                secret_access = get_field_value(user, 'secret-access')
                                region = get_field_value(user, 'region')
                                client_str = get_field_value(user, 'client')
                                if client_str and not _validate_client_name(client_str):
                                    logger.error("Invalid Client Name")
                                break
                if found:
                    break

    return accesskey, secret_access, region, client_str
