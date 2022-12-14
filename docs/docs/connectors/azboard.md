# Azure Board integration

Integration of Prancer Web with **Azure Board** will help you with ticket management, and file/spectate tickets based on Prancer CSPM or PAC findings.

The integration with **Azure Board** is as follows:

1. Each collection in the collection pages(**Infra/PAC** Management) can be integrated with **Azure Board**
2. Choose the dropdown option from the collection and select `Third Party Integration`.
3. Select the `Azure Board`

When the user clicks on the integration service, a new page/modal opens with pre-populated fields for the workitem. User can edit as per convenience. On submit, the workitem shall be created with the ticket platform **Azure Board**.

In Reporting pages : Infra Findings and Application Findings, a new option to create **Azure Board** ticket has to be created when opening a single item.

This will create an integration with **Azure Board** ticketing system (workitem to be created automatically with the proper description for the collection).

Here is a sample of the Azure Board structure file:

```json
{
    "fileType": "structure",
    "type": "azureboard",
    "url": "<azureboard-endpoint-url>",
    "username": "<azureboard-user-email>",
    "authtoken":"azureboard-accesstoken",
    "organisation": "prancer",
    "project": "<project-name>",
    "severity": "<severity>"
}
```

| Key           |Value Description |
| ------------- |:-------------:   |
|url| URL to the azure board|
|username|your user-email of azure cloud|
|authtoken|AuthToken of the azure board|
|project|Name of your project.|
|severity|Type of severity you want to assign to this particular task.(Options: High, Medium, Low)|

sample file:

```json
{
    "fileType": "structure",
    "type": "azureboard",
    "url": "https://dev.azure.com/wildkloud",
    "username": "prancer-user@prancer.io",
    "authtoken": "prancer-io-customer-accesstoken-azureboard",
    "organisation": "prancer",
    "project": "NextGen Cloud",
    "severity": "high"
}
```

## Generate AuthToken from Azure Board

Once you have logged in to the Azure follow these steps to generate the AuthToken:

1. Go to the Home Page
2. Select the `<project-name>`
3. Click the `User Settings` and select the `Personal access token`
4. Create a new token by clicking `New Token`
5. Provide `Name` and under `Work Items` give the `Read & Write` access.
6. Click on the `Create`.

By following the steps you'll be able to copy the token. Make sure the token is saved and secured somewhere safe, as you won't be able to see that again.
