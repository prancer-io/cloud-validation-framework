**Prancer** can leverage secrets from different sources such as an **Azure key vault** when required.

This concept only applies to the **Azure** connector that you will see a little later. If you do not want to store your SPN secrets in files anywhere, then a good alternative will be to use an **Azure key vault**.

# Limitations

It is important to understand that **Azure key vaults** are only available in interactive mode because the SPN password to access the key vault must be typed on the console when running the tests. This doesn't prevent you from using secrets as there are other ways to do so. Read on!

# Providing secrets to Prancer

There are multiple ways of providing secrets to **Prancer**:

1. Put secrets in the configuration files
2. Put the secret value in an environment variable (Linux only)
3. Configure and put the secret in an **Azure key vault**
4. Provide the secret manually at run-time in an interactive session

# Put secrets in the configuration files

While it is possible to put secrets in configuration files, it is **strongly advised not to be done**. Most of the time, these files are commited to a version control system and this means that the password is then stored forever in history.

# Exporting environment variables

The simplest approach after writting secrets in configuration files is to use environment variables when your system runs on Linux. 

To do so, export a `username=secret` environment variable where the value of that environment variable will be the secret **Prancer** needs to run with. For example:

    export username=secretkey

To support this, the `secret` must not be set in the connector's configuration file **and** there musn't be any **Azure key vault** configured in the main configuration file.

# Put the secrets in Azure Key Vaults

**Prancer** supports secrets to be read from an **Azure key vault**. This is done by using a special service principal name (SPN) using the **Azure** ReST APIs. The SPN should have access to read the secrets from the key vault and the key vault and secrets vault configuration must be set in the main configuration file.

When the tests run, it will ask you for your secret to unlock the **Azure key vault**. 

* **Note**: This means **you cannot use key vaults in a non-interactive way**.

# Provide the secret at run-time

If none of the previous methods worked, the system will ask for the password using the interactive command line. 

* **Note**: This means **you cannot use this method in a non-interactive way**.