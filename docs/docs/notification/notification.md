**Notification**
===

- The notification configuration file contains the details about sending the Notification to the user with the test result.

```
{
    "container": "<container-name>"
    "name": "<notification-name>",
    "json": {
        "fileType": "notifications"
        "type": "notifications",
        "notifications": [
            {
                "notificationId": "<notification-id>",
                "type": "email",
                "level": "all",
                "user": "<sender-email>",
                "to": [
                    "<receiver1-email>",
                    "<receiver2-email>"
                ],
                "smtp":{
                    "server":"smtp.gmail.com",
                    "port":587,
                    "tls":true
                }
            }
        ]
    }
}
```

- **Explanation:**
  - **container-name:** Name of the collection for which you want notifications.
  - **notification-name:** Any notification name for reference.
  - **notification-id:** Notification id to uniquely identify the notification.
  - **level:** level of output results to include in Notification. It could be "passed," "failed," or "all."
  - **user:** Add sender email from which you want to send an email.
  - **to:** Add a list of receiver emails to which you want to send the email notification.

- **Upload Notification File**
  - User can upload a new Notification Configuration file from infra management screen to the particular collection.
  - User can upload multiple `notification` JSON files followed by drag and drop on the particular container or by clicking the `Click here` button on collection, which will upload the notification files.