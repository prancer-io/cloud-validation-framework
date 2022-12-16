# Slack structure file

Integration of Prancer Web with **Slack** for notifications management based on Prancer CSPM or PAC findings.

The integration with **Slack** is as follows:

1. Each collection in the collection pages(**Infra/PAC** Management) can be integrated with **Slack**
2. Choose the dropdown option from the collection and select `Third Party Integration`.
3. Select the `Slack`

When the user clicks on the integration service, a new page/modal opens with pre-populated fields for the  ticket. User can edit as per convenience. On submit, The notifications shall be enabled for the specified collection.


Here is a sample of the **Slack** structure file:

```json
 {
    "fileType": "structure",
    "type": "slack",
    "webhook": "<webhook-url-from-slack>"
}
```

| Key           |Value Description |
| ------------- |:-------------:   |
|webhook| Created webhook from slack to be pasted here|

sample file:

```json
 {
    "fileType": "structure",
    "type": "slack",
    "webhook": "https://hooks.slack.com/services/***"
}
```

## Generate Webhook URL from slack

Once you have logged in to the **Slack** follow these steps to generate the AuthToken:

1. Go to the Home page
2. Drop down using option shown beside `<project-name>`, select `Settings & administration`, and select the `manage apps`
3. Click on `Build` from the top-right corner.
4. Select `Create New App` if not created.(In order to generate webhook URL you have to have an app created)
5. Click on the app that you have created
6. Select the `Incoming Webhooks`, which is underneath the `Features`
7. Click on the `Add New Webhook to Workspace` if not generated already.
8. Select the Channel that should receive the notifications

By following the steps you'll be able to copy the Webhook URL. This url will be available to copy anytime you want, unless you have revoked the webhook URL.
