class MalformedArnError(Exception):
    def __init__(self, arn_str):
        self.arn_str = arn_str

    def __str__(self):
        return 'arn_str: {arn_str}'.format(arn_str=self.arn_str)


class Arn(object):
    def __init__(self, partition, service, region, account_id, resource_type, resource):
        self.partition = partition
        self.service = service
        self.region = region
        self.account_id = account_id
        self.resource_type = resource_type
        self.resource = resource


def arnparse(arn_str):
    if not arn_str.startswith('arn:'):
        raise MalformedArnError(arn_str)

    elements = arn_str.split(':', 5)
    service = elements[2]
    resource = elements[5]

    if service in ['s3', 'sns', 'apigateway', 'execute-api', 'acm', 'rds']:
        resource_type = None
    else:
        resource_type, resource = _parse_resource(resource)

    return Arn(
        partition=elements[1],
        service=service,
        region=elements[3] if elements[3] != '' else None,
        account_id=elements[4] if elements[4] != '' else None,
        resource_type=resource_type,
        resource=resource,
    )


def _parse_resource(resource):
    first_separator_index = -1
    for idx, c in enumerate(resource):
        if c in (':', '/'):
            first_separator_index = idx
            break

    if first_separator_index != -1:
        resource_type = resource[:first_separator_index]
        resource = resource[first_separator_index + 1:]
    else:
        resource_type = None

    return resource_type, resource