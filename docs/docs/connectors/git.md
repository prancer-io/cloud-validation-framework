The **Filesystem** connector allows you to connect to files from a local file system or a git repository. This is the main connector we use for **Infrastructure as Code** (IaC) security validation. The **Filesystem** connector will help to inspect a static file committed into your project. Therefore, you should use this connector to preemptively validate your cloud management templates before applying your infrastructure changes.

# SSH user configuration

To use SSH as a checkout source, you will need a repository on a hosted solution that is reachable by **Prancer** and that supports SSH based checkouts. A common example would be to use **GitHub**, **GitLab**, **BitBucket** or **CodeCommit**. Depending on the private or public nature of your repository:

- You only need the url and branch name if the repository is public
- You need to provide the path to the SSH key file if the repository is private
- You need to provide a username if you want to use **Prancer** to create branches or tags

# HTTPS user configuration

To use HTTPS as a checkout source, you will need a repository on a hosted solution that is reachable by **Prancer** and that supports HTTPS based checkouts. A common example would be to use **GitHub**, **GitLab**, **BitBucket** or **CodeCommit**. Depending on the private or public nature of your repository:

- You only need the url and branch name if the repository is public
- You need to provide the username and password if the repository is private

# Connector configuration file

To configure the **Filesystem** connector, copy the following code to a file named `fsConnector.json` in your **Prancer** project folder.

> <NoteTitle>Notes: Naming conventions</NoteTitle>
>
> This file can be named anything you want, but we suggest `fsConnector.json` to clearly distinguish this from other connectors

**local filesystem example**

```
    {
        "fileType": "structure",
        "type": "filesystem",
        "companyName": "Organization name",
        "folderPath": "<path-to-folder>"
    }
```
Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| path-to-folder | Absolute path to the folder  |

* **Note**: Path expansions are not implemented yet, you need to provide full paths!


**Public HTTPS or SSH example**

    {
        "fileType": "structure",
        "type": "filesystem",
        "companyName": "Organization name",
        "gitProvider": "<url-to-repository>",
        "branchName": "<branch>",
        "private": false
    }

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| url-to-repository | Enter the HTTPS or SSH url to the repository |
| branch | Branch to checkout |
| private | Boolean value stating if the repository is private or public |

* **Note**: Path expansions are not implemented yet, you need to provide full paths!


**Private SSH example**

    {
        "fileType": "structure",
        "type": "filesystem",
        "companyName": "Organization name",
        "gitProvider": "<url-to-repository>",
        "branchName": "<branch>",
        "sshKeyfile": "<path-to-private-ssh-key-file>",
        "sshUser": "<username-of-repo>",
        "sshHost": "<hostname-of-repo>",
        "private": true
    }

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| url-to-repository | Enter the HTTPS or SSH url to the repository |
| branch | Branch to checkout |
| username-of-repo | Username used to execute operations on repository such as commits, merges, tags, etc |
| hostname-of-repo | Host entry to put in temporary config file, this should be the same as what is in `url-to-repository` |
| path-to-private-ssh-key-file | Path to the private key file when using a private SSH repository. this should be an absolute path. do not use `~` for home directory |
| private | Boolean value stating if the repository is private or public |

* **Note**: Path expansions are not implemented yet, you need to provide full paths!

**Private HTTPS example**

    {
        "fileType": "structure",
        "type": "filesystem",
        "companyName": "Organization name",
        "gitProvider": "<url-to-repository>",
        "branchName": "<branch>",
        "httpsUser": "<username>",
        "httpsPassword": "<password>",
        "private": true
    }

Remember to substitute all values in this file that looks like a `<tag>` such as:

| tag | What to put there |
|-----|-------------------|
| url-to-repository | Enter the HTTPS or SSH url to the repository |
| branch | Branch to checkout |
| username | Username used to connect to the repository when using a private HTTPS repository |
| password | Password used to connect to the repository when using a private HTTPS repository |
| private | Boolean value stating if the repository is private or public |


> <NoteTitle>Notes</NoteTitle>
> Putting the `httpsPassword` in the connector file is only good for testing purposes. We recommend moving the `httpsPassword` out of the connector file in production scenario. 

To move the `httpsPassword` out of the connector file, you have two options:
 - set the environment variable to store the password
 - using vault [vault configuration](../configuration/secrets.md)

To set an environment variable, you should export the `username` and assign the `password` value. For example, if your username is `prancer-git` and your password is `password`:

    export prancer-git=password

When you run the prancer, it will automatically read the value from the environment variable.

# Users

Other connectors such as **AWS** and **Azure** allow you to configure multiple users, the **filesystem** connector doesn't as it doesn't have permissions other than read. This means that you must always use the same username defined in the **filesystem** connector file in the snapshot configuration files.