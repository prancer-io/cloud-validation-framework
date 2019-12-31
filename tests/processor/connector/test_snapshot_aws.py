""" Tests for snapshot azure"""
from unittest.mock import Mock

snapshot = {
    "source": "awsStructure.json",
    "testUser": "kbajey@gmail.com",
    "nodes": [
        {
            "snapshotId": "8",
            "type": "security_groups",
            "collection": "security_groups",
            "id": {"GroupNames": ["launch-wizard-1"]}
        }
    ]
}

snapshot_with_client = {
    "source": "awsStructure.json",
    "testUser": "kbajey@gmail.com",
    "nodes": [
        {
            "snapshotId": "8",
            "type": "security_groups",
            "collection": "security_groups",
            "id": {"GroupNames": ["launch-wizard-1"]},
            "region": "us-west-2",
            "client": "EC2"
        }
    ]
}
master_snapshot =  {
        "source" : "awsStructure", 
        "testUser" : "kbajey@gmail.com", 
        "projectId" : [
            "d34d6141-7a19-4458-b0dd-f038bb7760c1"
        ], 
        "type" : "aws", 
        "nodes" : [
            {
                "masterSnapshotId" : "1", 
                "arn" : "arn:aws:s3:::", 
                "collection" : "s3", 
                "listMethod" : "list_buckets", 
                "detailMethods" : [
                    "get_bucket_acl",
                ]
            }, 
            {
                "masterSnapshotId" : "101", 
                "arn" : "arn:aws:ec2:us-west-1::", 
                "collection" : "ec2", 
                "listMethod" : "describe_instances", 
                "detailMethods" : [
                    "describe_instances"
                ]
            }
        ]
    }

def mock_db_json_source():
    return True

def mock_fs_json_source():
    return False

def mock_config_value(section, key, default=None):
    if key in ['structure', "STRUCTURE"]:
        return 'structure'
    elif key == 'dbname':
        return 'dbname'
    return 'pytestdb'

def mock_snapshot_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return [{'json': snapshot}]

def mock_get_collection_size(collection_name):
    return 100

def mock_aws_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return [
      {
        'json':{
          "organization": "company1",
          "organization-unit": [
            {
              "name": "abc",
              "accounts": [
                {
                  "account-name": "Ajey K",
                  "account-description": "AWS cloud details",
                  "account-id": "3684074453691",
                  "users": [
                    {
                      "name": "kbajey@gmail.com",
                      "access-key": "AKIAIY7ZSPUJE4XLZ4WA",
                      "secret-access": "",
                      "region": "us-west-2",
                      "client": "EC2"
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    ]

def mock_aws_get_documents_wthout_client(collection, query=None, dbname=None, sort=None, limit=10):
    return [
      {
        'json':{
          "organization": "company1",
          "organization-unit": [
            {
              "name": "abc",
              "accounts": [
                {
                  "account-name": "Ajey K",
                  "account-description": "AWS cloud details",
                  "account-id": "3684074453691",
                  "users": [
                    {
                      "name": "kbajey@gmail.com",
                      "access-key": "AKIAIY7ZSPUJE4XLZ4WA",
                      "secret-access": ""
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    ]

def mock_describe_security_groups(**kwargs):
    return {'a': 'b'}

def mock_describe_regions(**kwargs):
    return {}

def mock_get_vault_data(client_id):
    return 'abcd'

def mock_get_bucket_acl(**kwargs):
    return {'hello', 'world'}


def mock_list_buckets(**kwargs):
    return {
    'Buckets': [
        {
            'Name': 'BucketA',
            'CreationDate': "datetime(2015, 1, 1)"
        },
    ],
    'Owner': {
        'DisplayName': 'string',
        'ID': 'string'
    }
}

def mock_describe_instances(**kwargs):
    return {
        'Reservations': [
            {
                'Instances': [
                    {
                        'InstanceId': 'ec2A',
                    },
                ],
            },
        ],
    }

class Meta:
    class _service_model:
        service_name = "hello"
    region_name = "world"

class MyMock(Mock):
    meta = Meta
    def __init__(*args, **kwargs):
        aws_client = args[0]

    def __getattr__(self, name):
        if name == 'describe_security_groups':
            return mock_describe_security_groups
        elif name == 'describe_regions':
            return mock_describe_regions
        elif name == 'get_bucket_acl':
            return mock_get_bucket_acl
        elif name == 'list_buckets':
            return mock_list_buckets
        elif name == 'describe_instances':
            return mock_describe_instances        
        return None

class MockSession:
    def get_available_regions(service_name):
        return ['hello']

def mock_insert_one_document(doc, collection, dbname, check_key):
    pass


def mock_client(*args, **kwargs):
    return  MyMock(*args, **kwargs)

def mock_invalid_client(*args, **kwargs):
    raise Exception("Unknown access key and secret")


def test_get_aws_describe_function():
    from processor.connector.snapshot_aws import get_aws_describe_function
    assert None == get_aws_describe_function({})
    assert 'describe_security_groups' == get_aws_describe_function({'type': 'security_groups'})

def test_get_checksum():
    from processor.connector.snapshot_aws import get_checksum
    assert get_checksum(None) is not None
    assert get_checksum('abc') is not None
    assert get_checksum(Mock()) is not None


def test_get_node():
    from processor.connector.snapshot_aws import get_node
    awsclient = MyMock()
    val = get_node(awsclient, {
            "snapshotId": "8",
            "type": "security_groups",
            "collection": "security_groups",
            "id": {"GroupNames": ["launch-wizard-1"]}
        }, 'awsStructure')
    assert val is not None
    val = get_node(awsclient, {
            "snapshotId": "8",
            "type": "security_groups",
            "collection": "security_groups",
            "id1": {"GroupNames": ["launch-wizard-1"]}
        }, 'awsStructure')
    assert val is not None
    val = get_node(awsclient, {
        "snapshotId": "8",
        "type": "security_groups1",
        "collection": "security_groups",
        "id": {"GroupNames": ["launch-wizard-1"]}
    }, 'awsStructure')
    assert val is not None
    val = get_node(awsclient, {
        "snapshotId": "8",
        "type1": "security_groups1",
        "collection": "security_groups",
        "id": {"GroupNames": ["launch-wizard-1"]}
    }, 'awsStructure')
    assert val is not None
    val = get_node(awsclient, {
        "snapshotId": "9",
        "type": "regions",
        "collection": "regions",
        "id": {"RegionNames": ["us-west-2"]}
    }, 'awsStructure')
    assert val is not None
    val = get_node(awsclient, {
        "snapshotId": "10",
        "type": "get_bucket_acl",
        "collection": "regions",
        "id": {"Bucket": "a-test-bucket-name"}
    }, 'awsStructure')
    assert val is not None


def test_get_node_from_snapshot_configuration():
    from processor.connector.snapshot_aws import get_node
    awsclient = MyMock()
    val = get_node(awsclient, {
        "snapshotId" : "10", 
        "validate" : True, 
        "detailMethods" : [
            "get_bucket_acl",
            "get_bucket_acl1", 
        ], 
        "masterSnapshotId" : "1", 
        "collection" : "s3", 
        "arn" : "arn:aws:s3:us-east-1::liqtest01"
    }, 'awsStructure')
    assert val is not None

def test_get_all_nodes(monkeypatch):
    from processor.connector.snapshot_aws import get_all_nodes
    awsclient = MyMock()
    connector = mock_aws_get_documents('hello')[0]
    node = master_snapshot['nodes'][0]
    val = get_all_nodes(awsclient, node, master_snapshot, connector)

    node = master_snapshot['nodes'][1]
    val = get_all_nodes(awsclient, node, master_snapshot, connector)

def test_db_get_aws_data(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_aws.get_documents', mock_snapshot_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_aws.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_aws.json_source', mock_db_json_source)
    from processor.connector.snapshot_aws import get_aws_data
    val = get_aws_data('awsStructure.json')
    assert True == isinstance(val, dict)


def test_filesystem_get_aws_data(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_aws.get_documents', mock_snapshot_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_aws.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_aws.json_source', mock_fs_json_source)
    from processor.connector.snapshot_aws import get_aws_data
    val = get_aws_data('awsStructure.json')
    assert True == isinstance(val, dict)


def test_populate_aws_snapshot(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_aws.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_documents', mock_aws_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_aws.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_aws.client', mock_client)
    monkeypatch.setattr('processor.connector.snapshot_aws.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_collection_size', mock_get_collection_size)
    from processor.connector.snapshot_aws import populate_aws_snapshot
    val = populate_aws_snapshot(snapshot, 'mycontainer1')
    assert val == {'8': True}

def test_populate_aws_snapshot_with_mastersnapshot(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_aws.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_documents', mock_aws_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_aws.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_aws.client', mock_client)
    monkeypatch.setattr('processor.connector.snapshot_aws.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_aws.Session', MockSession)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_collection_size', mock_get_collection_size)
    from processor.connector.snapshot_aws import populate_aws_snapshot
    val = populate_aws_snapshot(master_snapshot, 'mycontainer1')
    assert val != {}

def test_exception_populate_aws_snapshot(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_aws.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_documents', mock_aws_get_documents)
    monkeypatch.setattr('processor.connector.snapshot_aws.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_aws.client', mock_invalid_client)
    monkeypatch.setattr('processor.connector.snapshot_aws.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_collection_size', mock_get_collection_size)
    from processor.connector.snapshot_aws import populate_aws_snapshot
    val = populate_aws_snapshot(snapshot, 'mycontainer1')
    assert val == {'8': False}


def test_client_acceptance_from_snapshot(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_aws.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_documents', mock_aws_get_documents_wthout_client)
    monkeypatch.setattr('processor.connector.snapshot_aws.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_aws.client', mock_client)
    monkeypatch.setattr('processor.connector.snapshot_aws.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_collection_size', mock_get_collection_size)
    from processor.connector.snapshot_aws import populate_aws_snapshot
    val = populate_aws_snapshot(snapshot_with_client, 'mycontainer1')
    assert val == {'8': True}

def test_client_acceptance_from_snapshot_negative(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_aws.config_value', mock_config_value)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_documents', mock_aws_get_documents_wthout_client)
    monkeypatch.setattr('processor.connector.snapshot_aws.json_source', mock_db_json_source)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_vault_data', mock_get_vault_data)
    monkeypatch.setattr('processor.connector.snapshot_aws.client', mock_client)
    monkeypatch.setattr('processor.connector.snapshot_aws.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.connector.snapshot_aws.get_collection_size', mock_get_collection_size)
    from processor.connector.snapshot_aws import populate_aws_snapshot
    val = populate_aws_snapshot(snapshot, 'mycontainer1')
    assert val == {'8': False}

def test_get_function_kwargs(monkeypatch):
    from processor.connector.snapshot_aws import _get_function_kwargs
    val = _get_function_kwargs("arn:aws:rds:us-east-2::res1", "describe_db_instances", {})
    assert val ==  {'DBInstanceIdentifier': "res1"}
    val = _get_function_kwargs("arn:aws:s3:us-east-2::res1", "get_bucket_acl", {})
    assert val ==  {'Bucket': "res1"}
    val = _get_function_kwargs("arn:aws:ec2:us-east-2::res1", "describe_instances", {})
    assert val ==  {'InstanceIds': ["res1"]}
    val = _get_function_kwargs("arn:aws:elb:us-east-2::res1", "describe_load_balancers", {})
    assert val ==  {'LoadBalancerNames': ["res1"]}
    val = _get_function_kwargs("arn:aws:elb:us-east-2::res1", "describe_load_balancer_attributes", {})
    assert val ==  {'LoadBalancerName': "res1"}
    val = _get_function_kwargs("arn:aws:acm:us-east-2::res1", "describe_certificate", {})
    assert val ==  {'CertificateArn': "arn:aws:acm:us-east-2::res1"}
    val = _get_function_kwargs("arn:aws:cloudformation:us-east-2::res1", "describe_stacks", {})
    assert val ==  {'StackName': "res1"}
    val = _get_function_kwargs("arn:aws:cloudtrail:us-east-2::res1", "describe_trails", {})
    assert val ==  {'trailNameList': ["res1"]}
    val = _get_function_kwargs("arn:aws:cloudtrail:us-east-2::res1", "get_insight_selectors", {})
    assert val ==  {'TrailName': "res1"}
    val = _get_function_kwargs("arn:aws:apigateway:us-east-2::res1", "get_request_validators", {})
    assert val ==  {'restApiId': "res1"}
    existing_json = {
        'Reservations': [
            {'Instances':[
                {'ImageId': "hello"}
            ]}
        ]}
    val = _get_function_kwargs("arn:aws:ec2:us-east-2::res1", "describe_images", existing_json)
    assert val ==  {'ImageIds': ["hello"]}
    existing_json = {
        'Reservations': [
            {'Instances':[
                {'VpcId': "hello"}
            ]}
        ]}
    val = _get_function_kwargs("arn:aws:ec2:us-east-2::res1", "describe_vpcs", existing_json)
    assert val ==  {'VpcIds': ["hello"]}
    existing_json = {
        'Reservations': [
            {'Instances':[
                {'SubnetId': "hello"}
            ]}
        ]}
    val = _get_function_kwargs("arn:aws:ec2:us-east-2::res1", "describe_subnets", existing_json)
    assert val ==  {'SubnetIds': ["hello"]}
    existing_json = {
        'Reservations': [
            {'OwnerId': "world"}
        ]}
    val = _get_function_kwargs("arn:aws:ec2:us-east-2::res1", "describe_snapshots", existing_json)
    assert val ==  {'OwnerIds': ["world"]}
    existing_json = {
        'Reservations': [
            {'Instances':[
                {'ImageId': "hello"}
            ]}
        ]}










