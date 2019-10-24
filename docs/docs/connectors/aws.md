The **AWS** (Amazon Web Services) connector allows you to inspect your **AWS** infrastructure using their api. The connector is a wrapper around the **AWS** ReST api and command line tool. It leverages inspection of the infrastructure using the `describe-xyz` operations available for each service provider.

# IAM user configuration

To connect using the **AWS** connector, you must create a user in **IAM** and configure its policies properly. The **IAM** user requires read policies on all services that you wish to inspect. For example, to inspect the **EC2** infrastructure, give the `AmazonEC2ReadOnlyAccess` policy.

Here are steps to creating such a user if you don't have one yet:

1. Visit the [IAM console](https://console.aws.amazon.com/iam/home)
2. Click on the `Users` section on the left menu
3. Click on `Add user`
4. Name the user anything you want, we suggest `prancer_ro`
5. Only enable `Programmatic access`
6. Click `Next: Permissions`
7. Click `Attach existing policies directly`
8. Search for the `AmazonEC2ReadOnlyAccess` policy and check it
9. Click `Next: Tags`
10. Click `Next: Review`
11. Click `Create user`
12. **Take note** of the `Access key ID`
13. **Take note** of the `Secret access key`
14. Click `Close`

# Connector configuration file

To configure the **AWS** connector, copy the following code to a file named `awsConnector.json` in your **Prancer** project folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want but we suggest `awsConnector.json`

    {
        "organization": "Organization name",
        "fileType": "structure",
        "type": "aws",
        "organization-unit": [
            {
                "name": "Unit/Department name",
                "accounts": [
                    {
                        "account-name": "Account name",
                        "account-description": "Description of account",
                        "account-id": "<account-id>",
                        "users": [
                            {
                                "name": "<iam-user>",
                                "access-key": "<iam-access-key>",
                                "secret-access": "<secret-access-key>",
                                "region":"<region>",
                                "client": "EC2"
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
| account-id | Your **AWS** account id, find this in the **AWS console** account menu drop-down |
| iam-user | Name of the **IAM** user, we suggest `prancer_ro` |
| iam-access-key | The programmatic **access key** associated to that user |
| secret-access-key | The programmatic **secret** associated to the access key |

If you do not have access to an **access key** or to the **secret** you will have to create a new access key and decommission the old one.

# Organization

You do not need an **AWS** organization to use the **AWS** connector but you must fill in the data as presented.

If you do not have an **AWS** organization, just enter values that would correspond if you had one. The organizational units section is strictly for organizing your configuration.

You can define as many organizations as you want in a connector file.

# Accounts and users

The accounts portion specify which account you want to inspect. You can configure as many accounts and users as you want per file. 

If you want to link multiple accounts together in your tests or want different users to be used to inspect your configuration, you must specify all of them here. Later, in snapshot configuration files, you will specify which user to use to inspect the infrastructure, but it must be defined here beforehand.