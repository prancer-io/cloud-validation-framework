The **Filesystem** connector allows you to inspect files from a local file system or git repository. It acts more as a prevention mechanism when opposed to service connectors such as **AWS** or **Azure**. This is the main connector we use for **Infrastructure as Code** validation. While the **Filesystem** connector will inspect a static file committed into your project, the service connectors validate actual infrastructure components. Therefore, you should use this connector to preemptively validate your cloud management templates before applying changes to your infrastructure.

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
> This file can be named anything you want but we suggest `fsConnector.json`

**local filesystem example**

{
    "fileType": "structure",
    "type": "filesystem",
    "companyName": "Organization name",
    "folderPath": "<path-to-folder>"
}

**Public HTTPS or SSH example**

    {
        "fileType": "structure",
        "type": "filesystem",
        "companyName": "Organization name",
        "gitProvider": "<url-to-repository>",
        "branchName": "<branch>",
        "private": false
    }

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
| httpsUser | Username used to connect to the repository when using a private HTTPS repository |
| httpsPassword | Password used to connect to the repository when using a private HTTPS repository |
| sshUser | Username used to execute operations on repository such as commits, merges, tags, etc |
| sshHost | Host entry to put in temporary config file, this should be the same as what is in `url-to-repository` |
| sshKeyfile | Path to the private key file when using a private SSH repository. this should be an absolute path. do not use `~` for home directory |
| private | Boolean value stating if the repository is private or public |
| folderPath | Absolute path to the folder  |

* **Note**: Path expansions are not implemented yet, you need to provide full paths!

# Users

Other connectors such as **AWS** and **Azure** allow you to configure multiple users, the **filesystem** connector doesn't as it doesn't have permissions other than read. This means that you must always use the same username defined in the **filesystem** connector file in the snapshot configuration files.