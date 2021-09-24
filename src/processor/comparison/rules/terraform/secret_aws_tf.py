import json
import re
import collections
import traceback
import math


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
    entropy_list = []
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
                        if isinstance(nested_resource, str) and re.match(PASSWORD_VALUE_RE, nested_resource) and (re.match(PASSWORD_KEY_RE, str(key), re.I) if PASSWORD_KEY_RE else True) and (not(re.match(EXCLUDE_RE, str(nested_resource))) if EXCLUDE_RE else True):
                            if shannon_entropy_password:
                                _, normalized_entropy = shannon_entropy(
                                    nested_resource)
                                if normalized_entropy > 0.965:
                                    entropy_list.append({
                                        "path": "resources/"+resource.get("type")+"/" + "/".join([str(path) for path in path]),
                                        "value": nested_resource
                                    })
                                    issue_found = True
                                    print("\n\n")
                                    print("Resource Type:",
                                          resource.get("type"))
                                    print("Path to leaked password:", path)
                                    print("leaked password:", nested_resource)
                                    print("\n")
                                else:
                                    print(normalized_entropy, nested_resource)
                            else:
                                issue_found = True
                                print("\n\n")
                                print("Resource Type:", resource.get("type"))
                                print("Path to leaked password:", path)
                                print("leaked password:", nested_resource)
                                print("\n")

        output["issue"] = True if issue_found else False

        if entropy_list:
            output["entropy_password"] = entropy_list
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
    EXCLUDE_CONTAINS = ['aad', 'access', 'acl', 'acm', 'amazon', 'ami', 'ami-', 'analytics', 'and', 'application', 'appspec', 'arn', 'aurora', 'authority', 'autonomous', 'aws', 'billing', 'block', 'border', 'bucket', 'cdn', 'certificate', 'cli', 'cloud', 'cloudhub', 'cmk', 'cofig', 'command', 'compute', 'conditional', 'config', 'console', 'container', 'control', 'dashboard', 'default', 'description', 'device', 'directory', 'dns', 'ebs', 'ec2', 'ecr', 'ecs', 'ecu', 'efs', 'eib', 'elastic', 'email', 'emr', 'endpoint', 'envelope', 'ephemeral', 'etl', 'example', 'exbibyte', 'farm', 'fbl', 'federated', 'federation', 'feedback', 'file', 'fim', 'firehose', 'format', 'forums', 'function', 'gateway', 'gib', 'gibibyte', 'group', 'hub', 'iam', 'identifiers', 'identity', 'idp', 'image', 'interface', 'isp', 'key', 'kib', 'kibibyte', 'kms', 'language',
                        'line', 'list', 'logloop', 'mail', 'management', 'manager', 'marker', 'mebibyte', 'member', 'mfa', 'mib', 'mime', 'mobile', 'mta', 'name', 'notification', 'number', 'object', 'origin', 'parameter', 'path', 'pca', 'pebibyte', 'period', 'pib', 'policy', 'prefix', 'private', 'properties', 'protocol', 'rds', 'recipe', 'registry', 'representational', 'resource', 'resources', 'return', 'role', 's3', 'scp', 'security', 'service', 'services', 'ses', 'sign-on', 'simple', 'sims', 'simulator', 'single', 'sns', 'sqs', 'sse', 'sso', 'state', 'storage', 'store', 'streams', 'sts', 'sts:', 'subnet', 'swf', 'system', 'tag', 'tebibyte', 'tib', 'tls', 'token', 'transfer', 'unit', 'user', 'validation', 'variable', 'version', 'vgw', 'virtual', 'virtualization', 'vpc', 'vpn', 'wam', 'web', 'workflow', 'workspaces', 'yib', 'yobibyte', 'zebibyte', 'zib']
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
        output["entropy_password_err"] = "There is a possibility that secure password is exposed"

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


if __name__ == '__main__':

    generated_snapshot_path = "snapshot_tf.json"
    with open(generated_snapshot_path, "r") as snapshot:
        generated_snapshot = json.load(snapshot)

    output = aws_password_leak(generated_snapshot)
    print("\n\n", output)
    output = gl_aws_secrets(generated_snapshot)
    print("\n\n", output)
    output = gl_aws_account(generated_snapshot)
    print("\n\n", output)
    output = al_access_key_id(generated_snapshot)
    print("\n\n", output)
    output = al_mws(generated_snapshot)
    print("\n\n", output)
    output = entropy_password(generated_snapshot)
    # print("\n\n", output["issue"])
    print("\n\n", output)
    for password in output.get("entropy_password", []):
        print(password)
