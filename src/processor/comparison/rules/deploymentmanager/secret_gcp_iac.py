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


def google_password_leak(generated_snapshot: dict, kwargs={}) -> dict:

    PASSWORD_KEY_RE = r".*(?i)(password|secret).*"
    PASSWORD_VALUE_RE = r'^(?=^(?!\$\{.*\}$))(?=(?=.*[a-z][A-Z])|(?=.*[A-Z][a-z])|(?=.*[a-z][0-9])|(?=.*[0-9][a-z])|(?=.*[0-9][A-Z])|(?=.*[A-Z][0-9]))(.*[\^$*.\[\]{}\(\)?\-"!@\#%&\/,><\’:;|_~`]?)\S{8,99}$'
    EXCLUDE_REGEX = r'(?=.*([\[{(<]){1,})((\(.*\)){0,})((\[.*\]){0,})((\{.*\}){0,})((\<.*\>){0,})'

    output = secret_finder(
        generated_snapshot, PASSWORD_VALUE_RE, PASSWORD_KEY_RE, EXCLUDE_RE=EXCLUDE_REGEX)

    if output["issue"] == True:
        output["google_password_leak_err"] = "Ensure no hardcoded password set in the template"

    elif output["issue"] == None:
        output["google_password_leak_err"] = output["err"]
        output.pop("err")

    elif output["issue"] == False:
        output["google_password_leak_err"] = ""
    return output


def entropy_password(generated_snapshot: dict, kwargs={}) -> dict:

    PASSWORD_VALUE_RE = r'^(?=^(?!\$\{.*\}$))(?=(?=.*[a-z][A-Z])|(?=.*[A-Z][a-z])|(?=.*[a-z][0-9])|(?=.*[0-9][a-z])|(?=.*[0-9][A-Z])|(?=.*[A-Z][0-9]))(?=.*[^A-Za-z0-9])\S{8,99}$'
    EXCLUDE_CONTAINS = ['gcloud', 'access-approval', 'Overview', 'requests', 'approve', 'dismiss', 'get', 'list', 'settings', 'delete', 'update', 'access-context-manager', 'cloud-bindings', 'create', 'describe', 'levels', 'conditions', 'replace-all', 'perimeters', 'dry-run', 'drop', 'enforce', 'enforce-all', 'policies', 'active-directory', 'domains', 'describe-ldaps-settings', 'get-iam-policy', 'reset-admin-password', 'set-iam-policy', 'trusts', 'validate-state', 'update-ldaps-settings', 'operations', 'cancel', 'custom-jobs', 'stream-logs', 'endpoints', 'deploy-model', 'explain', 'predict', 'undeploy-model', 'hp-tuning-jobs', 'model-monitoring-jobs', 'pause', 'resume', 'models', 'upload', 'ai-platform', 'jobs', 'submit', 'prediction', 'training', 'local', 'train', 'add-iam-policy-binding', 'remove-iam-policy-binding', 'wait', 'versions', 'set-default', 'alpha', 'sql-integrations', 'peerings', 'local-run', 'raw-predict', 'index-endpoints', 'deploy-index', 'undeploy-index', 'indexes', 'tensorboard-experiments', 'tensorboard-runs', 'tensorboard-time-series', 'read', 'tensorboards', 'locations', 'anthos', 'apply', 'auth', 'login', 'config', 'controller', 'get-credentials', 'create-login-config', 'export', 'api-gateway', 'api-configs', 'apis', 'gateways', 'apigee', 'deploy', 'undeploy', 'applications', 'archives', 'deployments', 'developers', 'environments', 'organizations', 'provision', 'products', 'app', 'domain-mappings', 'ssl-certificates', 'artifacts', 'apt', 'import', 'docker', 'images', 'tags', 'add', 'packages', 'print-settings', 'gradle', 'mvn', 'npm', 'python', 'yum', 'repositories', 'asset', 'feeds', 'get-history', 'assured', 'workloads', 'activate-service-account', 'configure-docker', 'print-access-token', 'print-identity-token', 'revoke', 'bigtable', 'app-profiles', 'backups', 'clusters', 'hot-tablets', 'instances', 'tables', 'restore', 'upgrade', 'billing', 'accounts', 'projects', 'link', 'unlink', 'budgets', 'bms', 'datasets', 'copy', 'insert', 'show-rows', 'builds', 'configure', 'gke', 'enterprise-config', 'bitbucketserver', 'github', 'log', 'reject', 'triggers', 'cloud-source-repositories', 'pubsub', 'webhook', 'run', 'worker-pools', 'certificate-manager', 'certificates', 'dns-authorizations', 'maps', 'entries', 'cloud-shell', 'get-mount-command', 'scp', 'ssh', 'code', 'clean-up', 'dev', 'composer', 'check-upgrade', 'list-packages', 'list-upgrades', 'restart-web-server', 'storage', 'dags', 'data', 'plugins', 'compute', 'accelerator-types', 'addresses', 'backend-buckets', 'add-signed-url-key', 'delete-signed-url-key', 'backend-services', 'add-backend', 'edit', 'get-health', 'remove-backend', 'set-security-policy', 'update-backend', 'commitments', 'create-license', 'update-reservations', 'config-ssh', 'connect-to-serial-port', 'copy-files', 'diagnose', 'export-logs', 'routes', 'sosreport', 'disk-types', 'disks', 'add-labels', 'add-resource-policies', 'move', 'remove-labels', 'remove-resource-policies', 'resize', 'snapshot', 'external-vpn-gateways', 'firewall-policies', 'associations', 'clone-rules', 'list-rules', 'rules', 'firewall-rules', 'forwarding-rules', 'set-target', 'future-reservations', 'health-checks', 'grpc', 'http', 'http2', 'https', 'ssl', 'tcp', 'http-health-checks', 'https-health-checks', 'deprecate', 'describe-from-family', 'diff', 'vulnerabilities', 'describe-note', 'instance-groups', 'get-named-ports', 'list-instances', 'managed', 'abandon-instances', 'create-instance', 'delete-instances', 'describe-instance', 'export-autoscaling', 'instance-configs', 'list-errors', 'recreate-instances', 'resume-instances', 'rolling-action', 'replace', 'restart', 'start-update', 'stop-proactive-update', 'set-autohealing', 'set-autoscaling', 'set-instance-template', 'set-named-ports', 'set-standby-policy', 'set-target-pools', 'start-instances', 'stop-autoscaling', 'stop-instances', 'suspend-instances', 'update-autoscaling', 'update-instances', 'wait-until', 'wait-until-stable', 'unmanaged', 'add-instances', 'remove-instances', 'instance-templates', 'create-with-container', 'add-access-config', 'add-metadata', 'add-tags', 'attach-disk', 'bulk', 'delete-access-config', 'detach-disk', 'get-guest-attributes', 'get-serial-port-output', 'get-shielded-identity', 'network-interfaces', 'get-effective-firewalls', 'ops-agents', 'os-inventory', 'remove-metadata', 'remove-tags', 'reset', 'send-diagnostic-interrupt', 'set-disk-auto-delete', 'set-machine-type', 'set-min-cpu-platform', 'set-name', 'set-scheduling', 'set-scopes', 'simulate-maintenance-event', 'start', 'stop', 'suspend', 'tail-serial-port-output', 'update-access-config', 'update-container', 'update-from-file', 'instant-snapshots', 'interconnects', 'attachments', 'dedicated', 'partner', 'get-diagnostics', 'macsec', 'add-key', 'get-config', 'remove-key', 'machine-images', 'machine-types', 'network-edge-security-services', 'network-endpoint-groups', 'list-network-endpoints', 'network-firewall-policies', 'networks', 'list-ip-addresses', 'list-ip-owners', 'list-routes', 'subnets', 'expand-ip-range', 'list-usable', 'org-security-policies', 'copy-rules', 'os-config', 'guest-policies', 'lookup', 'instance-os-policies-compliances', 'inventories', 'os-policy-assignments', 'list-revisions', 'os-upgrade', 'patch-deployments', 'patch-jobs', 'execute', 'list-instance-details', 'vulnerability-reports', 'os-login', 'describe-profile', 'remove-profile', 'ssh-keys', 'remove', 'packet-mirrorings', 'project-info', 'set-default-service-account', 'set-usage-bucket', 'public-advertised-prefixes', 'public-delegated-prefixes', 'delegated-sub-prefixes', 'regions', 'reservations', 'reset-windows-password', 'resource-policies', 'group-placement', 'instance-schedule', 'snapshot-schedule', 'vm-maintenance', 'concurrency-limit', 'maintenance-window', 'create-snapshot-schedule', 'create-vm-maintenance', 'routers', 'add-bgp-peer', 'add-interface', 'get-nat-mapping-info', 'get-status', 'nats', 'remove-bgp-peer', 'remove-interface', 'update-bgp-peer', 'update-interface', 'security-policies', 'list-preconfigured-expression-sets', 'service-attachments', 'shared-vpc', 'associated-projects', 'disable', 'enable', 'get-host-project', 'list-associated-resources', 'list-host-projects', 'sign-url', 'snapshots', 'sole-tenancy', 'node-groups', 'list-nodes', 'node-templates', 'node-types', 'ssl-policies', 'list-available-features', 'start-iap-tunnel', 'target-grpc-proxies', 'target-http-proxies', 'target-https-proxies', 'target-instances', 'target-pools', 'add-health-checks', 'remove-health-checks', 'set-backup', 'target-ssl-proxies', 'target-tcp-proxies', 'target-vpn-gateways', 'tpus', 'execution-groups', 'reimage', 'tpu-vm', 'service-identity', 'url-maps', 'add-host-rule', 'add-path-matcher', 'invalidate-cdn-cache', 'list-cdn-cache-invalidations', 'remove-host-rule', 'remove-path-matcher', 'set-default-service', 'validate', 'vpn-gateways', 'vpn-tunnels', 'zones', 'configurations', 'activate', 'set', 'unset', 'container', 'aws', 'get-kubeconfig', 'get-server-config', 'node-pools', 'azure', 'clients', 'get-public-cert', 'backup-restore', 'backup-plans', 'restores', 'volume-backups', 'volume-restores', 'binauthz', 'attestations', 'sign-and-create', 'attestors', 'public-keys', 'continuous-validation', 'create-signature-payload', 'policy', 'export-system-policy', 'create-auto', 'hub', 'cloudrun', 'config-management', 'fetch-for-apply', 'status', 'unmanage', 'version', 'features', 'identity-service', 'ingress', 'memberships', 'generate-gateway-rbac', 'register', 'unregister', 'mesh', 'multi-cluster-services', 'service-directory', 'add-tag', 'list-tags', 'untag', 'rollback', 'data-catalog', 'crawler-runs', 'crawlers', 'entry-groups', 'search', 'tag-templates', 'fields', 'enum-values', 'rename', 'taxonomies', 'policy-tags', 'database-migration',
                        'connection-profiles', 'cloudsql', 'mysql', 'migration-jobs', 'generate-ssh-script', 'promote', 'verify', 'dataflow', 'export-steps', 'resume-unsupported-sdk', 'logs', 'metrics', 'dataproc', 'autoscaling-policies', 'create-from-file', 'kill', 'hadoop', 'hive', 'pig', 'presto', 'pyspark', 'spark', 'spark-r', 'spark-sql', 'workflow-templates', 'add-job', 'instantiate', 'instantiate-from-file', 'remove-dag-timeout', 'remove-job', 'set-cluster-selector', 'set-dag-timeout', 'set-managed-cluster', 'datastore', 'databases', 'cleanup', 'delivery-pipelines', 'releases', 'rollouts', 'targets', 'deployment-manager', 'cancel-preview', 'manifests', 'resources', 'type-providers', 'types', 'dialogflow', 'agent', 'query', 'entity-types', 'intents', 'dlp', 'datasources', 'bigquery', 'analyze', 'inspect', 'gcs', 'redact', 'job-triggers', 'text', 'dns', 'active-peering-zones', 'dns-keys', 'managed-zones', 'record-sets', 'changes', 'transaction', 'abort', 'response-policies', 'registrations', 'authorization-code', 'contacts', 'management', 'get-register-parameters', 'get-transfer-parameters', 'search-domains', 'transfer', 'emulators', 'env-init', 'env-unset', 'firestore', 'spanner', 'configs', 'quota', 'services', 'check-iam-policy', 'undelete', 'essential-contacts', 'filestore', 'firebase', 'test', 'android', 'locales', 'ios', 'ip-blocks', 'network-profiles', 'composite', 'functions', 'add-invoker-policy-binding', 'call', 'event-types', 'remove-invoker-policy-binding', 'game', 'servers', 'describe-rollout', 'fetch-state', 'update-rollout', 'realms', 'genomics', 'pipelines', 'healthcare', 'annotation-stores', 'evaluate', 'consent-stores', 'check-data-access', 'evaluate-user-consents', 'query-accessible-data', 'deidentify', 'dicom-stores', 'fhir-stores', 'hl7v2-stores', 'nlp', 'analyze-entities', 'help', 'iam', 'list-grantable-roles', 'list-testable-permissions', 'lint-condition', 'roles', 'service-accounts', 'keys', 'get-public-key', 'sign-blob', 'sign-jwt', 'workload-identity-pools', 'create-cred-config', 'providers', 'create-aws', 'create-oidc', 'update-aws', 'update-oidc', 'iap', 'oauth-brands', 'oauth-clients', 'reset-secret', 'web', 'identity', 'groups', 'check-transitive-membership', 'get-membership-graph', 'modify-membership-roles', 'search-transitive-groups', 'search-transitive-memberships', 'preview', 'ids', 'init', 'interactive', 'iot', 'devices', 'commands', 'send', 'get-value', 'credentials', 'clear', 'bind', 'list-bound-devices', 'unbind', 'states', 'registries', 'kms', 'asymmetric-decrypt', 'asymmetric-sign', 'decrypt', 'encrypt', 'import-jobs', 'keyrings', 'remove-rotation-schedule', 'set-primary-version', 'set-rotation-schedule', 'destroy', 'get-certificate-chain', 'mac-sign', 'mac-verify', 'lifesciences', 'logging', 'buckets', 'resource-descriptors', 'sinks', 'tail', 'views', 'write', 'media', 'memcache', 'apply-parameters', 'apply-software-update', 'metastore', 'imports', 'language', 'analyze-entity-sentiment', 'analyze-sentiment', 'analyze-syntax', 'classify-text', 'speech', 'recognize', 'recognize-long-running', 'translate', 'batch-translate-text', 'detect-language', 'get-supported-languages', 'translate-text', 'video', 'detect-explicit-content', 'detect-labels', 'detect-object', 'detect-shot-changes', 'detect-text', 'transcribe-speech', 'vision', 'detect-document', 'detect-faces', 'detect-image-properties', 'detect-landmarks', 'detect-logos', 'detect-objects', 'detect-product', 'detect-safe-search', 'detect-text-pdf', 'detect-text-tiff', 'detect-web', 'product-search', 'product-sets', 'add-product', 'list-products', 'remove-product', 'delete-all', 'suggest-crop', 'ml-engine', 'monitoring', 'channel-descriptors', 'channels', 'dashboards', 'network-connectivity', 'hubs', 'spokes', 'network-security', 'authorization-policies', 'client-tls-policies', 'server-tls-policies', 'network-services', 'endpoint-policies', 'grpc-routes', 'http-filters', 'http-routes', 'observability-policies', 'tcp-routes', 'notebooks', 'is-upgradeable', 'policy-troubleshoot', 'get-ancestors', 'publicca', 'external-account-keys', 'lite-operations', 'lite-reservations', 'list-topics', 'lite-subscriptions', 'ack-up-to', 'seek', 'subscribe', 'lite-topics', 'list-subscriptions', 'publish', 'schemas', 'validate-message', 'validate-schema', 'subscriptions', 'ack', 'modify-ack-deadline', 'modify-message-ack-deadline', 'modify-push-config', 'pull', 'topics', 'detach-subscription', 'list-snapshots', 'recaptcha', 'migrate', 'recommender', 'insights', 'mark-accepted', 'mark-active', 'mark-dismissed', 'recommendations', 'mark-claimed', 'mark-failed', 'mark-succeeded', 'recommender-configs', 'redis', 'failover', 'get-auth-string', 'reschedule-maintenance', 'resource-config', 'bulk-export', 'list-resource-types', 'terraform', 'generate-import', 'resource-manager', 'folders', 'liens', 'org-policies', 'allow', 'deny', 'disable-enforce', 'enable-enforce', 'set-policy', 'bindings', 'values', 'resource-settings', 'list-values', 'set-value', 'unset-value', 'revisions', 'update-traffic', 'scc', 'assets', 'get-parent', 'get-project', 'group', 'list-marks', 'run-discovery', 'update-marks', 'findings', 'set-mute', 'notifications', 'describe-explicit', 'modules', 'sources', 'scheduler', 'app-engine', 'namespaces', 'resolve', 'api-keys', 'clone', 'get-key-string', 'peered-dns-domains', 'vpc-peerings', 'connect', 'disable-vpc-service-controls', 'enable-vpc-service-controls', 'source', 'project-configs', 'repos', 'update-metadata', 'ddl', 'execute-sql', 'sessions', 'rows', 'sql', 'patch', 'bak', 'csv', 'flags', 'promote-replica', 'reset-ssl-config', 'restore-backup', 'client-certs', 'server-ca-certs', 'rotate', 'ssl-certs', 'tiers', 'users', 'set-password', 'survey', 'tasks', 'acknowledge', 'cancel-lease', 'create-app-engine-task', 'create-http-task', 'create-pull-task', 'lease', 'queues', 'create-app-engine-queue', 'create-pull-queue', 'purge', 'update-app-engine-queue', 'update-pull-queue', 'renew-lease', 'trace', 'transcoder', 'templates', 'vmware', 'nodetypes', 'nsx', 'privateclouds', 'vcenter', 'web-security-scanner', 'scan-configs', 'scan-runs', 'list-crawled-urls', 'browse', 'test-ip', 'disable-debug', 'enable-debug', 'open-console', 'set-traffic', 'get-operation', 'list-vulnerabilities', 'scan', 'analyze-iam-policy', 'analyze-iam-policy-longrunning', 'analyze-move', 'search-all-iam-policies', 'search-all-resources', 'application-default', 'set-quota-project', 'beta', 'gen-config', 'migrate-config', 'cron-xml-to-yaml', 'datastore-indexes-xml-to-yaml', 'dispatch-xml-to-yaml', 'queue-xml-to-yaml', 'repair', 'export-iam-policy-analysis', 'get-screenshot', 'vpc-access', 'connectors', 'data-fusion', 'flex-template', 'build', 'drain', 'show', 'datastream', 'discover', 'fetch-static-ips', 'private-connections', 'streams', 'debug', 'logpoints', 'gen-repo-info-file', 'list-user-verified', 'error-reporting', 'events', 'report', 'eventarc', 'attributes', 'method-names', 'service-names', 'brokers', 'network-management', 'connectivity-tests', 'rerun', 'privateca', 'reusable-configs', 'roots', 'subordinates', 'get-csr', 'runtime-config', 'variables', 'watch', 'waiters', 'secrets', 'replication', 'access', 'workflows', 'executions', 'describe-last', 'wait-last', 'cheat-sheet', 'components', 'install', 'reinstall', 'set-service-account', 'postgresql', 'feedback', 'simulator', 'replay-recent-access', 'info', 'policy-intelligence', 'query-activity', 'pools', 'get-ca-certs', 'replicate', 'get-ancestors-iam-policy', 'topic', 'accessibility', 'arg-files', 'cli-trees', 'client-certificate', 'command-conventions', 'datetimes', 'escaping', 'filters', 'flags-file', 'formats', 'gcloudignore', 'offline-help', 'projections', 'resource-keys', 'startup', 'uninstall', 'workspace-add-ons', 'install-status', 'get-authorization', 'sha', 'sha256']
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
        output["entropy_password_err"] = "There is a possibility that a value might contains a secret string or password"

    elif output["issue"] == None:
        output["entropy_password_err"] = output["err"]
        output.pop("err")

    else:
        output["entropy_password_err"] = ""
    return output
