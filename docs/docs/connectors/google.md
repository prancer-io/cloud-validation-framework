The **Google** connector allows you to inspect your **Google Cloud** infrastructure using their api. The connector is a wrapper around the **Google** ReST api.

# Google Cloud Platform Service Account

A service account is a special kind of account used by an application or a virtual machine (VM) instance, not a person. Applications use service accounts to make authorized API calls. To learn more about the Service Account, you can [review Google Cloud Platform documentation](https://cloud.google.com/iam/docs/service-accounts)

To grant access to prancer cloud validation framework to browse your Google Cloud Platform, you need to create a Service Account. It is highly recommended to follow [official google cloud platform documentation](https://cloud.google.com/iam/docs/creating-managing-service-accounts)

Here are the recommended steps to creating such a user if you don't have one yet:

1. Open the Service Accounts page in the Cloud Console.[click here to access](https://console.cloud.google.com/iam-admin/serviceaccounts)

2. Open the Service Accounts page

3. Click Select a project, choose your project, and click Open.

4. Click Create Service Account.

5. Enter a service account name (friendly display name), an optional description, select a role you wish to grant to the service account, and then click Save.

6. create a new key by selecting `create key`. Select the json as the type of key and it will be downloaded to your local disk. All the information you need is in that json file.

# Google Cloud Platform API methods

To configure the `Google Cloud Platform` connector, we need the a file detailing out all the available methods. We put those information in a separate file called `googleParams.json`. For more information, you can check [Google API client library](https://github.com/googleapis/google-api-python-client)

# Connector configuration file

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `googleConnector.json`

    {
        "organization": "company1",
        "type": "google",
        "fileType": "structure",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "projects": [
            {
                "project-name": "<project-name>",
                "project-id": "<project-id>",
                "users": [
                    {
                        "name": "<service-account-name>",
                        "type": "service_account",
                        "private_key_id": "<private-key-id>",
                        "private_key": "<private-key>",
                        "private_key_path":"<private_key_path>",
                        "client_email": "<client-email>",
                        "client_id": "<client-id>",
                        "client_x509_cert_url": "<client_x509_cert_url>",
                    }
                ]
            }
        ]
    }

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| project-name | The name of the project in the Google Cloud |
| project-id | project id in the google cloud|
| service-account-name | service account name |
| private_key_id | private key id |
| private_key | Embed the private key in the connector file|
| private_key_path | put the path of the private key in the connector file|
| client_email | client email |
| client_id | client id |
| client_x509_cert_url | client x509 cert url, you get this info from the key json output |


> It is not recommended to put any secret in the `connector` file. This is good just for testing purposes

> You should use either `private_key` or `private_key_path`

# Projects and Service Accounts

The **Google Cloud Platform** `connector` supports multiple projects and multiple service accounts for each project.

# Private Key

There are three options available to store the private key for the service account:
 - In connector file as a key
 - In connector file as a path
 - In a vault

 Keeping the private key in the `connector` file is good only for testing purposes. 

 You can keep the path to the private key in your connector file.

Keeping the private key in the vault is the most secure and recommended way of keeping the secret in prancer framework. To learn more visit [secrets section](../configuration/secrets.md)

<iframe width="560" height="315" src="https://www.youtube.com/embed/eRE-TZ74xt0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>