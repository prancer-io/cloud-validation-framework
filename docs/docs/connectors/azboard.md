# Azure Board structure file

The **Azure Board** connector allows you to inspect your **Azure Board** using their API. The connector is a wrapper around the **Azure Board** ReST API.

Here is a sample of the Azure Board structure file:

```json
    {
        {
            "fileType": "structure",
            "type": "azureboard",
            "url": "<azureboard-endpoint-url>",
            "username": "<username>",
            "authtoken":"azureboard-accesstoken",
            "organisation": "prancer",
            "project": "<project-name>",
            "severity": "<severity>"
        }
    }
```

| Key           |Value Description |
| ------------- |:-------------:   |
|url| URL to the azure board|
|username|your username of azure cloud|
|authtoken|AuthToken of the azure board|
|project|Name of your project.|
|severity|Type of severity you want to assign to this particular task.(Options: High, Medium, Low)|

sample file:

```json
{
    "fileType": "structure",
    "type": "azureboard",
    "url": "https://dev.azure.com/wildkloud",
    "username": "ishan.pansuriya@prancer.io",
    "authtoken": "ishan-pansuriya-prancer-io-customer-accesstoken-azureboard",
    "organisation": "prancer",
    "project": "NextGen Cloud",
    "severity": "high"
}
```
