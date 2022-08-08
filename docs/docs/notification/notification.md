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
                ]
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