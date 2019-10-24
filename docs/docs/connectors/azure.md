The **Azure** connector allows you to inspect your **Azure** infrastructure using their api. The connector is a wrapper around the **Azure** ReST api.

# Azure principals

To use the **Azure** connector, you must create a service principal name (SPN) in the **Azure Active Directory** and configure its permissions properly. The SPN requires read policies on all services that you wish to inspect.

Here are steps to creating such a user if you don't have one yet:

1. Visit the [Azure Active Directory](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/Overview)
2. Visit the [App registrations](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredAppsPreview)
3. Register a new application, we suggest the name `prancer_ro` and  with the web url `http://localhost/` (the url doesn't really matter)
4. Click `Register`
5. New page should show the **Client id** and **Tenant id** in the block at the top of the page, note them down.
6. Go to `Certificates and secrets` section
7. Create a new secret
8. Note down the secret, it will disapear if you don't
9. Go to [Subscriptions](https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade), create a subscription if needed
10. Select your subscription
11. Note down the subscription ID, you will need it later
13. Visit **Access control (IAM)** in the **subscription** panel
14. Click on `Add`, then `Role assignment`
15. Select `Reader` for the **role** and select your application's name (We suggested `prancer_ro` before) in the **Application name**

# Azure api versions

**Prancer** requires a special configuration to support calling the **Azure** apis. Each **Azure** api needs a specific version that the software should support and instead of baking this into the application we went for a description file that everyone can contribute to.

To configure this, first copy the following code into a file. Then, go to the [Azure api configuration](../configuration/basics.md) section and update the configuration file with the name of this file:

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `azureApiVersions.json`

    {
        "Microsoft.Compute/availabilitySets": {
            "version": "2018-06-01"
        },
        "Microsoft.Network/virtualNetworks": {
            "version": "2018-07-01"
        },
        "Microsoft.Storage/storageAccounts": {
            "version": "2018-07-01"
        },
        "Microsoft.KeyVault/vaults": {
            "version": "2015-06-01"
        },
        "Microsoft.Network/networkSecurityGroups": {
            "version": "2018-11-01"
        },
        "fileType": "structure",
        "type": "others"
    }

# Connector configuration file

To configure the `Azure` connector, copy the following code to a file named `azureConnector.json` in your **Prancer** project folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `azureConnector.json`

    {
        "companyName": "Company Name",
        "tenant_id": "<tenant-id>",
        "type": "azure",
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

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| tenant-id | The tenant id of the application you create in the **Active Directory** |
| subscription-id | Your subscription id, you can find it in the [Subscriptions](https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade) |
| spn-client-id | Client id of the application you registered previously |
| spn-client-secret | Secret key associated with client id previously created |

# Company and tenant

You need an **Azure** tenant to work with **Prancer**. Each `azureConnector.json` can only feature 1 tenant but can feature many accounts and users.

You do not need to have a real account/department name for the accounts section, you can use your application's name or organization's name. The accounts section is strictly for organizing your configuration.

# Subscription and users

The subscriptions portion specify which subscription you want to inspect. You can configure as many subscriptions and users as you want per file. 

If you want to link multiple subscriptions together in your tests or want different users to be used to inspect your configuration, you must specify all of them here. Later, in snapshot configuration files, you will specify which user to use to inspect the infrastructure, but it must be defined here beforehand.