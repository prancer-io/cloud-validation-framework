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
        if isinstance(snapshot.get("resources"), list):
            for resource in snapshot.get("resources"):
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
                                        "leaked_password_path": "resources/"+resource.get("type")+"/" + "/".join([str(path) for path in path]),
                                    })
                                    issue_found = True
                                    logger.warning("Leaked Password at:%s\nvalue:%s" % (
                                        "resources/"+resource.get("type")+"/" + "/".join([str(path) for path in path]), nested_resource))
                            else:
                                issue_found = True
                                errors.append({
                                    "leaked_password_path": "resources/"+resource.get("type")+"/" + "/".join([str(path) for path in path]),
                                })
                                logger.warning("Leaked Password at:%s\nvalue:%s" % (
                                    "resources/"+resource.get("type")+"/" + "/".join([str(path) for path in path]), nested_resource))

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


def password_leak(generated_snapshot: dict) -> dict:

    PASSWORD_KEY_RE = r".*(?i)(password|securevalue|secret|privatekey|primarykey|secondarykey).*"
    PASSWORD_VALUE_RE = r'^(?!.*\$\{.*\}.*)(?=(?=.*[a-z][A-Z])|(?=.*[A-Z][a-z])|(?=.*[a-z][0-9])|(?=.*[0-9][a-z])|(?=.*[0-9][A-Z])|(?=.*[A-Z][0-9]))(.*[\^$*.\[\]{}\(\)?\-"!@\#%&\/,><\’:;|_~`]?)\S{8,99}$'
    EXCLUDE_REGEX = r'(?=.*([\[{(<]){1,})((\(.*\)){0,})((\[.*\]){0,})((\{.*\}){0,})((\<.*\>){0,})'

    output = secret_finder(
        generated_snapshot, PASSWORD_VALUE_RE, PASSWORD_KEY_RE, EXCLUDE_RE=EXCLUDE_REGEX)

    if output["issue"] == True:
        output["password_leak_err"] = "There is a possibility that secure password is exposed"

    elif output["issue"] == None:
        output["password_leak_err"] = output["err"]
        output.pop("err")

    elif output["issue"] == False:
        output["password_leak_err"] = ""
    return output


def entropy_password(generated_snapshot: dict) -> dict:

    PASSWORD_VALUE_RE = r'^(?!.*\$\{.*\}.*)(?=(?=.*[a-z][A-Z])|(?=.*[A-Z][a-z])|(?=.*[a-z][0-9])|(?=.*[0-9][a-z])|(?=.*[0-9][A-Z])|(?=.*[A-Z][0-9]))(?=.*[^A-Za-z0-9])\S{8,99}$'
    EXCLUDE_CONTAINS = ['AAD', 'AKS', 'API', 'Add', 'Advisor', 'Analysis', 'Analytics', 'Analyzer', 'App', 'Authorization', 'Automation', 'Azure', 'BI', 'Batch', 'Billing', 'Blockchain', 'Blueprints', 'Bot', 'Bus', 'CDN', 'Cache', 'Central', 'Certificate', 'Change', 'Cloud', 'Cognitive', 'Communication', 'Compute', 'Configuration', 'Consumption', 'Container', 'Cosmos', 'Custom', 'Customer', 'DB', 'DNS', 'Data', 'Databricks', 'Dedicated', 'Deployment', 'DevOps', 'DevTest', 'Device', 'Digital', 'Domain', 'Door', 'Event', 'Fabric', 'Factory', 'FarmBeats', 'Front', 'Graph', 'Grid', 'HDInsight', 'HSMs/', 'Hat', 'Hub', 'Hubs', 'Identity', 'Insights', 'Instance', 'IoT', 'Key', 'Kusto', 'Labs', 'Lake', 'Learning', 'Logic', 'Machine', 'Maintenance', 'Managed', 'Management', 'Manager', 'Maps', 'MariaDB', 'Media', 'Migrate', 'Migration', 'MySQL', 'NetApp', 'Network', 'Notification', 'Ons', 'OpenShift', 'Operational', 'Operations', 'Overview', 'Peering', 'Policy', 'Portal', 'PostgreSQL', 'Power', 'Providers', 'Provisioning', 'Recovery', 'Red', 'Registration', 'Registry', 'Relay', 'Resource', 'Resources', 'SQL', 'Scheduler', 'Search', 'Security', 'Series', 'Service', 'Services', 'Share', 'SignalR', 'Spring', 'Stack', 'StorSimple', 'Storage', 'Store', 'Stream', 'Subscription', 'Synapse', 'Sync', 'Time', 'Traffic', 'Twins', 'Update', 'Vault', 'Vaults', 'Video', 'Virtual', 'Web', 'aad', 'abandon-instances', 'abort', 'accelerator', 'accelerator-types', 'acceptedportfolioshare', 'access', 'access-approval', 'access-context-manager', 'accessanalyzer', 'accessibility', 'accesskey', 'accesspoint', 'accesspointpolicy', 'account', 'accountauditconfiguration', 'accounts', 'ack', 'ack-up-to', 'acknowledge', 'acl', 'acm', 'acmpca', 'activate', 'activate-service-account', 'active-directory', 'active-peering-zones', 'activity', 'add', 'add-access-config', 'add-backend', 'add-bgp-peer', 'add-health-checks', 'add-host-rule', 'add-iam-policy-binding', 'add-instances', 'add-interface', 'add-invoker-policy-binding', 'add-job', 'add-key', 'add-labels', 'add-metadata', 'add-path-matcher', 'add-product', 'add-resource-policies', 'add-signed-url-key', 'add-tag', 'add-tags', 'addon', 'addresses', 'agent', 'aggregationauthorization', 'ai-platform', 'alarm', 'alert', 'alexa', 'alias', 'allow', 'alpha', 'amazon', 'amazonmq', 'ami', 'ami-', 'amplify', 'analysis', 'analytics', 'analyze', 'analyze-entities', 'analyze-entity-sentiment', 'analyze-iam-policy', 'analyze-iam-policy-longrunning', 'analyze-move', 'analyze-sentiment', 'analyze-syntax', 'analyzer', 'and', 'android', 'annotation-stores', 'anomalydetector', 'anthos', 'api', 'api-configs', 'api-gateway', 'api-keys', 'apicache', 'apidestination', 'apigateway', 'apigatewaymanagedoverrides', 'apigatewayv2', 'apigee', 'apikey', 'apimapping', 'apis', 'app', 'app-engine', 'app-profiles', 'appconfig', 'appflow', 'appimageconfig', 'application', 'application-default', 'applicationautoscaling', 'applicationcloudwatchloggingoption', 'applicationinsights', 'applicationoutput', 'applicationreferencedatasource', 'applications', 'applicationversion', 'apply', 'apply-parameters', 'apply-software-update', 'appmesh', 'approve', 'apprunner', 'appspec', 'appstream', 'appsync', 'aps', 'apt', 'archive', 'archives', 'arg-files', 'arn', 'artifacts', 'ask', 'assessment', 'assessmenttarget', 'assessmenttemplate', 'asset', 'assets', 'assignment', 'associated-projects', 'association', 'associations', 'assured', 'asymmetric-decrypt', 'asymmetric-sign', 'athena', 'attach-disk', 'attachments', 'attestations', 'attestors', 'attributegroup', 'attributegroupassociation', 'attributes', 'auditmanager', 'aurora', 'auth', 'authority', 'authorization-code', 'authorization-policies', 'authorizer', 'autonomous', 'autoscaling', 'autoscaling-policies', 'autoscalinggroup', 'autoscalingplans', 'aws', 'azure', 'backend-buckets', 'backend-services', 'backup', 'backup-plans', 'backup-restore', 'backupplan', 'backups', 'backupselection', 'backupvault', 'bak', 'basepathmapping', 'batch', 'batch-translate-text', 'beta', 'bigquery', 'bigtable', 'billing', 'binauthz', 'bind', 'bindings', 'bitbucketserver', 'block', 'bms', 'border', 'branch', 'broker', 'brokers', 'browse', 'bucket', 'bucketpolicy', 'buckets', 'budget', 'budgets', 'budgetsaction', 'build', 'builds', 'bulk', 'bulk-export', 'bytematchset', 'cachecluster', 'cachepolicy', 'call', 'canary', 'cancel', 'cancel-lease', 'cancel-preview', 'capacityprovider', 'capacityreservation', 'carriergateway', 'cassandra', 'cdn', 'ce', 'certificate', 'certificate-manager', 'certificateauthority', 'certificateauthorityactivation', 'certificatemanager', 'certificates', 'changes', 'channel', 'channel-descriptors', 'channels', 'chatbot', 'cheat-sheet', 'check-data-access', 'check-iam-policy', 'check-transitive-membership', 'check-upgrade', 'classifier', 'classify-text', 'clean-up', 'cleanup', 'clear', 'cli', 'cli-trees', 'client-certificate', 'client-certs', 'client-tls-policies', 'clientcertificate', 'clients', 'clientvpnauthorizationrule', 'clientvpnendpoint', 'clientvpnroute', 'clientvpntargetnetworkassociation', 'clone', 'clone-rules', 'cloud', 'cloud-bindings', 'cloud-shell', 'cloud-source-repositories', 'cloud9', 'cloudformation', 'cloudformationproduct', 'cloudformationprovisionedproduct', 'cloudfront', 'cloudfrontoriginaccessidentity', 'cloudhub', 'cloudrun', 'cloudsql', 'cloudtrail', 'cloudwatch', 'cluster', 'clustercapacityproviderassociations', 'clusterparametergroup', 'clusters', 'clustersecuritygroup', 'clustersubnetgroup', 'cmk', 'code', 'codeartifact', 'codebuild', 'codecommit', 'codedeploy', 'codeguruprofiler', 'codegurureviewer', 'codepipeline', 'coderepository', 'codesigningconfig', 'codestar', 'codestarconnections', 'codestarnotifications', 'cofig', 'cognito', 'command', 'command-conventions', 'commands', 'commitments', 'component', 'components', 'componentversion', 'composer', 'composite', 'compositealarm', 'compute', 'computeenvironment', 'concurrency-limit', 'conditional', 'conditions', 'config', 'config-management', 'config-ssh', 'configrule', 'configs', 'configuration', 'configurationaggregator', 'configurationassociation', 'configurationprofile', 'configurationrecorder', 'configurations', 'configurationtemplate', 'configure', 'configure-docker', 'conformancepack', 'connect', 'connect-to-serial-port', 'connection', 'connection-profiles', 'connectivity-tests', 'connectordefinition', 'connectordefinitionversion', 'connectorprofile', 'connectors', 'consent-stores', 'console', 'contact', 'contactchannel', 'contacts', 'container', 'containerrecipe', 'continuous-validation', 'control', 'controller', 'copy', 'copy-files', 'copy-rules', 'coredefinition', 'coredefinitionversion', 'costcategory', 'crawler', 'crawler-runs', 'crawlers', 'create', 'create-app-engine-queue', 'create-app-engine-task', 'create-auto', 'create-aws', 'create-cred-config', 'create-from-file', 'create-http-task', 'create-instance', 'create-license', 'create-login-config', 'create-oidc', 'create-pull-queue', 'create-pull-task', 'create-signature-payload', 'create-snapshot-schedule', 'create-vm-maintenance', 'create-with-container', 'credentials', 'cron-xml-to-yaml', 'csv', 'custom-jobs', 'customactiontype', 'customdataidentifier', 'customergateway', 'customergatewayassociation', 'custommetric', 'customresource', 'dags', 'dashboard', 'dashboards', 'data', 'data-catalog', 'data-fusion', 'database', 'database-migration', 'databases', 'databrew', 'datacatalog', 'datacatalogencryptionsettings', 'dataflow', 'dataflowendpointgroup', 'datalakesettings', 'datapipeline', 'dataproc', 'dataqualityjobdefinition', 'dataset', 'datasets', 'datasource', 'datasources', 'datastore', 'datastore-indexes-xml-to-yaml', 'datastream', 'datasync', 'datetimes', 'dax', 'dbcluster', 'dbclusterparametergroup', 'dbinstance', 'dbparametergroup', 'dbproxy', 'dbproxyendpoint', 'dbproxytargetgroup', 'dbsecuritygroup', 'dbsubnetgroup', 'ddl', 'debug', 'decrypt', 'dedicated', 'default', 'deidentify', 'delegated-sub-prefixes', 'delete', 'delete-access-config', 'delete-all', 'delete-instances', 'delete-signed-url-key', 'delivery-pipelines', 'deliverychannel', 'deliverystream', 'deny', 'deploy', 'deploy-index', 'deploy-model', 'deployment', 'deployment-manager', 'deploymentconfig', 'deploymentgroup', 'deployments', 'deploymentstrategy', 'deprecate', 'describe', 'describe-explicit', 'describe-from-family', 'describe-instance', 'describe-last', 'describe-ldaps-settings', 'describe-note', 'describe-profile', 'describe-rollout', 'description', 'destination', 'destroy', 'detach-disk', 'detach-subscription', 'detect-document', 'detect-explicit-content', 'detect-faces', 'detect-image-properties', 'detect-labels', 'detect-landmarks', 'detect-language', 'detect-logos', 'detect-object', 'detect-objects', 'detect-product', 'detect-safe-search', 'detect-shot-changes', 'detect-text', 'detect-text-pdf', 'detect-text-tiff', 'detect-web', 'detective', 'detector', 'detectormodel', 'dev', 'developers', 'devendpoint', 'device', 'devicedefinition', 'devicedefinitionversion', 'devicefleet', 'devices', 'devopsguru', 'dhcpoptions', 'diagnose', 'dialogflow', 'dicom-stores', 'diff', 'dimension', 'directory', 'directoryconfig', 'directoryservice', 'disable', 'disable-debug', 'disable-enforce', 'disable-vpc-service-controls', 'discover', 'discoverer', 'disk-types', 'disks', 'dismiss', 'dispatch-xml-to-yaml', 'distribution', 'distributionconfiguration', 'dlm', 'dlp', 'dms', 'dns', 'dns-authorizations', 'dns-keys', 'docdb', 'docker', 'document', 'documentationpart', 'documentationversion', 'domain', 'domain-mappings', 'domainconfiguration', 'domainname', 'domains', 'drain', 'drop', 'dry-run', 'dynamodb', 'ebs', 'ec2', 'ec2fleet', 'ecr', 'ecs', 'ecu', 'edit', 'efs', 'egressonlyinternetgateway', 'eib', 'eip', 'eks', 'elastic', 'elasticache', 'elasticbeanstalk', 'elasticloadbalancing', 'elasticloadbalancingv2', 'elasticsearch', 'email', 'emr', 'emrcontainers', 'emulators', 'enable', 'enable-debug', 'enable-enforce', 'enable-vpc-service-controls', 'enclavecertificateiamroleassociation', 'encrypt', 'endpoint', 'endpoint-policies', 'endpointconfig', 'endpointgroup', 'endpoints', 'enforce', 'enforce-all', 'enterprise-config', 'entity-types', 'entitytype', 'entries', 'entry-groups', 'enum-values', 'env-init', 'env-unset', 'envelope', 'environment', 'environmentec2', 'environments', 'ephemeral', 'error-reporting', 'escaping', 'essential-contacts', 'etl', 'evaluate', 'evaluate-user-consents', 'event-types', 'eventarc', 'eventbus', 'eventbuspolicy', 'eventinvokeconfig', 'events', 'eventschemas', 'eventsourcemapping', 'eventsubscription', 'eventtype', 'example', 'exbibyte', 'execute', 'execute-sql', 'execution-groups', 'executions', 'expand-ip-range', 'experimenttemplate', 'explain', 'export', 'export-autoscaling', 'export-iam-policy-analysis', 'export-logs', 'export-steps', 'export-system-policy', 'external-account-keys', 'external-vpn-gateways', 'failover', 'fargateprofile', 'farm', 'fbl', 'featuregroup', 'features', 'federated', 'federation', 'feedback', 'feeds', 'fetch-for-apply', 'fetch-state', 'fetch-static-ips', 'fhir-stores', 'fhirdatastore', 'fields', 'file', 'filestore', 'filesystem', 'filter', 'filters', 'fim', 'findings', 'findingsfilter', 'finspace', 'firebase', 'firehose', 'firestore', 'firewall', 'firewall-policies', 'firewall-rules', 'firewalldomainlist', 'firewallpolicy', 'firewallrulegroup', 'firewallrulegroupassociation', 'fis', 'flags', 'flags-file', 'fleet', 'fleetmetric', 'flex-template', 'flow', 'flowentitlement', 'flowlog', 'flowoutput', 'flowsource', 'flowvpcinterface', 'fms', 'folders', 'for', 'format', 'formats', 'forums', 'forwarding-rules', 'frauddetector', 'fsx', 'function', 'functionconfiguration', 'functiondefinition', 'functiondefinitionversion', 'functions', 'future-reservations', 'game', 'gamelift', 'gameservergroup', 'gamesessionqueue', 'gateway', 'gatewayresponse', 'gatewayroute', 'gatewayroutetableassociation', 'gateways', 'gcloud', 'gcloudignore', 'gcs', 'gen-config', 'gen-repo-info-file', 'generate-gateway-rbac', 'generate-import', 'generate-ssh-script', 'genomics', 'geofencecollection', 'geomatchset', 'get', 'get-ancestors', 'get-ancestors-iam-policy', 'get-auth-string', 'get-authorization', 'get-ca-certs', 'get-certificate-chain', 'get-config', 'get-credentials', 'get-csr', 'get-diagnostics', 'get-effective-firewalls', 'get-guest-attributes', 'get-health', 'get-history', 'get-host-project', 'get-iam-policy', 'get-key-string', 'get-kubeconfig', 'get-membership-graph', 'get-mount-command', 'get-named-ports', 'get-nat-mapping-info', 'get-operation', 'get-parent', 'get-project', 'get-public-cert', 'get-public-key', 'get-register-parameters', 'get-screenshot', 'get-serial-port-output', 'get-server-config', 'get-shielded-identity', 'get-status', 'get-supported-languages', 'get-transfer-parameters', 'get-value', 'gib', 'gibibyte', 'github', 'githubrepository', 'gke', 'globalaccelerator', 'globalcluster', 'globalnetwork', 'globalreplicationgroup', 'globaltable', 'glue', 'gradle', 'grant', 'graph', 'graphqlapi', 'graphqlschema', 'greengrass', 'greengrassv2', 'groundstation', 'group', 'group-placement', 'groups', 'groupversion', 'grpc', 'grpc-routes', 'guardduty', 'guest-policies', 'hadoop', 'health-checks', 'healthcare', 'healthcheck', 'healthlake', 'help', 'hive', 'hl7v2-stores', 'host', 'hostedconfigurationversion', 'hostedzone', 'hot-tablets', 'hp-tuning-jobs', 'http', 'http-filters', 'http-health-checks', 'http-routes', 'http2', 'httpnamespace', 'https', 'https-health-checks', 'hub', 'hubs', 'iam', 'iap', 'identifiers', 'identity', 'identity-service', 'identitypool', 'identitypoolroleattachment', 'idp', 'ids', 'image', 'imagebuilder', 'imagepipeline', 'imagerecipe', 'images', 'imageversion', 'import', 'import-jobs', 'imports', 'index-endpoints', 'indexes', 'info', 'infrastructureconfiguration', 'ingress', 'init', 'input', 'inputsecuritygroup', 'insert', 'insightrule', 'insights', 'inspect', 'inspector', 'install', 'install-status', 'instance', 'instance-configs', 'instance-groups', 'instance-os-policies-compliances', 'instance-schedule', 'instance-templates', 'instanceaccesscontrolattributeconfiguration', 'instancefleetconfig', 'instancegroupconfig', 'instanceprofile', 'instances', 'instant-snapshots', 'instantiate', 'instantiate-from-file', 'integration', 'integrationresponse', 'intents', 'interactive', 'interconnects', 'interface', 'internetgateway', 'invalidate-cdn-cache', 'inventories', 'ios', 'iot', 'iot1click', 'iotanalytics', 'iotevents', 'iotfleethub', 'ip-blocks', 'ipset', 'is-upgradeable', 'isp', 'job', 'job-triggers', 'jobdefinition', 'jobqueue', 'jobs', 'jobtemplate', 'kendra', 'key', 'keygroup', 'keyrings', 'keys', 'keyspace', 'kib', 'kibibyte', 'kill', 'kinesis', 'kinesisanalytics', 'kinesisanalyticsv2', 'kinesisfirehose', 'kms', 'label', 'lakeformation', 'lambda', 'language', 'launchconfiguration', 'launchnotificationconstraint', 'launchroleconstraint',
                        'launchtemplate', 'launchtemplateconstraint', 'layer', 'layerversion', 'layerversionpermission', 'lease', 'ledger', 'levels', 'license', 'licensemanager', 'liens', 'lifecyclehook', 'lifecyclepolicy', 'lifesciences', 'line', 'link', 'linkassociation', 'lint-condition', 'list', 'list-associated-resources', 'list-available-features', 'list-bound-devices', 'list-cdn-cache-invalidations', 'list-crawled-urls', 'list-errors', 'list-grantable-roles', 'list-host-projects', 'list-instance-details', 'list-instances', 'list-ip-addresses', 'list-ip-owners', 'list-marks', 'list-network-endpoints', 'list-nodes', 'list-packages', 'list-preconfigured-expression-sets', 'list-products', 'list-resource-types', 'list-revisions', 'list-routes', 'list-rules', 'list-snapshots', 'list-subscriptions', 'list-tags', 'list-testable-permissions', 'list-topics', 'list-upgrades', 'list-usable', 'list-user-verified', 'list-values', 'list-vulnerabilities', 'listener', 'listenercertificate', 'listenerrule', 'lite-operations', 'lite-reservations', 'lite-subscriptions', 'lite-topics', 'loadbalancer', 'local', 'local-run', 'locales', 'localgatewayroute', 'localgatewayroutetablevpcassociation', 'location', 'locationefs', 'locationfsxwindows', 'locationnfs', 'locationobjectstorage', 'locations', 'locations3', 'locationsmb', 'log', 'loggerdefinition', 'loggerdefinitionversion', 'logging', 'loggingconfiguration', 'loggroup', 'login', 'logloop', 'logpoints', 'logs', 'logstream', 'lookoutmetrics', 'lookoutvision', 'lookup', 'mac-sign', 'mac-verify', 'machine-images', 'machine-types', 'macie', 'macro', 'macsec', 'mail', 'maintenance-window', 'maintenancewindow', 'maintenancewindowtarget', 'maintenancewindowtask', 'managed', 'managed-zones', 'managedblockchain', 'managedpolicy', 'management', 'manager', 'manifests', 'map', 'maps', 'mark-accepted', 'mark-active', 'mark-claimed', 'mark-dismissed', 'mark-failed', 'mark-succeeded', 'marker', 'master', 'matchmakingconfiguration', 'matchmakingruleset', 'mebibyte', 'media', 'mediaconnect', 'mediaconvert', 'medialive', 'member', 'memberinvitation', 'memberships', 'memcache', 'mesh', 'metastore', 'method', 'method-names', 'metricfilter', 'metrics', 'metricstream', 'mfa', 'mib', 'microsoftad', 'migrate', 'migrate-config', 'migration-jobs', 'mime', 'missionprofile', 'mitigationaction', 'ml-engine', 'mltransform', 'mobile', 'model', 'model-monitoring-jobs', 'modelbiasjobdefinition', 'modelexplainabilityjobdefinition', 'modelpackagegroup', 'modelqualityjobdefinition', 'models', 'modify-ack-deadline', 'modify-membership-roles', 'modify-message-ack-deadline', 'modify-push-config', 'moduledefaultversion', 'modules', 'moduleversion', 'monitoring', 'monitoringschedule', 'mounttarget', 'move', 'msk', 'mta', 'multi-cluster-services', 'multiregionaccesspoint', 'multiregionaccesspointpolicy', 'mvn', 'mwaa', 'mysql', 'name', 'namedquery', 'namespaces', 'natgateway', 'nats', 'neptune', 'network-connectivity', 'network-edge-security-services', 'network-endpoint-groups', 'network-firewall-policies', 'network-interfaces', 'network-management', 'network-profiles', 'network-security', 'network-services', 'networkacl', 'networkaclentry', 'networkfirewall', 'networkinsightsanalysis', 'networkinsightspath', 'networkinterface', 'networkinterfacepermission', 'networkmanager', 'networks', 'nlp', 'node', 'node-groups', 'node-pools', 'node-templates', 'node-types', 'nodegroup', 'nodetypes', 'notebookinstance', 'notebookinstancelifecycleconfig', 'notebooks', 'notification', 'notificationchannel', 'notificationrule', 'notifications', 'npm', 'nsx', 'number', 'oauth-brands', 'oauth-clients', 'object', 'observability-policies', 'offline-help', 'oidcprovider', 'open-console', 'opensearchservice', 'operations', 'ops-agents', 'opsworks', 'opsworkscm', 'optiongroup', 'org-policies', 'org-security-policies', 'organizationconfigrule', 'organizationconformancepack', 'organizations', 'origin', 'originrequestpolicy', 'os-config', 'os-inventory', 'os-login', 'os-policy-assignments', 'os-upgrade', 'outcome', 'packages', 'packet-mirrorings', 'parameter', 'parametergroup', 'partition', 'partner', 'patch', 'patch-deployments', 'patch-jobs', 'patchbaseline', 'path', 'pause', 'pca', 'pebibyte', 'peered-dns-domains', 'peerings', 'perimeters', 'period', 'permission', 'permissions', 'permissionset', 'pib', 'pig', 'pipeline', 'pipelines', 'placeindex', 'placement', 'placementgroup', 'plugins', 'policies', 'policy', 'policy-intelligence', 'policy-tags', 'policy-troubleshoot', 'pools', 'portfolio', 'portfolioprincipalassociation', 'portfolioproductassociation', 'portfolioshare', 'postgresql', 'predict', 'prediction', 'prefix', 'prefixlist', 'preparedstatement', 'preset', 'presto', 'preview', 'primarytaskset', 'print-access-token', 'print-identity-token', 'print-settings', 'private', 'private-connections', 'privateca', 'privateclouds', 'privatednsnamespace', 'product-search', 'product-sets', 'products', 'profilepermission', 'profilinggroup', 'project', 'project-configs', 'project-info', 'projections', 'projects', 'promote', 'promote-replica', 'properties', 'protocol', 'providers', 'provision', 'provisioningtemplate', 'public-advertised-prefixes', 'public-delegated-prefixes', 'public-keys', 'publicca', 'publicdnsnamespace', 'publickey', 'publictypeversion', 'publish', 'publisher', 'pubsub', 'pull', 'purge', 'pyspark', 'python', 'qldb', 'query', 'query-accessible-data', 'query-activity', 'querydefinition', 'queue', 'queue-xml-to-yaml', 'queuepolicy', 'queues', 'quicksight', 'quota', 'ram', 'ratebasedrule', 'raw-predict', 'rds', 'read', 'realms', 'realtimelogconfig', 'recaptcha', 'recipe', 'recognize', 'recognize-long-running', 'recommendations', 'recommender', 'recommender-configs', 'record-sets', 'recordset', 'recordsetgroup', 'recreate-instances', 'redact', 'redis', 'redshift', 'regexpatternset', 'regions', 'register', 'registrations', 'registries', 'registry', 'registrypolicy', 'reimage', 'reinstall', 'reject', 'releases', 'remediationconfiguration', 'remove', 'remove-backend', 'remove-bgp-peer', 'remove-dag-timeout', 'remove-health-checks', 'remove-host-rule', 'remove-iam-policy-binding', 'remove-instances', 'remove-interface', 'remove-invoker-policy-binding', 'remove-job', 'remove-key', 'remove-labels', 'remove-metadata', 'remove-path-matcher', 'remove-product', 'remove-profile', 'remove-resource-policies', 'remove-rotation-schedule', 'remove-tags', 'rename', 'renew-lease', 'repair', 'replace', 'replace-all', 'replay-recent-access', 'replicakey', 'replicate', 'replication', 'replicationconfiguration', 'replicationgroup', 'replicationinstance', 'replicationset', 'replicationsubnetgroup', 'replicationtask', 'report', 'reportgroup', 'repos', 'repositories', 'repository', 'repositoryassociation', 'representational', 'requests', 'requestvalidator', 'rerun', 'reschedule-maintenance', 'reservations', 'reset', 'reset-admin-password', 'reset-secret', 'reset-ssl-config', 'reset-windows-password', 'resize', 'resolve', 'resolver', 'resolverdnssecconfig', 'resolverendpoint', 'resolverqueryloggingconfig', 'resolverqueryloggingconfigassociation', 'resolverrule', 'resolverruleassociation', 'resource', 'resource-config', 'resource-descriptors', 'resource-keys', 'resource-manager', 'resource-policies', 'resource-settings', 'resourceassociation', 'resourcecollection', 'resourcedatasync', 'resourcedefaultversion', 'resourcedefinition', 'resourcedefinitionversion', 'resourcegroup', 'resourcegroups', 'resourcepolicy', 'resources', 'resourceshare', 'resourceupdateconstraint', 'resourceversion', 'response-policies', 'responseplan', 'restapi', 'restart', 'restart-web-server', 'restore', 'restore-backup', 'restores', 'resume', 'resume-instances', 'resume-unsupported-sdk', 'return', 'reusable-configs', 'revisions', 'revoke', 'robomaker', 'robot', 'robotapplication', 'robotapplicationversion', 'role', 'roles', 'rollback', 'rolling-action', 'rollouts', 'roots', 'rotate', 'rotationschedule', 'route', 'route53', 'route53resolver', 'routecalculator', 'routeresponse', 'routers', 'routes', 'routetable', 'rows', 'rule', 'rulegroup', 'rules', 'run', 'run-discovery', 'runtime-config', 's3', 's3objectlambda', 's3outposts', 'sagemaker', 'samlprovider', 'samplingrule', 'scalabletarget', 'scalingplan', 'scalingpolicy', 'scan', 'scan-configs', 'scan-runs', 'scc', 'schedule', 'scheduledaction', 'scheduledaudit', 'scheduler', 'schema', 'schemas', 'schemaversion', 'schemaversionmetadata', 'scp', 'script', 'sdb', 'search', 'search-all-iam-policies', 'search-all-resources', 'search-domains', 'search-transitive-groups', 'search-transitive-memberships', 'secret', 'secrets', 'secretsmanager', 'secrettargetattachment', 'security', 'security-policies', 'securityconfiguration', 'securitygroup', 'securityhub', 'securityprofile', 'seek', 'send', 'send-diagnostic-interrupt', 'server', 'server-ca-certs', 'server-tls-policies', 'servercertificate', 'servers', 'service', 'service-accounts', 'service-attachments', 'service-directory', 'service-identity', 'service-names', 'serviceaction', 'serviceactionassociation', 'servicecatalog', 'servicecatalogappregistry', 'servicediscovery', 'servicelinkedrole', 'services', 'ses', 'session', 'sessions', 'set', 'set-autohealing', 'set-autoscaling', 'set-backup', 'set-cluster-selector', 'set-dag-timeout', 'set-default', 'set-default-service', 'set-default-service-account', 'set-disk-auto-delete', 'set-iam-policy', 'set-instance-template', 'set-machine-type', 'set-managed-cluster', 'set-min-cpu-platform', 'set-mute', 'set-name', 'set-named-ports', 'set-password', 'set-policy', 'set-primary-version', 'set-quota-project', 'set-rotation-schedule', 'set-scheduling', 'set-scopes', 'set-security-policy', 'set-service-account', 'set-standby-policy', 'set-target', 'set-target-pools', 'set-traffic', 'set-usage-bucket', 'set-value', 'settings', 'sha', 'sha256', 'shared-vpc', 'show', 'show-rows', 'sign-and-create', 'sign-blob', 'sign-jwt', 'sign-on', 'sign-url', 'signer', 'signingprofile', 'simple', 'simplead', 'sims', 'simulate-maintenance-event', 'simulationapplication', 'simulationapplicationversion', 'simulator', 'single', 'sinks', 'site', 'sizeconstraintset', 'skill', 'slackchannelconfiguration', 'snapshot', 'snapshot-schedule', 'snapshots', 'sns', 'sole-tenancy', 'sosreport', 'source', 'sourcecredential', 'sources', 'spanner', 'spark', 'spark-r', 'spark-sql', 'speech', 'spokes', 'spotfleet', 'sql', 'sql-integrations', 'sqlinjectionmatchset', 'sqs', 'sse', 'ssh', 'ssh-keys', 'ssl', 'ssl-certificates', 'ssl-certs', 'ssl-policies', 'ssm', 'ssmcontacts', 'ssmincidents', 'sso', 'stack', 'stackfleetassociation', 'stackset', 'stacksetconstraint', 'stackuserassociation', 'stage', 'start', 'start-iap-tunnel', 'start-instances', 'start-update', 'startup', 'state', 'statemachine', 'states', 'status', 'step', 'stepfunctions', 'stop', 'stop-autoscaling', 'stop-instances', 'stop-proactive-update', 'storage', 'storagelens', 'store', 'storedquery', 'stream', 'stream-logs', 'streamconsumer', 'streamingdistribution', 'streams', 'sts', 'sts:', 'studio', 'studiosessionmapping', 'submit', 'subnet', 'subnetcidrblock', 'subnetgroup', 'subnets', 'subordinates', 'subscribe', 'subscription', 'subscriptiondefinition', 'subscriptiondefinitionversion', 'subscriptionfilter', 'subscriptions', 'suggest-crop', 'survey', 'suspend', 'suspend-instances', 'swf', 'synthetics', 'system', 'table', 'tables', 'tag', 'tag-templates', 'tagoption', 'tagoptionassociation', 'tags', 'tail', 'tail-serial-port-output', 'target-grpc-proxies', 'target-http-proxies', 'target-https-proxies', 'target-instances', 'target-pools', 'target-ssl-proxies', 'target-tcp-proxies', 'target-vpn-gateways', 'targetgroup', 'targets', 'task', 'taskdefinition', 'tasks', 'taskset', 'taxonomies', 'tcp', 'tcp-routes', 'tebibyte', 'template', 'templates', 'tensorboard-experiments', 'tensorboard-runs', 'tensorboard-time-series', 'tensorboards', 'terraform', 'test', 'test-ip', 'text', 'theme', 'thing', 'threatintelset', 'tib', 'tiers', 'timestream', 'tls', 'token', 'topic', 'topicpolicy', 'topicrule', 'topicruledestination', 'topics', 'tpu-vm', 'tpus', 'trace', 'tracker', 'trackerconsumer', 'trafficmirrorfilter', 'trafficmirrorfilterrule', 'trafficmirrorsession', 'trafficmirrortarget', 'trail', 'train', 'training', 'transaction', 'transcoder', 'transcribe-speech', 'transfer', 'transitgateway', 'transitgatewayattachment', 'transitgatewaymulticastdomain', 'transitgatewaymulticastdomainassociation', 'transitgatewaymulticastgroupmember', 'transitgatewaymulticastgroupsource', 'transitgatewaypeeringattachment', 'transitgatewayregistration', 'transitgatewayroute', 'transitgatewayroutetable', 'transitgatewayroutetableassociation', 'transitgatewayroutetablepropagation', 'transitgatewayvpcattachment', 'translate', 'translate-text', 'trigger', 'triggers', 'trusts', 'type-providers', 'typeactivation', 'types', 'unbind', 'undelete', 'undeploy', 'undeploy-index', 'undeploy-model', 'uninstall', 'unit', 'unlink', 'unmanage', 'unmanaged', 'unregister', 'unset', 'unset-value', 'untag', 'update', 'update-access-config', 'update-app-engine-queue', 'update-autoscaling', 'update-aws', 'update-backend', 'update-bgp-peer', 'update-container', 'update-from-file', 'update-instances', 'update-interface', 'update-ldaps-settings', 'update-marks', 'update-metadata', 'update-oidc', 'update-pull-queue', 'update-reservations', 'update-rollout', 'update-traffic', 'upgrade', 'upload', 'url-maps', 'usageplan', 'usageplankey', 'user', 'usergroup', 'userpool', 'userpoolclient', 'userpooldomain', 'userpoolgroup', 'userpoolidentityprovider', 'userpoolresourceserver', 'userpoolriskconfigurationattachment', 'userpooluicustomizationattachment', 'userpooluser', 'userpoolusertogroupattachment', 'userprofile', 'users', 'usertogroupaddition', 'validate', 'validate-message', 'validate-schema', 'validate-state', 'validation', 'values', 'variable', 'variables', 'vcenter', 'verify', 'version', 'versions', 'vgw', 'video', 'views', 'virtual', 'virtualcluster', 'virtualgateway', 'virtualization', 'virtualmfadevice', 'virtualnode', 'virtualrouter', 'virtualservice', 'vision', 'vm-maintenance', 'vmware', 'volume', 'volume-backups', 'volume-restores', 'vpc', 'vpc-access', 'vpc-peerings', 'vpccidrblock', 'vpcendpoint', 'vpcendpointconnectionnotification', 'vpcendpointservice', 'vpcendpointservicepermissions', 'vpclink', 'vpn', 'vpn-gateways', 'vpn-tunnels', 'vpnconnectionroute', 'vpngateway', 'vulnerabilities', 'vulnerability-reports', 'waf', 'wafregional', 'wafv2', 'wait', 'wait-last', 'wait-until', 'wait-until-stable', 'waitcondition', 'waitconditionhandle', 'waiters', 'wam', 'warmpool', 'watch', 'web', 'web-security-scanner', 'webacl', 'webaclassociation', 'webhook', 'worker-pools', 'workflow', 'workflow-templates', 'workflows', 'workgroup', 'workload-identity-pools', 'workloads', 'workspace', 'workspace-add-ons', 'workspaces', 'workteam', 'write', 'xray', 'xssmatchset', 'yib', 'yobibyte', 'yum', 'zebibyte', 'zib', 'zones']
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
