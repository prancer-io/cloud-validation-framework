# Tutorial - Connect your Prancer project to an AWS account

This section will show you how to create the configuration file used to connect `Prancer` to your `AWS` account using the usual access keys and secrets that the `AWS CLI` would use.

## Assumptions

This tutorial assumes a few things:

1. You have an [AWS](https://aws.amazon.com/) account
2. Your `AWS console user` has enough rights to create `EC2` resources and can create `IAM` users

## Creating the Read-Only Prancer user

> If you already have an `IAM` user configured and have access to it's access key and secret, skip to the next section.

To run `Prancer` against `AWS`, you will need a user with certain privileges and the **`Access key`** and **`Secret`** of that user. Those information are given when you create the user in the `IAM` console.

To create such a user, just follow the steps below:

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
12. Note down the `Access key ID`
13. Note down the `Secret access key`
14. Click `Close`

> Note that the policies added here are only for EC2 resources. If you needed `Prancer` to check other kinds of resources, you would need to add the appropriate `ReadOnlyAccess` policy.

## Configure the connector

In your `Prancer` project folder, create a configuration file named `awsStructure.json` and copy the following content in it:

    {
        "organization": "prancer-test",
        "fileType": "structure",
        "organization-unit": [
            {
                "name": "prancer-test",
                "accounts": [
                    {
                        "account-name": "prancer-test",
                        "account-description": "prancer-test",
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

Next, replace all values in this file that looks like a tag such as:

| tag | What to put there |
|-----|-------------------|
| account-id | Your AWS account id, find this in the `AWS console` account menu drop-down |
| iam-user | Name of the `IAM` user, we previously suggested `prancer_ro` |
| iam-access-key | The `access key` that you took note of in the previous section |
| secret-access-key | The `secret` associated to the access key that you took note of in the previous section |

## Conclusion

That's it, you are done.

You can now go back to the previous tutorial that brought you here to continue looking at the tutorials on [Prancer's Guidance section](http://www.prancer.io/guidance/)