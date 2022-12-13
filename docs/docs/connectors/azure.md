The **Azure** connector allows you to inspect your **Azure** infrastructure using their API. The connector is a wrapper around the **Azure** ReST API.

# Azure Service Principals

To use the **Azure** connector, you must create a service principal name (SPN) in the **Azure Active Directory** and configure its permissions properly. The SPN requires read permission on all services that you wish to inspect.

It is recommended that you follow official Microsoft documentation to understand more about the [service principal objects][service-principal-objects]

Here are the recommended steps to creating such a user if you don't have one yet:

1. Visit the [Azure Active Directory][Azure-Active-Directory]
2. Visit the [App registrations][App-registrations]
3. Register a new application, we suggest the name `prancer_ro`, choose a single tenant app and with the redirect url `http://localhost/` (the url doesn't really matter)
4. Click `Register`
5. New page should show the **Application (client) ID** and **Directory (tenant) ID** in the block at the top of the page, note them down.
6. Go to `Certificates and secrets` section
7. Create a new client secret
8. Note down the secret, it will disappear if you don't
9. Go to [Subscriptions][subscriptions], create a subscription if needed
10. Select your subscription
11. Note down the subscription ID, you will need it later
12. Visit **Access control (IAM)** in the **subscription** panel
13. Select `Role assignments` tab, Click on `Add`, then `Add role assignment`
14. Select `Reader` for the **Role** and select your application's name (We suggested `prancer_ro` earlier) in the Application name **Select** section and click save.

> <NoteTitle>Notes: Multiple SPNs</NoteTitle>
>
> Prancer cloud validation framework supports multiple SPNs to connect to the Azure. By doing that, you can have different permissions set for each SPN to run various validation scenarios!

# Azure api versions

**Prancer** requires a special configuration to support calling the **Azure** apis. To understand more, go to the [Azure api configuration](../configuration/basics.md) section.
# Connector configuration file

To configure the `Azure` connector, copy the following code to a file named `azureConnector.json` in your **Prancer** project folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want, but we suggest `azureConnector.json`

```json
    {
        "filetype":"structure",
        "type":"azure",
        "companyName": "Company Name",
        "tenant_id": "<tenant-id>",
        "accounts": [
            {
                "department": "Unit/Department name",
                "subscription": [
                    {
                        "subscription_name": "Subscription (Account) name",
                        "subscription_description": "Subscription (Account) description",
                        "subscription_id": "<subscription-id>",
                        "users": [
                            {
                                "name":"<spn-username>",
                                "client_id": "<spn-client-id>",
                                "client_secret": "<spn-client-secret>"
                            }
                        ]
                    }
                ]
            }
        ]
    }
```

Remember to substitute all values in this file that looks like a `<tag>` such as:

| Tag | What to put there |
|-----|-------------------|
| tenant-id | The tenant id of the application you create in the **Active Directory** |
| subscription-id | Your subscription id, you can find it in the [Subscriptions][subscriptions]|
| spn-client-id | Client id of the application you registered previously |
| spn-client-secret | Secret key associated with client id previously created |

> It is not recommended to put the secret key in the `connector` file. This is only good for testing purposes.

# Company and tenant

You need an **Azure** tenant to work with **Prancer**. Each `azureConnector.json` can only feature one tenant and many subscriptions and users.

You do not need to have an actual account/department name for the accounts section, you can use your application's name or organization's name. The accounts section is strictly for organizing your configuration and Microsoft Enterprise customers.

# Subscription and users

The subscriptions portion specify which subscription you want to inspect. You can configure as many subscriptions and users as you wish per file.

If you want to link multiple subscriptions together in your tests or want different users to be used to inspect your configuration, you must specify all of them here. Later, in snapshot configuration files, you will determine which user to use to inspect the infrastructure, but it must be defined beforehand.

# Client Secret

There are three options available to store the client secret for an SPN account:

- In the connector file
- In the Environment variable
- In a vault

 Keeping the client secret in the `connector` file is suitable only for testing purposes.

 You can keep the client secret as an environment variable. The environment variable's name will be the name of the SPN account. For example, if the name of the SPN account is `prancer_spn` and the secret is `a1b2c3` :

```bash
    export prancer_spn=a1b2c3
```

Keeping the client secret in the vault is the most secure and recommended way of keeping the secret in the prancer framework. To learn more, visit [secrets section][secrets-section]

<!-- All Links from this page -->

[service-principal-objects]: https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals
[subscriptions]:             https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade
[secrets-section]:           ../configuration/secrets.md
[Azure-Active-Directory]:    https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/Overview
[App-registrations]:         https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps

Keeping the client secret in the vault is the most secure and recommended way of keeping the secret in prancer framework. To learn more visit [secrets section](../configuration/secrets.md)

<iframe width="560" height="315" src="https://www.youtube.com/embed/T1Y9k-B6muw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>