We have no way to read **Azure ARM** templates yet. But, don't worry, there are ways around this for the beta, we can use the **Git** connector to read that file as one big resource.

# Limitations of this workaround

This workaround has limitations but we are working on solutions to make it easier to work with **Azure ARM** templates:

1. We read the whole template as one big resource even though it is a descriptor for multiple resources

# We read the whole template as one big resource

This is counter-intuitive because **Azure ARM** templates are descriptors for resources and thus, each item in the file should be considered a different resource. But because we use the **Git** connector to read those files, the whole file is considered one big resource.

This means that most of your tests will be prefixed with pretty long rules like:

    {template}.resources.VPC.properties.xxx.yyy.zzz

The only workaround that you could do for now is to use a similar approach as above and split the **JSON** version of that file into multiple items using a tool like **jq**.

Taking the following **JSON** template into account:

    {
        "resources": [
            {
                "name": "My network name",
                "type": "Microsoft.Network/virtualNetworks",
                "location": "eastus",
                "properties": {
                    "addressSpace": {
                        "addressPrefixes": [
                            "172.1.16.0/24"
                        ]
                    },
                    "subnets": [
                        {
                            "name": "A subnet",
                            "properties": {
                                "addressPrefix": "172.1.16.0/24"
                            }
                        }
                    ]
                }
            },{
                "type": "Microsoft.Network/publicIPAddresses",
                "name": "My public ip",
                "location": "eastus",
                "properties": {
                    "publicIPAllocationMethod": "Dynamic",
                    "dnsSettings": {
                        "domainNameLabel": "DNSPrefix"
                    }
                }
            }
        ]
    }

A quick and dirty example would be:

    cat input.json | jq '.resources[] | select(.name == "My network name") | .properties' > "template-network.json"
    cat input.json | jq '.resources[] | select(.name == "My public ip") | .properties' > "template-publicip.json"

Then, you should just commit those files to **Git** and use them in your **Prancer** test suite just like a file that would normally exist.