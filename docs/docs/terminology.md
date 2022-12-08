# Prancer Terminology

**Prancer** has its own set of terms that need to be understood before you delve deeper into it. Take time to understand each concept properly before going on.

# Providers & connectors

A **provider** is a system that provides data to **Prancer** platform. For example:

- Azure
- Amazon Web Services
- Google Cloud
- Kubernetes
- Filesystem

A **connector** file holds enough information to connect to those providers. For example, address and credentials are information we usually see in a **connector** file. 

# Monitored resources & snapshots

A **monitored resource**, is an item that you want **Prancer** to observe, monitor, and validate. This resource could be in the cloud or in a filesystem. You define monitored resources through a **snapshot configuration** file.

A **snapshot configuration** file is used to define what you want to observe. It will use a **connector** that you previously configured to get a representation of a **monitored resource** on the referenced **provider**. By using different **connectors**, you can gather a broad range of snapshots of your various systems.

A **master snapshot configuration** file is used to define the type of resources you want to observe. The difference between **master snapshot configuration** file and a **snapshot configuration** file is that you have a type of resource in the first one. But in the latter, you have individual resources.
For example, following items are content of a **master snapshot configuration:** Virtual Machines,
Virtual Networks and
Security Groups .

However, the content of the **snapshot configuration** file is as follows:
Virtual Machine A,
Virtual Machine B,
Virtual Network a,
Security Group 1 and
Security Group 2

As you see in this example, in the **master snapshot configuration** file, we have the type of resources (i.e. Virtual Machines, Virtual Networks and Security Groups), but in the **snapshot configuration** file, we have the individual instances of these resource types.

The **crawler** processor uses the **master snapshot configuration** file to find new resources in the target environment and generates a **snapshot configuration** file if we need it.

When you gather data about your **monitored resources**, you create **snapshots**. **Snapshots** are actual representations of **monitored resources** in JSON format. These **snapshots** are kept in a filesystem/database over time so you can track the changes if anything happens.

# Tests, rules & reports

**Prancer** uses **tests** to validate your infrastructure. A **test** runs a set of rules on available **snapshot** items. The output of the **test** could be <strong style="color: green;">passed</strong>  or <strong style="color: red; ">failed</strong>. To figure out what to run the tests over. A **test file** contains various test cases against the **monitored resources**.

**Rules** are an essential part of a **test**. **Rules** define what needs to be tested. **Prancer** uses a custom Domain Specific Language (DSL) that looks a lot like **Javascript** to run tests. The **rules** comparison engine runs against a **monitored resource**'s **snapshot** and checks the values collected against others (static or dynamic) to validate your infrastructure or files. It is also possible to write tests in OPA **Rego** policy language.

A **Master test** file is a test file in the prancer cloud validation framework, which defines test cases for different **types** of monitored resources rather than individual resources. A master test file works in tandem with the **master snapshot configuration** file to run test cases on different types of resources.

When **Prancer** runs tests, it generates an **output** for every test file. All the test cases available in a test file will be evaluated, and a result will be saved to this report file so you can put them in an artifact system for later reference.

# Collections

A **collection** is a set of configuration files that can be committed to a version control system alongside of your project. Example of such files:

* Project configuration
* Connector configuration
* Snapshot configuration
* Test file
* Optional Exclusion file for specific resource/specific test/combination of both.

The **Collection** is a powerful concept that can be used based on the organization's definition. It could work as a project, a repo, a business sector, or a company.

These files should follow your development project that would usually contain **infrastructure as code** files such as:

* **AWS CloudFormation** templates
* **Azure ARM** templates
* **Terraform** scripts
* etc

With those two elements in place, **Prancer** can be used to validate the files **before** applying them and can also be used **after** applying them directly on the provider of your choice.

**Collections** (previously known as containers) are simple folders that allow you to group your snapshots and tests in a logical way to help you better manage your different tests, infrastructure components and results.

To understand these concepts better, you can review [Introduction to Prancer Platform Configuration Files](https://www.prancer.io/what-are-the-configuration-files-in-the-prancer-framework/)