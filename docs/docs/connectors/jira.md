# Jira structure file

Integration of Prancer Web with **Jira** for story management and file/view tickets based on Prancer CSPM or PAC findings.

The integration with **Jira** is as follows:

1. Each collection in the collection pages(**Infra/PAC** Management) can be integrated with **Jira**
2. Choose the dropdown option from the collection and select `Third Party Integration`.
3. Select the `Jira`

When the user clicks on the integration service, a new page/modal opens with pre-populated fields for the  ticket. User can edit as per convenience. On submit, the ticket shall be created with the ticket platform **Jira**.

In Reporting pages : Infra Findings and Application Findings, a new option to create **Jira** ticket has to be created when opening a single item.

This will create an integration with **Jira** ticketing system (ticket to be created automatically with the proper description for the collection).
Here is a sample of the **Jira** structure file:

```json
{
    "fileType": "structure",
    "type": "jira",
    "url": "<Jira-endpoint-URL>",
    "username": "<jira-user-email>",
    "authtoken": "accesstoken-jira",
    "organisation": "Prancer",
    "project": "<project-name>",
    "severity": "<severity>"
}
```

| Key           |Value Description |
| ------------- |:-------------:   |
|url| URL to the Jira board|
|username|your user-email of jira|
|authtoken|AuthToken of the jira|
|project|Name of your project.|
|severity|Type of severity you want to assign to this particular task.(Options: High, Medium, Low)|

sample file:

```json
{
    "fileType": "structure",
    "type": "jira",
    "url": "https://testjiraprancer.atlassian.net",
    "username": "prancer-user@prancer.io",
    "authtoken": "prancer-user-prancer-io-customer120-accesstoken-jira",
    "organisation": "Prancer",
    "project": "SAM",
    "severity": "High"
}
```

## Generate AuthToken from Jira

Once you have logged in to the Jira follow these steps to generate the AuthToken:

1. Go to the Home page
2. Click on `Settings`, and select the `Atlassian account settings`
3. Click on the `Security`
4. Underneath `API token` click on the `create and manage API tokens`
5. Click on `Create API token`, and add label

By following the steps you'll be able to copy the token. Make sure the token is saved and secured somewhere safe, as you won't be able to see that again.
