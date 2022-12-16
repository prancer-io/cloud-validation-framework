# Teams structure file

Integration of Prancer Web with **Teams** for notifications management based on Prancer CSPM or PAC findings.

The integration with **Teams** is as follows:

1. Each collection in the collection pages(**Infra/PAC** Management) can be integrated with **Teams**
2. Choose the dropdown option from the collection and select `Third Party Integration`.
3. Select the `Teams`

When the user clicks on the integration service, a new page/modal opens with pre-populated fields for the  ticket. User can edit as per convenience. On submit, The notifications shall be enabled for the specified collection.


Here is a sample of the **Teams** structure file:

```json
 {
    "fileType": "structure",
    "type": "teams",
    "webhook": "<webhook-url-from-Teams>"
}
```

| Key           |Value Description |
| ------------- |:-------------:   |
|webhook| Created webhook from teams to be pasted here|

sample file:

```json
 {
    "fileType": "structure",
    "type": "teams",
    "webhook": "https://prancerenterprise.webhook.office.com/webhookb2/***"
}
```

## Generate Webhook URL from teams

Once you have logged in to the **Teams** follow these steps to generate the AuthToken:

1. Go to the Teams
2. Select the `Teams` from the left-panel
3. Select the Channel that should receive the notifications
4. Click on the `More options`(i.e. 3 dots)
5. Select the `Connectors`
6. Select the `Incoming Webhook`, and click on `webhook URL`

By following the steps you'll be able to copy the Webhook URL. This url will be available to copy anytime you want, unless you have revoked the webhook URL.
