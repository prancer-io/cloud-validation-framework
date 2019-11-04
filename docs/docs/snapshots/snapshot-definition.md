## Introduction
prancer cloud validation framework can connect to various providers to capture monitored resources states and run tests against them. To do that, we need configuration files to address those monitored resources and take snapshots and store them. 

## Definitions
- **Master Snapshot Configuration File**: a json based configuration file in the prancer cloud validation framework which defines the **type of resources** in a target environment. As an example, in a master snapshot configuration file we define different type of resources in the Azure: Virtual Machine, Virtual Network, Network Security Group.

- **Snapshot Configuration File**: a json based configuration file in the prancer cloud validation framework which defines **individual resources** in a target environment. As an example, in a snapshot configuration file we define individual resources in our Azure cloud: Virtual Machine 1, Virtual Machine 2, Virtual Network A.

- **Snapshot**: a json based file which contains the *state* of a monitored resource at a given time.

> **crawler** which is an enterprise edition feature of the Prancer cloud validation framework is using the **master snapshot configuration file** to examine the target environment and find new resources. It generates the snapshot configuration files automatically. For more information read the crawler section.