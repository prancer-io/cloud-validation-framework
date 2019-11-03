In a master test file, we are defining the test cases against the resource types rather than individual resources. it works in tandem with the master snapshot configuration file.

```
{
    "fileType": "mastertest",
    "notification": [<notifications>],
    "masterSnapshot": "<master-Snapshot-name>",
    "testSet": [
        {
            "masterTestName": "<master-Test-Name>",
            "version": "<version>",
            "cases": [
                {
                    "masterTestId": "<master-Test-Id>",
                    "rule":"<rule>"
                }
            ]
        }
    ]
}
```

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| notifications | the name of the notification file we want to use along with this test file |
| master-Snapshot-name | the name of the master snapshot configuration file we want to use along with this test file |
| master-Test-Name | the name of the master test name for this section |
| version | the version of the rule engine. current version is `0.1` |
| master-Test-Id | the id of the master test case |
| rule | the rule we want to examine |

Here is an example of that:
```
{
    "fileType": "mastertest",
    "notification": [],
    "masterSnapshot": "snapshot3",
    "testSet": [
        {
            "masterTestName": "test3",
            "version": "0.1",
            "cases": [
                {
                    "masterTestId": "1",
                    "rule":"exist({12}.location)"
                },
                {
                    "masterTestId": "2",
                    "rule":"{13}.location='eastus2'"
                },
                {
                    "masterTestId": "3",
                    "rule": "exist({14}.properties.addressSpace.addressPrefixes[])"
                },
                {
                    "masterTestId": "4",
                    "rule": "count({15}.properties.dhcpOptions.dnsServers[])=2"
                },
                {
                    "masterTestId": "5",
                    "rule": "{16}.properties.subnets['name'='abc-nprod-dev-eastus2-Subnet1'].properties.addressPrefix='192.23.26.0/24'"
                },
                {
                    "masterTestId": "6",
                    "rule": "{17}.tags.COST_LOCATION={18}.tags.COST_LOCATION"
                }
            ]
        }
    ]
}
```
