**Prancer Enterprise APIs**
===

Authentication APIs

| API | Description |
|------------|-------------|
| [Login API](authentication.md#login-api) |  API for authenticate user by email and password. |
| [Validate Access Token](authentication.md#validate-access-token) |  API for authenticate user by access token. |
| [Refresh Token](authentication.md#refresh-token) |  Refresh the expired JWT bearer token. |
| [Logout User](authentication.md#logout-api) |  Logout user. |


Collection APIs

| API | Description |
|------------|-------------|
| [Collection create](collection.md#collection-create) |  Create a new collection. |
| [Collection get](collection.md#collection-get) |  Populate list of collections. |
| [Collection exist](collection.md#collection-exists) | Check collection exist or not. |
| [Database collections](collection.md#database-collection-get) | Database collections in which the actual cloud/IaC snapshot JSON is stored. |
| [Get collection Config Items](collection.md#get-collection-config-items) | Get Collection configuration files like masterSnapshot, masterTest, Connectors etc. |
| [Update collection Config Items](collection.md#update-collection-config-items) | Update Collection configuration files like masterSnapshot, masterTest, Connectors etc. |

Compliance APIs

| API | Description |
|------------|-------------|
| [Run compliance](compliance.md#compliance-run-compliance) | Run compliance on a specific collection. |
| [Run crawler](compliance.md#compliance-run-crawler) | Run crawler on a specific collection. |
| [Schedule a compliance](compliance.md#compliance-add-schedulers) | Schedule a compliance to run automatically. |
| [Update a scheduler](compliance.md#compliance-update-schedulers) | Update a scheduled compliance job. |
| [Get scheduled compliances](compliance.md#compliance-get-scheduler-list) | Get the list of scheduled compliance. |
| [Get a scheduled compliance](compliance.md#compliance-get-a-scheduler) | Get a scheduled compliance. |
| [Delete a scheduler](compliance.md#compliance-delete-scheduler) | Delete a scheduled compliance. |

Configuration APIs

| API | Description |
|------------|-------------|
| [Collection configuration get](config.md#collection-config-get) | Get the configuration of specific collection. |
| [Collection configuration save](config.md#collection-config-create-or-update) | Save or update the configuration of specific collection. |
| [Global configuration get](config.md#configuration-get) | Get the global configuration of system. |
| [Global configuration update](config.md#configuration-update) | Update the global configuration of system. |

Connector APIs

| API | Description |
|------------|-------------|
| [Connector - get](connector.md#connector-get) | Populate the list of connectors. |

Dashboard APIs

| API | Description |
|------------|-------------|
| [Get dashboard components](dashboard.md#dashboard-get-components) | Populate dashboard components. |
| [Get component stats](dashboard.md#dashboard-stats) | Get stats of a dashboard component. |
| [Create dashboard component](dashboard.md#dashboard-create-component) | Create a dashboard componenet |
| [Delete dashboard component](dashboard.md#dashboard-delete-component) | Delete a dashboard component. |

Policy APIs

| API | Description |
|------------|-------------|
| [Policy filter](policy.md#policy-filter) | Populate the list of policies of a collection. |
| [Get policy rego](policy.md#get-policy-rego) | Get details of a rego file. |
| [Save Policy](policy.md#save-policy) | Save a policy |
| [Policy dashboard](policy.md#policy-dashboard) | Get the dashboard stats of a policy. |

Remediation APIs

| API | Description |
|------------|-------------|
| [Run Remediation](remediation.md#remediation-run) | Run remediation to autofix the issue in a Cloud/IaC resource.|


Report APIs

| API | Description |
|------------|-------------|
| [Search Report](reports.md#report-search) | Search the compliance report of a specific type of collection. |

Resources APIs

| API | Description |
|------------|-------------|
| [Search resources](resources.md#resources-search) | Search resources of a specific collection. |
| [Get resource dashboard](resources.md#resources-dashboard) | Get dashboard stats of a resource. |
| [Get resource snapshot](resources.md#resources-get) | Get snapshot JSON of a Cloud/IaC resource. |
| [Get resource testcase details](resources.md#resource-testcase-detail) | Get full details of a single testcase. |
| [Get resource configuration drift](resources.md#resource-configuration-drift-detail) | Get details of a resource configuration drift. |
| [Save resource filter](resources.md#resource-filter-save) | Save filtered parameters of search resources. |
| [Get resource filters](resources.md#resource-filter-get) | Get the list of saved resource filters. |
| [Delete resource filter](resources.md#resource-filter-delete) | Delete a resource filter. |
| [Query resources](resources.md#resource-query) | Run the mongodb query to filter the specific resources. |
| [Resource query sample](resources.md#resource-query-sample) | List of sample queries to filter the resources. |
| [Resource exclusion create](resources.md#resource-exclusion-create) | Exclude resources, so no compliance will run on that resources. |
| [Get resource exclusions](resources.md#resource-exclusion-get) | Get the list of excluded resources. |
| [Delete resource exclusions](resources.md#resource-exclusion-delete) | Remove the exclusion on resources. |

Tags APIs

| API | Description |
|------------|-------------|
| [Default tags](tags.md#default-tags) | Get the list of predefined compliance tags. |

Users APIs

| API | Description |
|------------|-------------|
| [Get users](users.md#users-get) | Get the list of users. |
| [Update user's tour status](users.md#users-update-tour-status) | Update the status of tour guidance in website. |

Permissions APIs

| API | Description |
|------------|-------------|
| [Get permissions](permissions.md#permissions-get) | Get list of available permissions. |
| [Create permission role](permissions.md#permissions-role-create) | Create a user role based on permissions. |
| [Get permission role](permissions.md#permissions-role-get) | Get the list of permission roles. |
| [Delete permission role](permissions.md#permissions-role-delete) | Delete a permission role. |

Vault APIs

| API | Description |
|------------|-------------|
| [Vault get](vault.md#vault-get) | Get specific value from the vault. |
| [Vault save](vault.md#vault-save-key) | Save new secret into the vault. |
| [Vault update](vault.md#vault-update) | Update secret value into the vault. |
| [Vault delete](vault.md#vault-delete-key) | Delete a key from the vault. |

Webhook APIs

| API | Description |
|------------|-------------|
| [Save webhook config](webhook.md#webhook-save) | Enable or Disable webhook auto-fix config for a collection. |

Wizard APIs

| API | Description |
|------------|-------------|
| [Google Wizard Redirection](wizard.md#google-wizard-redirection-api) | API for get redirect link for google oauth app. |
| [Google Wizard Providers](wizard.md#google-wizard-provider-api) | Get the list of google projects after authenticate google. |
| [Github Wizard Redirection](wizard.md#github-wizard-redirection-api) | API for get redirect link for github oauth app. |
| [Github Wizard Providers](wizard.md#github-wizard-provider-api) | Get the list of github repositories using gihub oauth app. |
| [Azure Wizard Providers](wizard.md#azure-wizard-provider-api) | Get the list of azure subscriptions. |
| [AWS Wizard Providers](wizard.md#aws-wizard-provider-api) | Get the list of AWS accounts. |
| [Google Wizard create](wizard.md#google-wizard-create-api) | Create google collection for a project. |
| [Kubernetes Wizard create](wizard.md#kubernetes-wizard-create-api) | API to create kubernetes collection for a namespace. |
| [Kubernetes Wizard Providers](wizard.md#kubernetes-wizard-provider-api) | Get the kubernetes namespaces in the api server. |
| [Create Wizard](wizard.md#wizard-creation-creation-of-a-wizard-for-cloud-provider) | API to create a wizard for the cloud provider. |
| [Wizard Status API](wizard.md#wizard-status-api) | API to get status of wizard creation. |
