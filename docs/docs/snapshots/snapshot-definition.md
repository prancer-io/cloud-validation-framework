## Introduction
prancer validation framework can connect to various providers to capture monitored resources states and run compliance tests against them. For that purpose, we need snapshot configuration files to specify those monitored resources and take snapshots and store them. 

## Definitions
- **Master Snapshot Configuration File**: a json based configuration file in the prancer cloud validation framework which defines the **type of monitored resources** in a target environment. As an example, in a master snapshot configuration file we define different type of resources in the Azure: Virtual Machine, Virtual Network, Network Security Group, ....

- **Snapshot Configuration File**: a json based configuration file in the prancer cloud validation framework which defines **individual monitored resources** in a target environment. As an example, in a snapshot configuration file we define individual resources in our Azure cloud: Virtual Machine 1, Virtual Machine 2, Virtual Network A.

- **Snapshot**: a json based file which contains the *state* of a monitored resource at a given time.

> **crawler** which is an enterprise edition feature of the Prancer cloud validation framework leverages the **master snapshot configuration file** to examine the target environment and find new resources. It generates the snapshot configuration files automatically. For more information read the crawler section.

<iframe width="560" height="315" src="https://www.youtube.com/embed/zDbnHKaXBhM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>