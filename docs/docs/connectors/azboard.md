# Azure Board structure file

The **Azure Board** connector allows you to inspect your **Azure Board** using their API. The connector is a wrapper around the **Azure Board** ReST API.

Here is a sample of the Azure Board structure file:

```json
    {
        "_id": {
            "$oid": "63844e7f34f186aa98b1c05e"
        },
        "checksum": "",
        "collection": "structures",
        "container": "azure_board_container",
        "name": "azureboard_connector",
        "timestamp": {
            "$numberLong": "1669615231678"
        },
        "type": "structure",
        "json": {
            "fileType": "structure",
            "type": "azureboard",
            "url": "https://dev.azure.com/wildkloud",
            "username": "<username>",
            "authtoken":"azureboard-accesstoken",
            "organisation": "prancer",
            "project": "<project-name>",
            "severity": "<severity>"
        }
    }
```
<!-- 
| Key           |Value Description |
| ------------- |:-------------:   |
|filetype |structure|
|type|kubernetes|
|company-name|your company name|
|cluster-name|your cluster name|
|cluster-url|use url like this `https://<IP>:6443` or you can use domain|
|namespace|use namespace which we need to connect for getting data|
|service-account-name|the service account name which has access to namespace|
|secret|the token of secret|

sample file:

```json
{
    "filetype": "structure",
    "type": "kubernetes",
    "companyName": "Company Name",
    "clusterName": "prancer-prod-prod-eastus2-aksprod01",
    "clusterUrl": "https://prancer-kube:6443",
    "namespaces": [
        {
            "namespace": "default",
            "serviceAccounts": [
                {
                    "name": "prancer_ro",
                    "secret":"<someToken>"
                }
            ]
        }
    ]
}
``` -->
