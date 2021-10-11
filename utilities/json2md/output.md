# Automated Vulnerability Scan result and Static Code Analysis for Azure Quickstart files

## Azure Kubernetes Services (AKS)

Source Repository: https://github.com/Azure/azure-quickstart-templates

Scan engine: **Prancer Framework** (https://www.prancer.io)

Compliance Database: https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac

## Compliance run Meta Data
| Title     | Description         |
|:----------|:--------------------|
| timestamp | 1628197704243       |
| snapshot  | master-snapshot_gen |
| container | scenario-arm-ms     |
| test      | master-test.json    |

## Results

### Test ID - PR-AZR-0006-ARM
Title: Azure CNI networking should be enabled in Azure AKS cluster\
Test Result: **failed**\
Description : Azure CNI provides the following features over kubenet networking:_x000D__x000D_- Every pod in the cluster is assigned an IP address in the virtual network. The pods can directly communicate with other pods in the cluster, and other nodes in the virtual network._x000D_- Pods in a subnet that have service endpoints enabled can securely connect to Azure services, such as Azure Storage and SQL DB._x000D_- You can create user-defined routes (UDR) to route traffic from pods to a Network Virtual Appliance._x000D_- Support for Network Policies securing communication between pods._x000D__x000D_This policy checks your AKS cluster for the Azure CNI network plugin and generates an alert if not found.\

#### Test Details
- eval: data.rule.aks_cni_net
- id : PR-AZR-0006-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT82                                                                                                                                                                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_1
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0006-ARM
Title: Azure CNI networking should be enabled in Azure AKS cluster\
Test Result: **failed**\
Description : Azure CNI provides the following features over kubenet networking:_x000D__x000D_- Every pod in the cluster is assigned an IP address in the virtual network. The pods can directly communicate with other pods in the cluster, and other nodes in the virtual network._x000D_- Pods in a subnet that have service endpoints enabled can securely connect to Azure services, such as Azure Storage and SQL DB._x000D_- You can create user-defined routes (UDR) to route traffic from pods to a Network Virtual Appliance._x000D_- Support for Network Policies securing communication between pods._x000D__x000D_This policy checks your AKS cluster for the Azure CNI network plugin and generates an alert if not found.\

#### Test Details
- eval: data.rule.aks_cni_net
- id : PR-AZR-0006-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                       |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT389                                                                                                                                                                                                                                                                                          |
| structure  | filesystem                                                                                                                                                                                                                                                                                                        |
| reference  | master                                                                                                                                                                                                                                                                                                            |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                 |
| collection | armtemplate                                                                                                                                                                                                                                                                                                       |
| type       | arm                                                                                                                                                                                                                                                                                                               |
| region     |                                                                                                                                                                                                                                                                                                                   |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_1
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0006-ARM
Title: Azure CNI networking should be enabled in Azure AKS cluster\
Test Result: **passed**\
Description : Azure CNI provides the following features over kubenet networking:_x000D__x000D_- Every pod in the cluster is assigned an IP address in the virtual network. The pods can directly communicate with other pods in the cluster, and other nodes in the virtual network._x000D_- Pods in a subnet that have service endpoints enabled can securely connect to Azure services, such as Azure Storage and SQL DB._x000D_- You can create user-defined routes (UDR) to route traffic from pods to a Network Virtual Appliance._x000D_- Support for Network Policies securing communication between pods._x000D__x000D_This policy checks your AKS cluster for the Azure CNI network plugin and generates an alert if not found.\

#### Test Details
- eval: data.rule.aks_cni_net
- id : PR-AZR-0006-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                         |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT396                                                                                                                                                                                                                                                                                            |
| structure  | filesystem                                                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_1
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0006-ARM
Title: Azure CNI networking should be enabled in Azure AKS cluster\
Test Result: **passed**\
Description : Azure CNI provides the following features over kubenet networking:_x000D__x000D_- Every pod in the cluster is assigned an IP address in the virtual network. The pods can directly communicate with other pods in the cluster, and other nodes in the virtual network._x000D_- Pods in a subnet that have service endpoints enabled can securely connect to Azure services, such as Azure Storage and SQL DB._x000D_- You can create user-defined routes (UDR) to route traffic from pods to a Network Virtual Appliance._x000D_- Support for Network Policies securing communication between pods._x000D__x000D_This policy checks your AKS cluster for the Azure CNI network plugin and generates an alert if not found.\

#### Test Details
- eval: data.rule.aks_cni_net
- id : PR-AZR-0006-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                 |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT399                                                                                                                                                                                                                                                                                                    |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                  |
| reference  | master                                                                                                                                                                                                                                                                                                                      |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                           |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                 |
| type       | arm                                                                                                                                                                                                                                                                                                                         |
| region     |                                                                                                                                                                                                                                                                                                                             |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_1
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0006-ARM
Title: Azure CNI networking should be enabled in Azure AKS cluster\
Test Result: **passed**\
Description : Azure CNI provides the following features over kubenet networking:_x000D__x000D_- Every pod in the cluster is assigned an IP address in the virtual network. The pods can directly communicate with other pods in the cluster, and other nodes in the virtual network._x000D_- Pods in a subnet that have service endpoints enabled can securely connect to Azure services, such as Azure Storage and SQL DB._x000D_- You can create user-defined routes (UDR) to route traffic from pods to a Network Virtual Appliance._x000D_- Support for Network Policies securing communication between pods._x000D__x000D_This policy checks your AKS cluster for the Azure CNI network plugin and generates an alert if not found.\

#### Test Details
- eval: data.rule.aks_cni_net
- id : PR-AZR-0006-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT591                                                                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_1
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0006-ARM
Title: Azure CNI networking should be enabled in Azure AKS cluster\
Test Result: **failed**\
Description : Azure CNI provides the following features over kubenet networking:_x000D__x000D_- Every pod in the cluster is assigned an IP address in the virtual network. The pods can directly communicate with other pods in the cluster, and other nodes in the virtual network._x000D_- Pods in a subnet that have service endpoints enabled can securely connect to Azure services, such as Azure Storage and SQL DB._x000D_- You can create user-defined routes (UDR) to route traffic from pods to a Network Virtual Appliance._x000D_- Support for Network Policies securing communication between pods._x000D__x000D_This policy checks your AKS cluster for the Azure CNI network plugin and generates an alert if not found.\

#### Test Details
- eval: data.rule.aks_cni_net
- id : PR-AZR-0006-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                   |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT866                                                                                                                                                                                                                                      |
| structure  | filesystem                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_1
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0006-ARM
Title: Azure CNI networking should be enabled in Azure AKS cluster\
Test Result: **failed**\
Description : Azure CNI provides the following features over kubenet networking:_x000D__x000D_- Every pod in the cluster is assigned an IP address in the virtual network. The pods can directly communicate with other pods in the cluster, and other nodes in the virtual network._x000D_- Pods in a subnet that have service endpoints enabled can securely connect to Azure services, such as Azure Storage and SQL DB._x000D_- You can create user-defined routes (UDR) to route traffic from pods to a Network Virtual Appliance._x000D_- Support for Network Policies securing communication between pods._x000D__x000D_This policy checks your AKS cluster for the Azure CNI network plugin and generates an alert if not found.\

#### Test Details
- eval: data.rule.aks_cni_net
- id : PR-AZR-0006-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                             |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT867                                                                                                                                                                                                                                                                                                |
| structure  | filesystem                                                                                                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_1
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0006-ARM
Title: Azure CNI networking should be enabled in Azure AKS cluster\
Test Result: **passed**\
Description : Azure CNI provides the following features over kubenet networking:_x000D__x000D_- Every pod in the cluster is assigned an IP address in the virtual network. The pods can directly communicate with other pods in the cluster, and other nodes in the virtual network._x000D_- Pods in a subnet that have service endpoints enabled can securely connect to Azure services, such as Azure Storage and SQL DB._x000D_- You can create user-defined routes (UDR) to route traffic from pods to a Network Virtual Appliance._x000D_- Support for Network Policies securing communication between pods._x000D__x000D_This policy checks your AKS cluster for the Azure CNI network plugin and generates an alert if not found.\

#### Test Details
- eval: data.rule.aks_cni_net
- id : PR-AZR-0006-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                             |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1148                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_1
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0006-ARM
Title: Azure CNI networking should be enabled in Azure AKS cluster\
Test Result: **passed**\
Description : Azure CNI provides the following features over kubenet networking:_x000D__x000D_- Every pod in the cluster is assigned an IP address in the virtual network. The pods can directly communicate with other pods in the cluster, and other nodes in the virtual network._x000D_- Pods in a subnet that have service endpoints enabled can securely connect to Azure services, such as Azure Storage and SQL DB._x000D_- You can create user-defined routes (UDR) to route traffic from pods to a Network Virtual Appliance._x000D_- Support for Network Policies securing communication between pods._x000D__x000D_This policy checks your AKS cluster for the Azure CNI network plugin and generates an alert if not found.\

#### Test Details
- eval: data.rule.aks_cni_net
- id : PR-AZR-0006-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                         |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1702                                                                                                                                                                                                                                                           |
| structure  | filesystem                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_1
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0006-ARM
Title: Azure CNI networking should be enabled in Azure AKS cluster\
Test Result: **passed**\
Description : Azure CNI provides the following features over kubenet networking:_x000D__x000D_- Every pod in the cluster is assigned an IP address in the virtual network. The pods can directly communicate with other pods in the cluster, and other nodes in the virtual network._x000D_- Pods in a subnet that have service endpoints enabled can securely connect to Azure services, such as Azure Storage and SQL DB._x000D_- You can create user-defined routes (UDR) to route traffic from pods to a Network Virtual Appliance._x000D_- Support for Network Policies securing communication between pods._x000D__x000D_This policy checks your AKS cluster for the Azure CNI network plugin and generates an alert if not found.\

#### Test Details
- eval: data.rule.aks_cni_net
- id : PR-AZR-0006-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                            |
|:-----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1703                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                             |
| reference  | master                                                                                                                                                                                                                                                                                 |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                      |
| collection | armtemplate                                                                                                                                                                                                                                                                            |
| type       | arm                                                                                                                                                                                                                                                                                    |
| region     |                                                                                                                                                                                                                                                                                        |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.us.json'] |

- masterTestId: TEST_AKS_1
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0006-ARM
Title: Azure CNI networking should be enabled in Azure AKS cluster\
Test Result: **failed**\
Description : Azure CNI provides the following features over kubenet networking:_x000D__x000D_- Every pod in the cluster is assigned an IP address in the virtual network. The pods can directly communicate with other pods in the cluster, and other nodes in the virtual network._x000D_- Pods in a subnet that have service endpoints enabled can securely connect to Azure services, such as Azure Storage and SQL DB._x000D_- You can create user-defined routes (UDR) to route traffic from pods to a Network Virtual Appliance._x000D_- Support for Network Policies securing communication between pods._x000D__x000D_This policy checks your AKS cluster for the Azure CNI network plugin and generates an alert if not found.\

#### Test Details
- eval: data.rule.aks_cni_net
- id : PR-AZR-0006-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                   |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1796                                                                                                                                                                                                                                                                     |
| structure  | filesystem                                                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_1
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0007-ARM
Title: Azure AKS cluster HTTP application routing should be disabled\
Test Result: **passed**\
Description : The HTTP application routing add-on is designed to let you quickly create an ingress controller and access your applications. This add-on is not currently designed for use in a production environment and is not recommended for production use. For production-ready ingress deployments that include multiple replicas and TLS support, see Create an HTTPS ingress controller.\

#### Test Details
- eval: data.rule.aks_http_routing
- id : PR-AZR-0007-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT82                                                                                                                                                                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_2
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0007-ARM
Title: Azure AKS cluster HTTP application routing should be disabled\
Test Result: **passed**\
Description : The HTTP application routing add-on is designed to let you quickly create an ingress controller and access your applications. This add-on is not currently designed for use in a production environment and is not recommended for production use. For production-ready ingress deployments that include multiple replicas and TLS support, see Create an HTTPS ingress controller.\

#### Test Details
- eval: data.rule.aks_http_routing
- id : PR-AZR-0007-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                       |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT389                                                                                                                                                                                                                                                                                          |
| structure  | filesystem                                                                                                                                                                                                                                                                                                        |
| reference  | master                                                                                                                                                                                                                                                                                                            |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                 |
| collection | armtemplate                                                                                                                                                                                                                                                                                                       |
| type       | arm                                                                                                                                                                                                                                                                                                               |
| region     |                                                                                                                                                                                                                                                                                                                   |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_2
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0007-ARM
Title: Azure AKS cluster HTTP application routing should be disabled\
Test Result: **passed**\
Description : The HTTP application routing add-on is designed to let you quickly create an ingress controller and access your applications. This add-on is not currently designed for use in a production environment and is not recommended for production use. For production-ready ingress deployments that include multiple replicas and TLS support, see Create an HTTPS ingress controller.\

#### Test Details
- eval: data.rule.aks_http_routing
- id : PR-AZR-0007-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                         |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT396                                                                                                                                                                                                                                                                                            |
| structure  | filesystem                                                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_2
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0007-ARM
Title: Azure AKS cluster HTTP application routing should be disabled\
Test Result: **passed**\
Description : The HTTP application routing add-on is designed to let you quickly create an ingress controller and access your applications. This add-on is not currently designed for use in a production environment and is not recommended for production use. For production-ready ingress deployments that include multiple replicas and TLS support, see Create an HTTPS ingress controller.\

#### Test Details
- eval: data.rule.aks_http_routing
- id : PR-AZR-0007-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                 |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT399                                                                                                                                                                                                                                                                                                    |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                  |
| reference  | master                                                                                                                                                                                                                                                                                                                      |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                           |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                 |
| type       | arm                                                                                                                                                                                                                                                                                                                         |
| region     |                                                                                                                                                                                                                                                                                                                             |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_2
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0007-ARM
Title: Azure AKS cluster HTTP application routing should be disabled\
Test Result: **passed**\
Description : The HTTP application routing add-on is designed to let you quickly create an ingress controller and access your applications. This add-on is not currently designed for use in a production environment and is not recommended for production use. For production-ready ingress deployments that include multiple replicas and TLS support, see Create an HTTPS ingress controller.\

#### Test Details
- eval: data.rule.aks_http_routing
- id : PR-AZR-0007-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT591                                                                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_2
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0007-ARM
Title: Azure AKS cluster HTTP application routing should be disabled\
Test Result: **passed**\
Description : The HTTP application routing add-on is designed to let you quickly create an ingress controller and access your applications. This add-on is not currently designed for use in a production environment and is not recommended for production use. For production-ready ingress deployments that include multiple replicas and TLS support, see Create an HTTPS ingress controller.\

#### Test Details
- eval: data.rule.aks_http_routing
- id : PR-AZR-0007-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                   |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT866                                                                                                                                                                                                                                      |
| structure  | filesystem                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_2
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0007-ARM
Title: Azure AKS cluster HTTP application routing should be disabled\
Test Result: **passed**\
Description : The HTTP application routing add-on is designed to let you quickly create an ingress controller and access your applications. This add-on is not currently designed for use in a production environment and is not recommended for production use. For production-ready ingress deployments that include multiple replicas and TLS support, see Create an HTTPS ingress controller.\

#### Test Details
- eval: data.rule.aks_http_routing
- id : PR-AZR-0007-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                             |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT867                                                                                                                                                                                                                                                                                                |
| structure  | filesystem                                                                                                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_2
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0007-ARM
Title: Azure AKS cluster HTTP application routing should be disabled\
Test Result: **passed**\
Description : The HTTP application routing add-on is designed to let you quickly create an ingress controller and access your applications. This add-on is not currently designed for use in a production environment and is not recommended for production use. For production-ready ingress deployments that include multiple replicas and TLS support, see Create an HTTPS ingress controller.\

#### Test Details
- eval: data.rule.aks_http_routing
- id : PR-AZR-0007-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                             |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1148                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_2
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0007-ARM
Title: Azure AKS cluster HTTP application routing should be disabled\
Test Result: **passed**\
Description : The HTTP application routing add-on is designed to let you quickly create an ingress controller and access your applications. This add-on is not currently designed for use in a production environment and is not recommended for production use. For production-ready ingress deployments that include multiple replicas and TLS support, see Create an HTTPS ingress controller.\

#### Test Details
- eval: data.rule.aks_http_routing
- id : PR-AZR-0007-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                         |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1702                                                                                                                                                                                                                                                           |
| structure  | filesystem                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_2
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0007-ARM
Title: Azure AKS cluster HTTP application routing should be disabled\
Test Result: **passed**\
Description : The HTTP application routing add-on is designed to let you quickly create an ingress controller and access your applications. This add-on is not currently designed for use in a production environment and is not recommended for production use. For production-ready ingress deployments that include multiple replicas and TLS support, see Create an HTTPS ingress controller.\

#### Test Details
- eval: data.rule.aks_http_routing
- id : PR-AZR-0007-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                            |
|:-----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1703                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                             |
| reference  | master                                                                                                                                                                                                                                                                                 |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                      |
| collection | armtemplate                                                                                                                                                                                                                                                                            |
| type       | arm                                                                                                                                                                                                                                                                                    |
| region     |                                                                                                                                                                                                                                                                                        |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.us.json'] |

- masterTestId: TEST_AKS_2
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0007-ARM
Title: Azure AKS cluster HTTP application routing should be disabled\
Test Result: **passed**\
Description : The HTTP application routing add-on is designed to let you quickly create an ingress controller and access your applications. This add-on is not currently designed for use in a production environment and is not recommended for production use. For production-ready ingress deployments that include multiple replicas and TLS support, see Create an HTTPS ingress controller.\

#### Test Details
- eval: data.rule.aks_http_routing
- id : PR-AZR-0007-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                   |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1796                                                                                                                                                                                                                                                                     |
| structure  | filesystem                                                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_2
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0008-ARM
Title: Azure AKS cluster monitoring should be enabled\
Test Result: **failed**\
Description : Azure Monitor for containers gives you performance visibility by collecting memory and processor metrics from controllers, nodes, and containers that are available in Kubernetes through the Metrics API. Container logs are also collected. After you enable monitoring from Kubernetes clusters, metrics and logs are automatically collected for you through a containerized version of the Log Analytics agent for Linux. Metrics are written to the metrics store and log data is written to the logs store associated with your Log Analytics workspace.\

#### Test Details
- eval: data.rule.aks_monitoring
- id : PR-AZR-0008-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT82                                                                                                                                                                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_3
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0008-ARM
Title: Azure AKS cluster monitoring should be enabled\
Test Result: **failed**\
Description : Azure Monitor for containers gives you performance visibility by collecting memory and processor metrics from controllers, nodes, and containers that are available in Kubernetes through the Metrics API. Container logs are also collected. After you enable monitoring from Kubernetes clusters, metrics and logs are automatically collected for you through a containerized version of the Log Analytics agent for Linux. Metrics are written to the metrics store and log data is written to the logs store associated with your Log Analytics workspace.\

#### Test Details
- eval: data.rule.aks_monitoring
- id : PR-AZR-0008-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                       |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT389                                                                                                                                                                                                                                                                                          |
| structure  | filesystem                                                                                                                                                                                                                                                                                                        |
| reference  | master                                                                                                                                                                                                                                                                                                            |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                 |
| collection | armtemplate                                                                                                                                                                                                                                                                                                       |
| type       | arm                                                                                                                                                                                                                                                                                                               |
| region     |                                                                                                                                                                                                                                                                                                                   |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_3
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0008-ARM
Title: Azure AKS cluster monitoring should be enabled\
Test Result: **failed**\
Description : Azure Monitor for containers gives you performance visibility by collecting memory and processor metrics from controllers, nodes, and containers that are available in Kubernetes through the Metrics API. Container logs are also collected. After you enable monitoring from Kubernetes clusters, metrics and logs are automatically collected for you through a containerized version of the Log Analytics agent for Linux. Metrics are written to the metrics store and log data is written to the logs store associated with your Log Analytics workspace.\

#### Test Details
- eval: data.rule.aks_monitoring
- id : PR-AZR-0008-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                         |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT396                                                                                                                                                                                                                                                                                            |
| structure  | filesystem                                                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_3
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0008-ARM
Title: Azure AKS cluster monitoring should be enabled\
Test Result: **failed**\
Description : Azure Monitor for containers gives you performance visibility by collecting memory and processor metrics from controllers, nodes, and containers that are available in Kubernetes through the Metrics API. Container logs are also collected. After you enable monitoring from Kubernetes clusters, metrics and logs are automatically collected for you through a containerized version of the Log Analytics agent for Linux. Metrics are written to the metrics store and log data is written to the logs store associated with your Log Analytics workspace.\

#### Test Details
- eval: data.rule.aks_monitoring
- id : PR-AZR-0008-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                 |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT399                                                                                                                                                                                                                                                                                                    |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                  |
| reference  | master                                                                                                                                                                                                                                                                                                                      |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                           |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                 |
| type       | arm                                                                                                                                                                                                                                                                                                                         |
| region     |                                                                                                                                                                                                                                                                                                                             |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_3
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0008-ARM
Title: Azure AKS cluster monitoring should be enabled\
Test Result: **passed**\
Description : Azure Monitor for containers gives you performance visibility by collecting memory and processor metrics from controllers, nodes, and containers that are available in Kubernetes through the Metrics API. Container logs are also collected. After you enable monitoring from Kubernetes clusters, metrics and logs are automatically collected for you through a containerized version of the Log Analytics agent for Linux. Metrics are written to the metrics store and log data is written to the logs store associated with your Log Analytics workspace.\

#### Test Details
- eval: data.rule.aks_monitoring
- id : PR-AZR-0008-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT591                                                                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_3
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0008-ARM
Title: Azure AKS cluster monitoring should be enabled\
Test Result: **failed**\
Description : Azure Monitor for containers gives you performance visibility by collecting memory and processor metrics from controllers, nodes, and containers that are available in Kubernetes through the Metrics API. Container logs are also collected. After you enable monitoring from Kubernetes clusters, metrics and logs are automatically collected for you through a containerized version of the Log Analytics agent for Linux. Metrics are written to the metrics store and log data is written to the logs store associated with your Log Analytics workspace.\

#### Test Details
- eval: data.rule.aks_monitoring
- id : PR-AZR-0008-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                   |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT866                                                                                                                                                                                                                                      |
| structure  | filesystem                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_3
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0008-ARM
Title: Azure AKS cluster monitoring should be enabled\
Test Result: **failed**\
Description : Azure Monitor for containers gives you performance visibility by collecting memory and processor metrics from controllers, nodes, and containers that are available in Kubernetes through the Metrics API. Container logs are also collected. After you enable monitoring from Kubernetes clusters, metrics and logs are automatically collected for you through a containerized version of the Log Analytics agent for Linux. Metrics are written to the metrics store and log data is written to the logs store associated with your Log Analytics workspace.\

#### Test Details
- eval: data.rule.aks_monitoring
- id : PR-AZR-0008-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                             |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT867                                                                                                                                                                                                                                                                                                |
| structure  | filesystem                                                                                                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_3
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0008-ARM
Title: Azure AKS cluster monitoring should be enabled\
Test Result: **passed**\
Description : Azure Monitor for containers gives you performance visibility by collecting memory and processor metrics from controllers, nodes, and containers that are available in Kubernetes through the Metrics API. Container logs are also collected. After you enable monitoring from Kubernetes clusters, metrics and logs are automatically collected for you through a containerized version of the Log Analytics agent for Linux. Metrics are written to the metrics store and log data is written to the logs store associated with your Log Analytics workspace.\

#### Test Details
- eval: data.rule.aks_monitoring
- id : PR-AZR-0008-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                             |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1148                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_3
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0008-ARM
Title: Azure AKS cluster monitoring should be enabled\
Test Result: **failed**\
Description : Azure Monitor for containers gives you performance visibility by collecting memory and processor metrics from controllers, nodes, and containers that are available in Kubernetes through the Metrics API. Container logs are also collected. After you enable monitoring from Kubernetes clusters, metrics and logs are automatically collected for you through a containerized version of the Log Analytics agent for Linux. Metrics are written to the metrics store and log data is written to the logs store associated with your Log Analytics workspace.\

#### Test Details
- eval: data.rule.aks_monitoring
- id : PR-AZR-0008-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                         |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1702                                                                                                                                                                                                                                                           |
| structure  | filesystem                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_3
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0008-ARM
Title: Azure AKS cluster monitoring should be enabled\
Test Result: **failed**\
Description : Azure Monitor for containers gives you performance visibility by collecting memory and processor metrics from controllers, nodes, and containers that are available in Kubernetes through the Metrics API. Container logs are also collected. After you enable monitoring from Kubernetes clusters, metrics and logs are automatically collected for you through a containerized version of the Log Analytics agent for Linux. Metrics are written to the metrics store and log data is written to the logs store associated with your Log Analytics workspace.\

#### Test Details
- eval: data.rule.aks_monitoring
- id : PR-AZR-0008-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                            |
|:-----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1703                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                             |
| reference  | master                                                                                                                                                                                                                                                                                 |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                      |
| collection | armtemplate                                                                                                                                                                                                                                                                            |
| type       | arm                                                                                                                                                                                                                                                                                    |
| region     |                                                                                                                                                                                                                                                                                        |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.us.json'] |

- masterTestId: TEST_AKS_3
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0008-ARM
Title: Azure AKS cluster monitoring should be enabled\
Test Result: **failed**\
Description : Azure Monitor for containers gives you performance visibility by collecting memory and processor metrics from controllers, nodes, and containers that are available in Kubernetes through the Metrics API. Container logs are also collected. After you enable monitoring from Kubernetes clusters, metrics and logs are automatically collected for you through a containerized version of the Log Analytics agent for Linux. Metrics are written to the metrics store and log data is written to the logs store associated with your Log Analytics workspace.\

#### Test Details
- eval: data.rule.aks_monitoring
- id : PR-AZR-0008-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                   |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1796                                                                                                                                                                                                                                                                     |
| structure  | filesystem                                                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_3
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0009-ARM
Title: Azure AKS cluster pool profile count should contain 3 nodes or more\
Test Result: **passed**\
Description : Ensure your AKS cluster pool profile count contains 3 or more nodes. This is recommended for a more resilient cluster. (Clusters smaller than 3 may experience downtime during upgrades.)_x000D__x000D_This policy checks the size of your cluster pool profiles and alerts if there are fewer than 3 nodes.\

#### Test Details
- eval: data.rule.aks_nodes
- id : PR-AZR-0009-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT82                                                                                                                                                                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_4
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0009-ARM
Title: Azure AKS cluster pool profile count should contain 3 nodes or more\
Test Result: **passed**\
Description : Ensure your AKS cluster pool profile count contains 3 or more nodes. This is recommended for a more resilient cluster. (Clusters smaller than 3 may experience downtime during upgrades.)_x000D__x000D_This policy checks the size of your cluster pool profiles and alerts if there are fewer than 3 nodes.\

#### Test Details
- eval: data.rule.aks_nodes
- id : PR-AZR-0009-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                       |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT389                                                                                                                                                                                                                                                                                          |
| structure  | filesystem                                                                                                                                                                                                                                                                                                        |
| reference  | master                                                                                                                                                                                                                                                                                                            |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                 |
| collection | armtemplate                                                                                                                                                                                                                                                                                                       |
| type       | arm                                                                                                                                                                                                                                                                                                               |
| region     |                                                                                                                                                                                                                                                                                                                   |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_4
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0009-ARM
Title: Azure AKS cluster pool profile count should contain 3 nodes or more\
Test Result: **passed**\
Description : Ensure your AKS cluster pool profile count contains 3 or more nodes. This is recommended for a more resilient cluster. (Clusters smaller than 3 may experience downtime during upgrades.)_x000D__x000D_This policy checks the size of your cluster pool profiles and alerts if there are fewer than 3 nodes.\

#### Test Details
- eval: data.rule.aks_nodes
- id : PR-AZR-0009-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                         |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT396                                                                                                                                                                                                                                                                                            |
| structure  | filesystem                                                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_4
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0009-ARM
Title: Azure AKS cluster pool profile count should contain 3 nodes or more\
Test Result: **passed**\
Description : Ensure your AKS cluster pool profile count contains 3 or more nodes. This is recommended for a more resilient cluster. (Clusters smaller than 3 may experience downtime during upgrades.)_x000D__x000D_This policy checks the size of your cluster pool profiles and alerts if there are fewer than 3 nodes.\

#### Test Details
- eval: data.rule.aks_nodes
- id : PR-AZR-0009-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                 |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT399                                                                                                                                                                                                                                                                                                    |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                  |
| reference  | master                                                                                                                                                                                                                                                                                                                      |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                           |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                 |
| type       | arm                                                                                                                                                                                                                                                                                                                         |
| region     |                                                                                                                                                                                                                                                                                                                             |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_4
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0009-ARM
Title: Azure AKS cluster pool profile count should contain 3 nodes or more\
Test Result: **passed**\
Description : Ensure your AKS cluster pool profile count contains 3 or more nodes. This is recommended for a more resilient cluster. (Clusters smaller than 3 may experience downtime during upgrades.)_x000D__x000D_This policy checks the size of your cluster pool profiles and alerts if there are fewer than 3 nodes.\

#### Test Details
- eval: data.rule.aks_nodes
- id : PR-AZR-0009-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT591                                                                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_4
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0009-ARM
Title: Azure AKS cluster pool profile count should contain 3 nodes or more\
Test Result: **passed**\
Description : Ensure your AKS cluster pool profile count contains 3 or more nodes. This is recommended for a more resilient cluster. (Clusters smaller than 3 may experience downtime during upgrades.)_x000D__x000D_This policy checks the size of your cluster pool profiles and alerts if there are fewer than 3 nodes.\

#### Test Details
- eval: data.rule.aks_nodes
- id : PR-AZR-0009-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                   |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT866                                                                                                                                                                                                                                      |
| structure  | filesystem                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_4
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0009-ARM
Title: Azure AKS cluster pool profile count should contain 3 nodes or more\
Test Result: **passed**\
Description : Ensure your AKS cluster pool profile count contains 3 or more nodes. This is recommended for a more resilient cluster. (Clusters smaller than 3 may experience downtime during upgrades.)_x000D__x000D_This policy checks the size of your cluster pool profiles and alerts if there are fewer than 3 nodes.\

#### Test Details
- eval: data.rule.aks_nodes
- id : PR-AZR-0009-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                             |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT867                                                                                                                                                                                                                                                                                                |
| structure  | filesystem                                                                                                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_4
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0009-ARM
Title: Azure AKS cluster pool profile count should contain 3 nodes or more\
Test Result: **passed**\
Description : Ensure your AKS cluster pool profile count contains 3 or more nodes. This is recommended for a more resilient cluster. (Clusters smaller than 3 may experience downtime during upgrades.)_x000D__x000D_This policy checks the size of your cluster pool profiles and alerts if there are fewer than 3 nodes.\

#### Test Details
- eval: data.rule.aks_nodes
- id : PR-AZR-0009-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                             |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1148                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_4
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0009-ARM
Title: Azure AKS cluster pool profile count should contain 3 nodes or more\
Test Result: **passed**\
Description : Ensure your AKS cluster pool profile count contains 3 or more nodes. This is recommended for a more resilient cluster. (Clusters smaller than 3 may experience downtime during upgrades.)_x000D__x000D_This policy checks the size of your cluster pool profiles and alerts if there are fewer than 3 nodes.\

#### Test Details
- eval: data.rule.aks_nodes
- id : PR-AZR-0009-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                         |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1702                                                                                                                                                                                                                                                           |
| structure  | filesystem                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_4
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0009-ARM
Title: Azure AKS cluster pool profile count should contain 3 nodes or more\
Test Result: **passed**\
Description : Ensure your AKS cluster pool profile count contains 3 or more nodes. This is recommended for a more resilient cluster. (Clusters smaller than 3 may experience downtime during upgrades.)_x000D__x000D_This policy checks the size of your cluster pool profiles and alerts if there are fewer than 3 nodes.\

#### Test Details
- eval: data.rule.aks_nodes
- id : PR-AZR-0009-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                            |
|:-----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1703                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                             |
| reference  | master                                                                                                                                                                                                                                                                                 |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                      |
| collection | armtemplate                                                                                                                                                                                                                                                                            |
| type       | arm                                                                                                                                                                                                                                                                                    |
| region     |                                                                                                                                                                                                                                                                                        |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.us.json'] |

- masterTestId: TEST_AKS_4
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0009-ARM
Title: Azure AKS cluster pool profile count should contain 3 nodes or more\
Test Result: **failed**\
Description : Ensure your AKS cluster pool profile count contains 3 or more nodes. This is recommended for a more resilient cluster. (Clusters smaller than 3 may experience downtime during upgrades.)_x000D__x000D_This policy checks the size of your cluster pool profiles and alerts if there are fewer than 3 nodes.\

#### Test Details
- eval: data.rule.aks_nodes
- id : PR-AZR-0009-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                   |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1796                                                                                                                                                                                                                                                                     |
| structure  | filesystem                                                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_4
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0010-ARM
Title: Azure AKS enable role-based access control (RBAC) should be enforced\
Test Result: **passed**\
Description : To provide granular filtering of the actions that users can perform, Kubernetes uses role-based access controls (RBAC). This control mechanism lets you assign users, or groups of users, permission to do things like create or modify resources, or view logs from running application workloads. These permissions can be scoped to a single namespace, or granted across the entire AKS cluster._x005F_x000D_ _x005F_x000D_ This policy checks your AKS cluster RBAC setting and alerts if disabled.\

#### Test Details
- eval: data.rule.aks_rbac
- id : PR-AZR-0010-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT82                                                                                                                                                                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_5
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0010-ARM
Title: Azure AKS enable role-based access control (RBAC) should be enforced\
Test Result: **passed**\
Description : To provide granular filtering of the actions that users can perform, Kubernetes uses role-based access controls (RBAC). This control mechanism lets you assign users, or groups of users, permission to do things like create or modify resources, or view logs from running application workloads. These permissions can be scoped to a single namespace, or granted across the entire AKS cluster._x005F_x000D_ _x005F_x000D_ This policy checks your AKS cluster RBAC setting and alerts if disabled.\

#### Test Details
- eval: data.rule.aks_rbac
- id : PR-AZR-0010-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                       |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT389                                                                                                                                                                                                                                                                                          |
| structure  | filesystem                                                                                                                                                                                                                                                                                                        |
| reference  | master                                                                                                                                                                                                                                                                                                            |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                 |
| collection | armtemplate                                                                                                                                                                                                                                                                                                       |
| type       | arm                                                                                                                                                                                                                                                                                                               |
| region     |                                                                                                                                                                                                                                                                                                                   |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_5
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0010-ARM
Title: Azure AKS enable role-based access control (RBAC) should be enforced\
Test Result: **passed**\
Description : To provide granular filtering of the actions that users can perform, Kubernetes uses role-based access controls (RBAC). This control mechanism lets you assign users, or groups of users, permission to do things like create or modify resources, or view logs from running application workloads. These permissions can be scoped to a single namespace, or granted across the entire AKS cluster._x005F_x000D_ _x005F_x000D_ This policy checks your AKS cluster RBAC setting and alerts if disabled.\

#### Test Details
- eval: data.rule.aks_rbac
- id : PR-AZR-0010-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                         |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT396                                                                                                                                                                                                                                                                                            |
| structure  | filesystem                                                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_5
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0010-ARM
Title: Azure AKS enable role-based access control (RBAC) should be enforced\
Test Result: **passed**\
Description : To provide granular filtering of the actions that users can perform, Kubernetes uses role-based access controls (RBAC). This control mechanism lets you assign users, or groups of users, permission to do things like create or modify resources, or view logs from running application workloads. These permissions can be scoped to a single namespace, or granted across the entire AKS cluster._x005F_x000D_ _x005F_x000D_ This policy checks your AKS cluster RBAC setting and alerts if disabled.\

#### Test Details
- eval: data.rule.aks_rbac
- id : PR-AZR-0010-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                 |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT399                                                                                                                                                                                                                                                                                                    |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                  |
| reference  | master                                                                                                                                                                                                                                                                                                                      |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                           |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                 |
| type       | arm                                                                                                                                                                                                                                                                                                                         |
| region     |                                                                                                                                                                                                                                                                                                                             |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_5
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0010-ARM
Title: Azure AKS enable role-based access control (RBAC) should be enforced\
Test Result: **passed**\
Description : To provide granular filtering of the actions that users can perform, Kubernetes uses role-based access controls (RBAC). This control mechanism lets you assign users, or groups of users, permission to do things like create or modify resources, or view logs from running application workloads. These permissions can be scoped to a single namespace, or granted across the entire AKS cluster._x005F_x000D_ _x005F_x000D_ This policy checks your AKS cluster RBAC setting and alerts if disabled.\

#### Test Details
- eval: data.rule.aks_rbac
- id : PR-AZR-0010-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT591                                                                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_5
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0010-ARM
Title: Azure AKS enable role-based access control (RBAC) should be enforced\
Test Result: **failed**\
Description : To provide granular filtering of the actions that users can perform, Kubernetes uses role-based access controls (RBAC). This control mechanism lets you assign users, or groups of users, permission to do things like create or modify resources, or view logs from running application workloads. These permissions can be scoped to a single namespace, or granted across the entire AKS cluster._x005F_x000D_ _x005F_x000D_ This policy checks your AKS cluster RBAC setting and alerts if disabled.\

#### Test Details
- eval: data.rule.aks_rbac
- id : PR-AZR-0010-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                   |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT866                                                                                                                                                                                                                                      |
| structure  | filesystem                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_5
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0010-ARM
Title: Azure AKS enable role-based access control (RBAC) should be enforced\
Test Result: **passed**\
Description : To provide granular filtering of the actions that users can perform, Kubernetes uses role-based access controls (RBAC). This control mechanism lets you assign users, or groups of users, permission to do things like create or modify resources, or view logs from running application workloads. These permissions can be scoped to a single namespace, or granted across the entire AKS cluster._x005F_x000D_ _x005F_x000D_ This policy checks your AKS cluster RBAC setting and alerts if disabled.\

#### Test Details
- eval: data.rule.aks_rbac
- id : PR-AZR-0010-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                             |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT867                                                                                                                                                                                                                                                                                                |
| structure  | filesystem                                                                                                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_5
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0010-ARM
Title: Azure AKS enable role-based access control (RBAC) should be enforced\
Test Result: **passed**\
Description : To provide granular filtering of the actions that users can perform, Kubernetes uses role-based access controls (RBAC). This control mechanism lets you assign users, or groups of users, permission to do things like create or modify resources, or view logs from running application workloads. These permissions can be scoped to a single namespace, or granted across the entire AKS cluster._x005F_x000D_ _x005F_x000D_ This policy checks your AKS cluster RBAC setting and alerts if disabled.\

#### Test Details
- eval: data.rule.aks_rbac
- id : PR-AZR-0010-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                             |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1148                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_5
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0010-ARM
Title: Azure AKS enable role-based access control (RBAC) should be enforced\
Test Result: **failed**\
Description : To provide granular filtering of the actions that users can perform, Kubernetes uses role-based access controls (RBAC). This control mechanism lets you assign users, or groups of users, permission to do things like create or modify resources, or view logs from running application workloads. These permissions can be scoped to a single namespace, or granted across the entire AKS cluster._x005F_x000D_ _x005F_x000D_ This policy checks your AKS cluster RBAC setting and alerts if disabled.\

#### Test Details
- eval: data.rule.aks_rbac
- id : PR-AZR-0010-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                         |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1702                                                                                                                                                                                                                                                           |
| structure  | filesystem                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_5
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0010-ARM
Title: Azure AKS enable role-based access control (RBAC) should be enforced\
Test Result: **failed**\
Description : To provide granular filtering of the actions that users can perform, Kubernetes uses role-based access controls (RBAC). This control mechanism lets you assign users, or groups of users, permission to do things like create or modify resources, or view logs from running application workloads. These permissions can be scoped to a single namespace, or granted across the entire AKS cluster._x005F_x000D_ _x005F_x000D_ This policy checks your AKS cluster RBAC setting and alerts if disabled.\

#### Test Details
- eval: data.rule.aks_rbac
- id : PR-AZR-0010-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                            |
|:-----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1703                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                             |
| reference  | master                                                                                                                                                                                                                                                                                 |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                      |
| collection | armtemplate                                                                                                                                                                                                                                                                            |
| type       | arm                                                                                                                                                                                                                                                                                    |
| region     |                                                                                                                                                                                                                                                                                        |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.us.json'] |

- masterTestId: TEST_AKS_5
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-0010-ARM
Title: Azure AKS enable role-based access control (RBAC) should be enforced\
Test Result: **failed**\
Description : To provide granular filtering of the actions that users can perform, Kubernetes uses role-based access controls (RBAC). This control mechanism lets you assign users, or groups of users, permission to do things like create or modify resources, or view logs from running application workloads. These permissions can be scoped to a single namespace, or granted across the entire AKS cluster._x005F_x000D_ _x005F_x000D_ This policy checks your AKS cluster RBAC setting and alerts if disabled.\

#### Test Details
- eval: data.rule.aks_rbac
- id : PR-AZR-0010-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                   |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1796                                                                                                                                                                                                                                                                     |
| structure  | filesystem                                                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_5
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-00101-ARM
Title: Managed Azure AD RBAC for AKS cluster should be enabled\
Test Result: **failed**\
Description : Azure Kubernetes Service (AKS) can be configured to use Azure Active Directory (AD) for user authentication. In this configuration, you sign in to an AKS cluster using an Azure AD authentication token. You can also configure Kubernetes role-based access control (Kubernetes RBAC) to limit access to cluster resources based a user's identity or group membership. Visit https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac for details.\

#### Test Details
- eval: data.rule.aks_aad_azure_rbac
- id : PR-AZR-00101-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT82                                                                                                                                                                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-attach-aks/prereqs/prereq.azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_6
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-00101-ARM
Title: Managed Azure AD RBAC for AKS cluster should be enabled\
Test Result: **failed**\
Description : Azure Kubernetes Service (AKS) can be configured to use Azure Active Directory (AD) for user authentication. In this configuration, you sign in to an AKS cluster using an Azure AD authentication token. You can also configure Kubernetes role-based access control (Kubernetes RBAC) to limit access to cluster resources based a user's identity or group membership. Visit https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac for details.\

#### Test Details
- eval: data.rule.aks_aad_azure_rbac
- id : PR-AZR-00101-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                       |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT389                                                                                                                                                                                                                                                                                          |
| structure  | filesystem                                                                                                                                                                                                                                                                                                        |
| reference  | master                                                                                                                                                                                                                                                                                                            |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                 |
| collection | armtemplate                                                                                                                                                                                                                                                                                                       |
| type       | arm                                                                                                                                                                                                                                                                                                               |
| region     |                                                                                                                                                                                                                                                                                                                   |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_6
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-00101-ARM
Title: Managed Azure AD RBAC for AKS cluster should be enabled\
Test Result: **failed**\
Description : Azure Kubernetes Service (AKS) can be configured to use Azure Active Directory (AD) for user authentication. In this configuration, you sign in to an AKS cluster using an Azure AD authentication token. You can also configure Kubernetes role-based access control (Kubernetes RBAC) to limit access to cluster resources based a user's identity or group membership. Visit https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac for details.\

#### Test Details
- eval: data.rule.aks_aad_azure_rbac
- id : PR-AZR-00101-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                         |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT396                                                                                                                                                                                                                                                                                            |
| structure  | filesystem                                                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_6
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-00101-ARM
Title: Managed Azure AD RBAC for AKS cluster should be enabled\
Test Result: **failed**\
Description : Azure Kubernetes Service (AKS) can be configured to use Azure Active Directory (AD) for user authentication. In this configuration, you sign in to an AKS cluster using an Azure AD authentication token. You can also configure Kubernetes role-based access control (Kubernetes RBAC) to limit access to cluster resources based a user's identity or group membership. Visit https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac for details.\

#### Test Details
- eval: data.rule.aks_aad_azure_rbac
- id : PR-AZR-00101-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                 |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT399                                                                                                                                                                                                                                                                                                    |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                  |
| reference  | master                                                                                                                                                                                                                                                                                                                      |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                           |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                 |
| type       | arm                                                                                                                                                                                                                                                                                                                         |
| region     |                                                                                                                                                                                                                                                                                                                             |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-advanced-networking-aad/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_6
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-00101-ARM
Title: Managed Azure AD RBAC for AKS cluster should be enabled\
Test Result: **failed**\
Description : Azure Kubernetes Service (AKS) can be configured to use Azure Active Directory (AD) for user authentication. In this configuration, you sign in to an AKS cluster using an Azure AD authentication token. You can also configure Kubernetes role-based access control (Kubernetes RBAC) to limit access to cluster resources based a user's identity or group membership. Visit https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac for details.\

#### Test Details
- eval: data.rule.aks_aad_azure_rbac
- id : PR-AZR-00101-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                                           |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT591                                                                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                                                                            |
| reference  | master                                                                                                                                                                                                                                                                                                                                |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                                     |
| collection | armtemplate                                                                                                                                                                                                                                                                                                                           |
| type       | arm                                                                                                                                                                                                                                                                                                                                   |
| region     |                                                                                                                                                                                                                                                                                                                                       |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.network/aks-application-gateway-ingress-controller/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_6
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-00101-ARM
Title: Managed Azure AD RBAC for AKS cluster should be enabled\
Test Result: **failed**\
Description : Azure Kubernetes Service (AKS) can be configured to use Azure Active Directory (AD) for user authentication. In this configuration, you sign in to an AKS cluster using an Azure AD authentication token. You can also configure Kubernetes role-based access control (Kubernetes RBAC) to limit access to cluster resources based a user's identity or group membership. Visit https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac for details.\

#### Test Details
- eval: data.rule.aks_aad_azure_rbac
- id : PR-AZR-00101-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                   |
|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT866                                                                                                                                                                                                                                      |
| structure  | filesystem                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_6
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-00101-ARM
Title: Managed Azure AD RBAC for AKS cluster should be enabled\
Test Result: **failed**\
Description : Azure Kubernetes Service (AKS) can be configured to use Azure Active Directory (AD) for user authentication. In this configuration, you sign in to an AKS cluster using an Azure AD authentication token. You can also configure Kubernetes role-based access control (Kubernetes RBAC) to limit access to cluster resources based a user's identity or group membership. Visit https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac for details.\

#### Test Details
- eval: data.rule.aks_aad_azure_rbac
- id : PR-AZR-00101-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                                             |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT867                                                                                                                                                                                                                                                                                                |
| structure  | filesystem                                                                                                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.kubernetes/aks-vmss-systemassigned-identity/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_6
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-00101-ARM
Title: Managed Azure AD RBAC for AKS cluster should be enabled\
Test Result: **failed**\
Description : Azure Kubernetes Service (AKS) can be configured to use Azure Active Directory (AD) for user authentication. In this configuration, you sign in to an AKS cluster using an Azure AD authentication token. You can also configure Kubernetes role-based access control (Kubernetes RBAC) to limit access to cluster resources based a user's identity or group membership. Visit https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac for details.\

#### Test Details
- eval: data.rule.aks_aad_azure_rbac
- id : PR-AZR-00101-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                             |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1148                                                                                                                                                                                                               |
| structure  | filesystem                                                                                                                                                                                                                              |
| reference  | master                                                                                                                                                                                                                                  |
| source     | gitConnectorArmMS                                                                                                                                                                                                                       |
| collection | armtemplate                                                                                                                                                                                                                             |
| type       | arm                                                                                                                                                                                                                                     |
| region     |                                                                                                                                                                                                                                         |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/demos/private-aks-cluster/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_6
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-00101-ARM
Title: Managed Azure AD RBAC for AKS cluster should be enabled\
Test Result: **failed**\
Description : Azure Kubernetes Service (AKS) can be configured to use Azure Active Directory (AD) for user authentication. In this configuration, you sign in to an AKS cluster using an Azure AD authentication token. You can also configure Kubernetes role-based access control (Kubernetes RBAC) to limit access to cluster resources based a user's identity or group membership. Visit https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac for details.\

#### Test Details
- eval: data.rule.aks_aad_azure_rbac
- id : PR-AZR-00101-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                         |
|:-----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1702                                                                                                                                                                                                                                                           |
| structure  | filesystem                                                                                                                                                                                                                                                                          |
| reference  | master                                                                                                                                                                                                                                                                              |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                   |
| collection | armtemplate                                                                                                                                                                                                                                                                         |
| type       | arm                                                                                                                                                                                                                                                                                 |
| region     |                                                                                                                                                                                                                                                                                     |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_6
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-00101-ARM
Title: Managed Azure AD RBAC for AKS cluster should be enabled\
Test Result: **failed**\
Description : Azure Kubernetes Service (AKS) can be configured to use Azure Active Directory (AD) for user authentication. In this configuration, you sign in to an AKS cluster using an Azure AD authentication token. You can also configure Kubernetes role-based access control (Kubernetes RBAC) to limit access to cluster resources based a user's identity or group membership. Visit https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac for details.\

#### Test Details
- eval: data.rule.aks_aad_azure_rbac
- id : PR-AZR-00101-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                            |
|:-----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1703                                                                                                                                                                                                                                                              |
| structure  | filesystem                                                                                                                                                                                                                                                                             |
| reference  | master                                                                                                                                                                                                                                                                                 |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                      |
| collection | armtemplate                                                                                                                                                                                                                                                                            |
| type       | arm                                                                                                                                                                                                                                                                                    |
| region     |                                                                                                                                                                                                                                                                                        |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/minio/minio-azure-gateway/azuredeploy.parameters.us.json'] |

- masterTestId: TEST_AKS_6
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------


### Test ID - PR-AZR-00101-ARM
Title: Managed Azure AD RBAC for AKS cluster should be enabled\
Test Result: **failed**\
Description : Azure Kubernetes Service (AKS) can be configured to use Azure Active Directory (AD) for user authentication. In this configuration, you sign in to an AKS cluster using an Azure AD authentication token. You can also configure Kubernetes role-based access control (Kubernetes RBAC) to limit access to cluster resources based a user's identity or group membership. Visit https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac for details.\

#### Test Details
- eval: data.rule.aks_aad_azure_rbac
- id : PR-AZR-00101-ARM

#### Snapshots
| Title      | Description                                                                                                                                                                                                                                                                                   |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id         | ARM_TEMPLATE_SNAPSHOT1796                                                                                                                                                                                                                                                                     |
| structure  | filesystem                                                                                                                                                                                                                                                                                    |
| reference  | master                                                                                                                                                                                                                                                                                        |
| source     | gitConnectorArmMS                                                                                                                                                                                                                                                                             |
| collection | armtemplate                                                                                                                                                                                                                                                                                   |
| type       | arm                                                                                                                                                                                                                                                                                           |
| region     |                                                                                                                                                                                                                                                                                               |
| paths      | ['https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.json', 'https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/jenkins/jenkins-cicd-container/azuredeploy.parameters.json'] |

- masterTestId: TEST_AKS_6
- masterSnapshotId: ['ARM_TEMPLATE_SNAPSHOT']
- type: rego
- rule: file(https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac/aks.rego)
- severity: Medium

tags
| Title      | Description   |
|:-----------|:--------------|
| cloud      | git           |
| compliance | []            |
| service    | ['arm']       |
----------------------------------------------------------------

