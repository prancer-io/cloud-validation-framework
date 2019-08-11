We have no way to read **CloudFormation** templates yet. But, don't worry, there are ways around this for the beta, we can use the **Git** connector to read the **JSON** version of that file as one big resource.

# Limitations of this workaround

This workaround has limitations but we are working on solutions to make it easier to work with **CloudFormation** templates:

1. We only support **JSON** templates, **YAML** based templates cannot be used
2. We read the whole template as one big resource even though it is a descriptor for multiple resources

# We only support JSON templates, YAML based templates cannot be used

Our engine doesn't have **YAML** to **JSON** support. What you could do is have a process that converts your **YAML** to a **JSON** file in the background when you are committing to your **Git** repository.

A quick but dirty example that works with **Python3** and `ruamel.yaml`:

    import ruamel.yaml
    import json

    in_file = 'input.yaml'
    out_file = 'output.json'

    yaml = ruamel.yaml.YAML(typ='safe')
    with open(in_file) as fpi:
        data = yaml.load(fpi)
        
    with open(out_file, 'w') as fpo:
        json.dump(data, fpo, indent=2)

But there are limitations to this example. You cannot use the `!Ref` or `!Sub` or any other functions unless you place them in double quotes. Also, changing the structure like this doesn't produce valid **CloudFormation** templates in **JSON** but it allows you to at least generate a **JSON** that you can read as one big snapshot and then work with it just like any other snapshot.

# We read the whole template as one big resource

This is counter-intuitive because **CloudFormation** templates are descriptors for resources and thus, each item in the file should be considered a different resource. But because we use the **Git** connector to read those files, the whole file is considered one big resource.

This means that most of your tests will be prefixed with pretty long rules like:

    {template}.resources.VPC.properties.xxx.yyy.zzz

The only workaround that you could do for now is to use a similar approach as above and split the **JSON** version of that file into multiple items using a tool like **jq**.

Taking the following **JSON** template into account:

    {
        "Parameters": {
            "KeyPair": {
                "Description": "Name of an existing EC2 KeyPair to enable SSH access to the instances. Linked to AWS Parameter",
                "Type": "AWS::EC2::KeyPair::KeyName",
                "ConstraintDescription": "must be the name of an existing EC2 KeyPair"
            }
        },
        "Resources": {
            "VPC": {
                "Type": "AWS::EC2::VPC",
                "Properties": {
                    "CidrBlock": "172.16.0.0/16",
                    "EnableDnsSupport": true,
                    "EnableDnsHostnames": true,
                    "InstanceTenancy": "default",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "!Sub \"${AWS::StackName}-vpc\""
                        }
                    ]
                }
            },
            "PublicSubnet": {
                "Type": "AWS::EC2::Subnet",
                "Properties": {
                    "AvailabilityZone": "ca-central-1a",
                    "VpcId": "!Ref VPC",
                    "CidrBlock": "172.16.1.0/24",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "!Sub \"${AWS::StackName}-public-subnet\""
                        }
                    ]
                }
            }
        }
    }

A quick and dirty example would be:

    cat "output.json" | jq '.Resources.VPC.Properties' > "output-vpc.json"
    cat "output.json" | jq '.Resources.VPC.PublicSubnet' > "output-subnet.json"

Then, you should just commit those files to **Git** and use them in your **Prancer** test suite just like a file that would normally exist.