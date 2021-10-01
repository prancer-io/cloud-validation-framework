import json
import re
import collections
import traceback
import math

from processor.logging.log_handler import getlogger
logger = getlogger()


def shannon_entropy(data):
    if not data:
        return 0
    entropy = 0
    normalized_ent = 0
    n = 0
    for x in range(256):
        p_x = float(data.count(chr(x)))/len(data)
        if p_x > 0:
            n += 1
            entropy += - p_x*math.log(p_x, 2)

    if math.log(n) > 0:
        normalized_ent = entropy / math.log(n, 2)
    return entropy, normalized_ent


def get_paths(source):
    paths = []
    if isinstance(source, collections.MutableMapping):
        for k, v in source.items():
            paths.append([k])
            paths += [[k] + x for x in get_paths(v)]
    elif isinstance(source, collections.Sequence) and not isinstance(source, str):
        for i, v in enumerate(source):
            paths.append([i])
            paths += [[i] + x for x in get_paths(v)]
    return paths


def secret_finder(snapshot, PASSWORD_VALUE_RE, PASSWORD_KEY_RE=None, EXCLUDE_RE=None, shannon_entropy_password=False):
    output = {}
    errors = []
    try:
        issue_found = False
        skipped = True
        if isinstance(snapshot.get("Resources"), list):
            for resource in snapshot.get("Resources"):
                skipped = False
                path_list = get_paths(resource)
                for path in path_list:
                    nested_resource = resource
                    for key in path:
                        nested_resource = nested_resource[key]
                        
                        if isinstance(nested_resource, (int, float, complex, bool)):
                            nested_resource = str(nested_resource)
                        
                        if isinstance(nested_resource, str) and re.match(PASSWORD_VALUE_RE, nested_resource) and (re.match(PASSWORD_KEY_RE, str(key), re.I) if PASSWORD_KEY_RE else True) and (not(re.match(EXCLUDE_RE, str(nested_resource))) if EXCLUDE_RE else True):
                            if shannon_entropy_password:
                                _, normalized_entropy = shannon_entropy(
                                    nested_resource)
                                if normalized_entropy > 0.965:
                                    errors.append({
                                        "leaked_password_path": "Resources/"+resource.get("Type")+"/" + "/".join([str(path) for path in path]),
                                    })
                                    issue_found = True
                                    logger.warning("Leaked Password at:%s\nvalue:%s" % (
                                        "Resources/"+resource.get("Type")+"/" + "/".join([str(path) for path in path]), nested_resource))
                            else:
                                issue_found = True
                                errors.append({
                                    "leaked_password_path": "Resources/"+resource.get("Type")+"/" + "/".join([str(path) for path in path]),
                                })
                                logger.warning("Leaked Password at:%s\nvalue:%s" % (
                                    "Resources/"+resource.get("Type")+"/" + "/".join([str(path) for path in path]), nested_resource))

        output["issue"] = True if issue_found else False

        if errors:
            output["errors"] = errors

        output["skipped"] = skipped
        return output
    except Exception as ex:
        print(traceback.format_exc())
        output["issue"] = None
        output["err"] = str(ex)
        output["skipped"] = skipped
        return output


def aws_password_leak(generated_snapshot: dict) -> dict:

    PASSWORD_KEY_RE = r".*(?i)password"
    PASSWORD_VALUE_RE = r'^(?!.*\$\{.*\}.*)(?=(?=.*[a-z][A-Z])|(?=.*[A-Z][a-z])|(?=.*[a-z][0-9])|(?=.*[0-9][a-z])|(?=.*[0-9][A-Z])|(?=.*[A-Z][0-9]))(.*[\^$*.\[\]{}\(\)?\-"!@\#%&\/,><\’:;|_~`]?)\S{8,99}$'
    output = secret_finder(
        generated_snapshot, PASSWORD_VALUE_RE, PASSWORD_KEY_RE)

    if output["issue"] == True:
        output["aws_password_leak_err"] = "There is a possibility that secure password is exposed"

    elif output["issue"] == None:
        output["aws_password_leak_err"] = output["err"]
        output.pop("err")

    elif output["issue"] == False:
        output["aws_password_leak_err"] = ""
    return output


def entropy_password(generated_snapshot: dict) -> dict:

    PASSWORD_VALUE_RE = r'^(?!.*\$\{.*\}.*)(?=(?=.*[a-z][A-Z])|(?=.*[A-Z][a-z])|(?=.*[a-z][0-9])|(?=.*[0-9][a-z])|(?=.*[0-9][A-Z])|(?=.*[A-Z][0-9]))(?=.*[^A-Za-z0-9])\S{8,99}$'
    EXCLUDE_CONTAINS = ['iotfleethub', 'zib', 'accesspointpolicy', 'hostedzone', 'launchtemplate', 'firehose', 'ce', 'clientcertificate', 'dns', 'list', 'customresource', 'ephemeral', 'repositoryassociation', 'flowoutput', 'assignment', 'yib', 'firewall', 'missionprofile', 'connection', 's3objectlambda', 'permissionset', 'replicationset', 'usertogroupaddition', 'networkinsightsanalysis', 'managedpolicy', 'alexa', 'dynamodb', 'deploymentgroup', 'map', 'resourcedefinition', 'firewalldomainlist', 'networkacl', 'querydefinition', 'crawler', 'conditional', 'gamesessionqueue', 'portfolio', 'xray', 'customergatewayassociation', 'autonomous', 'dbproxytargetgroup', 'functionconfiguration', 'distribution', 'imagerecipe', 'locationefs', 'clientvpnauthorizationrule', 'deliverystream', 'routetable', 'domainconfiguration', 'maintenancewindowtarget', 'task', 'githubrepository', 'instance', 'nodegroup', 'management', 'routecalculator', 'applicationcloudwatchloggingoption', 'elasticsearch', 'schemaversionmetadata', 'pca', 'connectordefinition', 'server', 'eip', 'gatewayroute', 'filesystem', 'dbcluster', 'loggroup', 'custommetric', 'destination', 'profilepermission', 'eib', 'unit', 'distributionconfiguration', 'opensearchservice', 'function', 'border', 'skill', 'step', 'resolverruleassociation', 'ask', 'image', 'backupvault', 'dbproxy', 'cmk', 'subscriptiondefinitionversion', 'schedule', 'analytics', 'dimension', 'idp', 'tagoption', 'datasync', 'elasticbeanstalk', 'recipe', 'compositealarm', 'transitgatewayroutetableassociation', 'usageplankey', 'virtualcluster', 'networkinterface', 'ram', 'stepfunctions', 'registry', 'volume', 'elasticloadbalancingv2', 'clustercapacityproviderassociations', 'store', 'clientvpnendpoint', 'robotapplicationversion', 'apigatewayv2', 'access', 'elasticloadbalancing', 'subscription', 'glue', 'notebookinstancelifecycleconfig', 'ami-', 'signer', 'domain', 'domainname', 'metricstream', 'launchconfiguration', 'codestarnotifications', 'securitygroup', 'mib', 'wafv2', 'autoscalingplans', 'reportgroup', 'cloudfrontoriginaccessidentity', 'pib', 'macro', 'streamingdistribution', 'clustersecuritygroup', 'permission', 'cloudformation', 'ssmcontacts', 'locationobjectstorage', 'manager', 'sdb', 'multiregionaccesspointpolicy', 'healthcheck', 'yobibyte', 'codestarconnections', 'coredefinitionversion', 'account', 'resourcedefaultversion', 'fsx', 'graphqlschema', 'tracker', 'configurationaggregator', 'securityconfiguration', 'license', 'lookup', 'waitconditionhandle', 'configurationtemplate', 'scalingpolicy', 'imageversion', 'inspector', 'iot1click', 'rds', 'routeresponse', 'theme', 'timestream', 'slackchannelconfiguration', 'pebibyte', 'accesskey', 'appmesh', 'protocol', 'athena', 'environment', 'certificateauthorityactivation', 'parametergroup', 'farm', 'greengrassv2', 'robot', 'primarytaskset', 'codestar', 'httpnamespace', 'virtualmfadevice', 'mta', 'moduledefaultversion', 'file', 'ipset', 'trafficmirrorsession', 'streamconsumer', 'qldb', 'resourceshare', 'activity', 'fms', 'replicakey', 'usageplan', 'certificateauthority', 'insightrule', 'resourcecollection', 'launchroleconstraint', 'oidcprovider', 'acmpca', 'placementgroup', 'workgroup', 'origin', 'publickey', 'trafficmirrorfilter', 'appstream', 'replicationconfiguration', 'waitcondition', 'configurationrecorder', 'ecr', 'representational', 'token', 'topicruledestination', 'tagoptionassociation', 'userpooldomain', 'configrule', 'assessmenttarget', 'vpc', 'kibibyte', 'table', 'devopsguru', 'schemaversion', 'notificationchannel', 'notebookinstance', 'basepathmapping', 'vpngateway', 'notificationrule', 'trail', 'accountauditconfiguration', 'codeartifact', 'databrew', 'hub', 'mediaconnect', 'datacatalog', 'groupversion', 'devicedefinitionversion', 'certificate', 'robotapplication', 'bucket', 'flowentitlement', 'transfer', 'secretsmanager', 'service', 'thing', 'amazonmq', 'assessment', 'apimapping', 'trackerconsumer', 'publisher', 'trafficmirrortarget', 'filter', 'opsworkscm', 'resolver', 'cachepolicy', 'samlprovider', 'app', 'example', 'budgets', 'link', 'gameservergroup', 'mobile', 'firewallpolicy', 'globalnetwork', 'devicedefinition', 'portfolioproductassociation', 'apidestination', 'cloudfront', 'dbparametergroup', 'archive', 'virtualservice', 'workteam', 'private', 'subscriptiondefinition', 'replicationgroup', 'sse', 'ecs', 'replicationtask', 'ledger', 'datasource', 'resolverrule', 'alert', 'container', 'simulator', 'originrequestpolicy', 'compute', 'group', 'documentationpart', 'msk', 'virtualization', 'userpoolriskconfigurationattachment', 'single', 'aurora', 'publictypeversion', 'mwaa', 'storedquery', 'mounttarget', 'exbibyte', 'cloud', 'networkmanager', 'analyzer', 'endpointgroup', 'dbinstance', 'listener', 'loggingconfiguration', 'description', 'webaclassociation', 'build', 'lambda', 'costcategory', 'vgw', 'sourcecredential', 'mitigationaction', 'rulegroup', 'sqs', 'eventschemas', 'modelexplainabilityjobdefinition', 'route53', 'sagemaker', 'federated', 'configurationassociation', 'customactiontype', 'lookoutmetrics', 'sizeconstraintset', 'workflow', 'identifiers', 'endpoint', 'natgateway', 'chatbot', 'neptune', 'block', 'kib', 'authorizer', 'variable', 'mfa', 'frauddetector', 'coderepository', 'flow', 'opsworks', 'configurationprofile', 'functiondefinitionversion', 'streams', 'sso', 'localgatewayroute', 'taskset', 'capacityreservation', 'instanceprofile', 'input', 'wafregional', 'wam', 'dbproxyendpoint', 'environmentec2', 'lifecyclehook', 'memberinvitation', 'regexpatternset', 'instancefleetconfig', 'docdb', 'graphqlapi', 'subscriptionfilter', 'waf', 'iotanalytics', 'stacksetconstraint', 'layerversionpermission', 'site', 'virtual', 'sns', 'detective', 'eventinvokeconfig', 'resolverendpoint', 'ssmincidents', 'webhook', 'patchbaseline', 'subnet', 'userpoolidentityprovider', 'notification', 'default', 'userpoolusertogroupattachment', 'microsoftad', 'apigatewaymanagedoverrides', 'hostedconfigurationversion', 'application', 'secret', 'virtualnode', 'bucketpolicy', 'resourcegroup', 'rotationschedule', 'clustersubnetgroup', 'userpoolresourceserver', 'repository', 'association', 'dbsubnetgroup', 'kinesis', 'logloop', 'state', 'threatintelset', 'fleetmetric', 'mesh', 'cognito', 'acceptedportfolioshare', 'provisioningtemplate', 'groundstation', 'acl', 'transitgatewaymulticastdomain', 'configuration', 'appconfig', 'dataflowendpointgroup', 'quicksight', 'cloudhub', 'master', 'ec2fleet', 'iot', 'analysis', 'scalabletarget', 'logs', 'flowvpcinterface', 'stackfleetassociation', 'cassandra', 'tib', 'subnetgroup', 'apigateway', 'transitgatewaypeeringattachment', 'transitgatewayvpcattachment', 'user', 'mediaconvert', 'backupplan', 'attributegroupassociation',
                        'cloudwatch', 'sqlinjectionmatchset', 'imagepipeline', 'userpoolgroup', 'feedback', 'cli', 'efs', 'locationnfs', 'line', 'storage', 'resource', 'forums', 'medialive', 'tag', 'locations3', 'device', 'datapipeline', 'flowsource', 'dashboard', 'object', 'transitgatewaymulticastgroupmember', 'fim', 'interface', 'servercertificate', 'integration', 'transitgatewayroutetablepropagation', 'kms', 'acm', 'publicdnsnamespace', 'batch', 'computeenvironment', 'transitgatewaymulticastdomainassociation', 'marker', 'topicpolicy', 'contactchannel', 'stackuserassociation', 'customdataidentifier', 'deploymentconfig', 'lakeformation', 'matchmakingruleset', 'mime', 'template', 'sims', 'project', 'detector', 'directoryservice', 'replicationinstance', 'preparedstatement', 'emr', 'session', 'directory', 'ebs', 'fargateprofile', 'federation', 'grant', 'auditmanager', 'connectordefinitionversion', 'system', 'dms', 'maintenancewindowtask', 'emrcontainers', 'eventbus', 'route53resolver', 'version', 'elastic', 'sts', 'codecommit', 'format', 'cloudtrail', 'resourcepolicy', 'deploymentstrategy', 'accelerator', 'aggregationauthorization', 'discoverer', 'attributegroup', 'portfolioprincipalassociation', 'globalreplicationgroup', 'responseplan', 'transitgatewaymulticastgroupsource', 'userpool', 'command', 'console', 'properties', 'locationsmb', 'codeguruprofiler', 'componentversion', 'monitoringschedule', 'rule', 'jobdefinition', 'applicationautoscaling', 'devendpoint', 'apicache', 'launchtemplateconstraint', 'listenerrule', 'securityhub', 'loadbalancer', 'budget', 'replicationsubnetgroup', 'jobtemplate', 'mltransform', 'linkassociation', 'servicediscovery', 'applicationinsights', 'datalakesettings', 'networkinterfacepermission', 'role', 'resourcedefinitionversion', 'resolverqueryloggingconfigassociation', 'servicecatalogappregistry', 'web', 'modelbiasjobdefinition', 'queuepolicy', 'security', 'gatewayresponse', 'partition', 'typeactivation', 'lookoutvision', 'stackset', 'datacatalogencryptionsettings', 'gamelift', 'studiosessionmapping', 'classifier', 'language', 'cloudformationprovisionedproduct', 'fis', 'integrationresponse', 'authority', 'scalingplan', 'dbclusterparametergroup', 'document', 'profilinggroup', 'amplify', 'channel', 'appimageconfig', 'directoryconfig', 'ratebasedrule', 'remediationconfiguration', 'simple', 'validation', 'eventsourcemapping', 'fbl', 'macie', 'vpccidrblock', 'ami', 'return', 'kinesisanalyticsv2', 'metricfilter', 'recordset', 'elasticache', 'organizationconformancepack', 'applicationreferencedatasource', 'policy', 'realtimelogconfig', 'ec2', 'locationfsxwindows', 'layer', 'keyspace', 'cachecluster', 'member', 'etl', 'simulationapplicationversion', 'method', 'userprofile', 'resourcedatasync', 'userpooluicustomizationattachment', 'launchnotificationconstraint', 'dataset', 'label', 'clusterparametergroup', 'privatednsnamespace', 'prefixlist', 'tebibyte', 'organizationconfigrule', 'location', 'localgatewayroutetablevpcassociation', 'servicecatalog', 'dlm', 'branch', 'appsync', 'managedblockchain', 'sts:', 'mebibyte', 'transitgateway', 'schema', 'networkfirewall', 'stage', 'fhirdatastore', 'accesspoint', 'job', 'iam', 'imagebuilder', 'resources', 'conformancepack', 'identitypoolroleattachment', 'storagelens', 'geofencecollection', 'serviceaction', 'redshift', 'globalcluster', 'accessanalyzer', 'eventtype', 'connectorprofile', 'deployment', 's3', 'loggerdefinitionversion', 'autoscaling', 'scp', 'resourcegroups', 'swf', 'firewallrulegroupassociation', 'alarm', 'usergroup', 'guardduty', 'matchmakingconfiguration', 'secrettargetattachment', 'statemachine', 'virtualgateway', 'robomaker', 'cloud9', 'recordsetgroup', 'deliverychannel', 'ssm', 'broker', 'taskdefinition', 'targetgroup', 'coredefinition', 'database', 'host', 'clientvpnroute', 'jobqueue', 'route', 'vpcendpoint', 'workspaces', 'config', 'logstream', 'tls', 'securityprofile', 'vpn', 'datastore', 'xssmatchset', 'vpcendpointconnectionnotification', 'agent', 'events', 'inputsecuritygroup', 'transitgatewayregistration', 'vpcendpointservice', 'cofig', 'gib', 'aps', 'capacityprovider', 'samplingrule', 'backupselection', 'infrastructureconfiguration', 'gatewayroutetableassociation', 'healthlake', 'studio', 'appspec', 'cluster', 'licensemanager', 'envelope', 'placeindex', 'topicrule', 'moduleversion', 'script', 'name', 'applicationversion', 'layerversion', 'lifecyclepolicy', 'namedquery', 'networkinsightspath', 'registrypolicy', 'maintenancewindow', 'internetgateway', 'resourceversion', 'webacl', 'clientvpntargetnetworkassociation', 'arn', 'vpcendpointservicepermissions', 'aws', 'networkaclentry', 'budgetsaction', 'experimenttemplate', 'path', 'enclavecertificateiamroleassociation', 'autoscalinggroup', 'anomalydetector', 'geomatchset', 'parameter', 'applicationoutput', 'ses', 'firewallrulegroup', 'resourceassociation', 'signingprofile', 'transitgatewayroute', 'number', 'eventbuspolicy', 'stream', 'aad', 'resolverdnssecconfig', 'multiregionaccesspoint', 'dhcpoptions', 'carriergateway', 'simplead', 'userpooluser', 'instancegroupconfig', 'codebuild', 'isp', 'canary', 'spotfleet', 'featuregroup', 'portfolioshare', 'dbsecuritygroup', 'amazon', 'transitgatewayroutetable', 'apikey', 'assessmenttemplate', 'trafficmirrorfilterrule', 'ecu', 'component', 'model', 'identitypool', 'fleet', 'apprunner', 'simulationapplication', 'kinesisanalytics', 'certificatemanager', 'functiondefinition', 'dataqualityjobdefinition', 'zebibyte', 'resolverqueryloggingconfig', 'dax', 'egressonlyinternetgateway', 'resourceupdateconstraint', 'stack', 'contact', 'userpoolclient', 'modelqualityjobdefinition', 'trigger', 'backup', 'iotevents', 'preset', 'sign-on', 'customergateway', 'gibibyte', 'node', 'alias', 'codegurureviewer', 'key', 'placement', 'restapi', 'warmpool', 'endpointconfig', 'greengrass', 'permissions', 'loggerdefinition', 'requestvalidator', 'api', 'pipeline', 'vpclink', 'services', 'bytematchset', 'eks', 'listenercertificate', 'codesigningconfig', 'topic', 'kinesisfirehose', 'cloudformationproduct', 'addon', 'devicefleet', 'queue', 'containerrecipe', 'transitgatewayattachment', 'vpnconnectionroute', 'gateway', 'cdn', 'servicelinkedrole', 'kendra', 'billing', 'serviceactionassociation', 'codepipeline', 'control', 'prefix', 'detectormodel', 'scheduledaction', 'entitytype', 'graph', 'globaltable', 'finspace', 'flowlog', 'appflow', 'instanceaccesscontrolattributeconfiguration', 's3outposts', 'synthetics', 'optiongroup', 'subnetcidrblock', 'mail', 'email', 'codedeploy', 'identity', 'findingsfilter', 'virtualrouter', 'workspace', 'and', 'globalaccelerator', 'period', 'scheduledaudit', 'modelpackagegroup', 'documentationversion', 'keygroup', 'outcome', 'eventsubscription', 'sha', 'sha256']
    EXCLUDE_REGEX = [
        "(?=^([a-zA-Z0-9]+\.+[a-zA-Z0-9]+\.[a-zA-Z0-9]+)(?![A-Za-z0-9])$)",
        "(?=^([a-zA-Z0-9]+\.+[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+)(?![A-Za-z0-9])$)",
        "(?=^([a-zA-Z0-9]+\_+[a-zA-Z0-9]+\_[a-zA-Z0-9]+)(?![A-Za-z0-9])$)",
        "(?=^([a-zA-Z0-9]+\-+[a-zA-Z0-9]+\-[a-zA-Z0-9]+)(?![A-Za-z0-9])$)",
        "(?=^([a-zA-Z0-9]+\.+[a-zA-Z0-9]*)$)",
        "(?=^(\/+\w{0,}){0,}$)",
        "(?=^([a-zA-Z0-9]*_[a-zA-Z0-9]*)$)",
        "(?=^([a-zA-Z0-9]*-[a-zA-Z0-9]*)$)",
    ]
    EXCLUDE_STARTSWITH = [
        "arn:"
    ]

    exclude_contains_regex = "(?=.*(?i)(%s).*)" % ("|".join(EXCLUDE_CONTAINS))

    exclude_startswith_regex = "(?=(%s))" % (
        "|".join(["^"+exclude for exclude in EXCLUDE_STARTSWITH]))
    exclude_regex = "|".join(EXCLUDE_REGEX)

    combined_exclude_regex = "|".join(
        [exclude_contains_regex, exclude_startswith_regex, exclude_regex])
    combined_exclude_regex = re.compile(combined_exclude_regex)

    output = secret_finder(
        generated_snapshot, PASSWORD_VALUE_RE, PASSWORD_KEY_RE=None, EXCLUDE_RE=combined_exclude_regex, shannon_entropy_password=True)

    if output["issue"] == True:
        output["entropy_password_err"] = "There is a possibility that Random secure password is exposed"

    elif output["issue"] == None:
        output["entropy_password_err"] = output["err"]
        output.pop("err")

    else:
        output["entropy_password_err"] = ""
    return output


def gl_aws_secrets(generated_snapshot: dict) -> dict:

    PASSWORD_KEY_RE = r"^(?i)aws_?(secret)?_?(access)?_?key$"
    PASSWORD_VALUE_RE = r"^[A-Za-z0-9/\\+=]{40}$"
    output = secret_finder(
        generated_snapshot, PASSWORD_VALUE_RE, PASSWORD_KEY_RE)

    if output["issue"] == True:
        output["gl_aws_secrets_err"] = "There is a possibility that AWS secret access key has leaked"

    elif output["issue"] == None:
        output["gl_aws_secrets_err"] = output["err"]
        output.pop("err")

    else:
        output["gl_aws_secrets_err"] = ""
    return output


def gl_aws_account(generated_snapshot: dict) -> dict:

    PASSWORD_KEY_RE = r"^(?i)aws_?(account)_?(id)$"
    PASSWORD_VALUE_RE = r"^[0-9]{12}$"
    output = secret_finder(
        generated_snapshot, PASSWORD_VALUE_RE, PASSWORD_KEY_RE)

    if output["issue"] == True:
        output["gl_aws_account_err"] = "There is a possibility that AWS account ID has leaked"

    elif output["issue"] == None:
        output["gl_aws_account_err"] = output["err"]
        output.pop("err")

    else:
        output["gl_aws_account_err"] = ""
    return output


def al_access_key_id(generated_snapshot: dict) -> dict:
    PASSWORD_KEY_RE = r"^(?i)aws_?(access)_?(key)_?(id)_?$"
    PASSWORD_VALUE_RE = r"^(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}"
    output = secret_finder(
        generated_snapshot, PASSWORD_VALUE_RE, PASSWORD_KEY_RE)
    if output["issue"] == True:
        output["al_access_key_id_err"] = "There is a possibility that Aws access key id is exposed"

    elif output["issue"] == None:
        output["al_access_key_id_err"] = output["err"]
        output.pop("err")
    else:
        output["al_access_key_id_err"] = ""
    return output


def al_mws(generated_snapshot: dict) -> dict:
    PASSWORD_VALUE_RE = r"(?i)amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    output = secret_finder(generated_snapshot, PASSWORD_VALUE_RE)

    if output["issue"] == True:
        output["al_mws_err"] = "There is a possibility that Amazon Marketplace Web Service secret key is exposed"

    elif output["issue"] == None:
        output["al_mws_err"] = output["err"]
        output.pop("err")

    else:
        output["al_mws_err"] = ""
    return output
