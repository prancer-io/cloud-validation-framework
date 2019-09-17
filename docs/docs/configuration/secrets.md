In order to connect to a back-end API system, **Prancer** can leverage secrets from different sources when required.

# Providing secrets to Prancer

There are multiple ways of providing secrets to **Prancer**. Here is the ordering which Prancer Validation Framework searches for secrets:

1. Secrets in the configuration file
2. Secret value in an environment variable (Linux only)
3. Configure and put the secret in a vault (**CyberArk** or **Azure key vault**)
4. Provide the secret manually at run-time in an interactive session

# Put secrets in the configuration files

While it is possible to put secrets in configuration files, it is **strongly advised not to be done**. Most of the time, these files are commited to a version control system and this means that the password is then stored forever in history.

# Exporting environment variables

The simplest approach after writting secrets in configuration files is to use environment variables when your system runs on Linux. 

To do so, export a `username=secret` environment variable where the value of that environment variable will be the secret **Prancer** needs to run with. For example:

    export username=secretkey

To support this, the `secret` must not be set in the connector's configuration file **and** there musn't be any **Azure key vault** configured in the main configuration file.


# Putting secrets in CyberArk
**CyberArk** (http://www.cyberark.com) Application Access Manager for DevOps provides a secrets management solution tailored specifically to the unique requirements of native-cloud and DevOps environments. The solution manages secrets and credentials used by non-human identities including DevOps and PaaS tools, and containers. **Prancer** validation framework supports secrets to be read from the **CyberArk**. Here are the steps:

1. DevOps Engineer starts the **Prancer** validation framework.
2. **Prancer** validation framework is integrated with CyberArk to retrieve secrets
    a. CyberArk Agent has to be installed and configured on the respective servers (containers) and the firewall ports have to be opened 
3. The **Prancer** validation framework runs the cyberArk agent cli and connects to the CyberArk safe to fetch the Password for the account.
4. CyberArk passes the retrieved password to the modules that need the secret during the validation process
5. If any errors occur (due to CyberArk not being installed properly or any other errors) then **Prancer** validation framework checks for the other ways to retireve the secret

In order to config CyberArk integration, you need to put these values in the config file:
```
[VAULT]
type = cyberark
CA_OBJECT = 'object name'
CA_SAFE = True
CA_EXE = 'Path to the cyberark executable'
CA_APPID = 'APP ID used for storing the object name'
```

# Putting secrets in Azure Key Vault

**Prancer** supports secrets to be read from an **Azure key vault**. This is done by using a special service principal name (SPN) using the **Azure** ReST APIs. The SPN should have access to read the secrets from the key vault and the key vault and secrets vault configuration must be set in the main configuration file.

When the tests run, it will ask you for your secret to unlock the **Azure key vault**. 

In order to config Azure Key Vault integration, you need to put these values in the config file:
```
[VAULT]
type = azure
tenant_id = 'Tenant Id'
client_id = 'Service Principal Id to connect to the Azure Keyvault'
keyvault = 'Keyvault where secrets are stored'
```

* **Note**: This means **you cannot use key vaults in a non-interactive way**.
## Limitations

It is important to understand that **Azure key vaults** are only available in interactive mode because the SPN password to access the key vault must be typed on the console when running the tests. This doesn't prevent you from using secrets as there are other ways to do so. Read on!


# Provide the secret at run-time

If none of the previous methods worked, the system will ask for the password using the interactive command line. 

* **Note**: This means **you cannot use this method in a non-interactive way**.