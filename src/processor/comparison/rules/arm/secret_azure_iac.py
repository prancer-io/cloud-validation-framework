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


def azure_password_leak(generated_snapshot: dict) -> dict:

    PASSWORD_KEY_RE = r".*(?i)(password|securevalue|secret|privatekey|primarykey|secondarykey).*"
    PASSWORD_VALUE_RE = r'^(?!.*\$\{.*\}.*)(?=(?=.*[a-z][A-Z])|(?=.*[A-Z][a-z])|(?=.*[a-z][0-9])|(?=.*[0-9][a-z])|(?=.*[0-9][A-Z])|(?=.*[A-Z][0-9]))(.*[\^$*.\[\]{}\(\)?\-"!@\#%&\/,><\’:;|_~`]?)\S{8,99}$'
    EXCLUDE_REGEX = r'(?=.*([\[{(<]){1,})((\(.*\)){0,})((\[.*\]){0,})((\{.*\}){0,})((\<.*\>){0,})'

    output = secret_finder(
        generated_snapshot, PASSWORD_VALUE_RE, PASSWORD_KEY_RE, EXCLUDE_RE=EXCLUDE_REGEX)

    if output["issue"] == True:
        output["azure_password_leak"] = "There is a possibility that secure password is exposed"

    elif output["issue"] == None:
        output["azure_password_leak"] = output["err"]
        output.pop("err")

    elif output["issue"] == False:
        output["azure_password_leak"] = ""
    return output


def entropy_password(generated_snapshot: dict) -> dict:

    PASSWORD_VALUE_RE = r'^(?!.*\$\{.*\}.*)(?=(?=.*[a-z][A-Z])|(?=.*[A-Z][a-z])|(?=.*[a-z][0-9])|(?=.*[0-9][a-z])|(?=.*[0-9][A-Z])|(?=.*[A-Z][0-9]))(?=.*[^A-Za-z0-9])\S{8,99}$'
    EXCLUDE_CONTAINS = ['API', 'AAD', 'Add', 'Advisor', 'AKS', 'Analysis', 'Analytics', 'Analyzer', 'API', 'App', 'Authorization', 'Automation', 'Azure', 'Batch', 'BI', 'Billing', 'Blockchain', 'Blueprints', 'Bot', 'Bus', 'Cache', 'CDN', 'Central', 'Certificate', 'Change', 'Cloud', 'Cognitive', 'Communication', 'Compute', 'Configuration', 'Consumption', 'Container', 'Cosmos', 'Custom', 'Customer', 'Data', 'Databricks', 'DB', 'Dedicated', 'Deployment', 'Device', 'DevOps', 'DevTest', 'Digital', 'DNS', 'Domain', 'Door', 'Event', 'Fabric', 'Factory', 'FarmBeats', 'for', 'Front', 'Graph', 'Grid', 'Hat', 'HDInsight', 'HSMs/', 'Hub', 'Hubs', 'Identity', 'Insights', 'Instance', 'IoT', 'Key', 'Kusto',
                        'Labs', 'Lake', 'Learning', 'Logic', 'Machine', 'Maintenance', 'Managed', 'Management', 'Manager', 'Maps', 'MariaDB', 'Media', 'Migrate', 'Migration', 'MySQL', 'NetApp', 'Network', 'Notification', 'Ons', 'OpenShift', 'Operational', 'Operations', 'Peering', 'Policy', 'Portal', 'PostgreSQL', 'Power', 'Providers', 'Provisioning', 'Recovery', 'Red', 'Registration', 'Registry', 'Relay', 'Resource', 'Resources', 'Scheduler', 'Search', 'Security', 'Series', 'Service', 'Services', 'Share', 'SignalR', 'Spring', 'SQL', 'Stack', 'Storage', 'Store', 'StorSimple', 'Stream', 'Subscription', 'Synapse', 'Sync', 'Time', 'Traffic', 'Twins', 'Update', 'Vault', 'Vaults', 'versions', 'Video', 'Virtual', 'Web', 'sha', 'sha256']
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
