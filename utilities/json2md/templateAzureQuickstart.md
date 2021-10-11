# Automated Vulnerability Scan result and Static Code Analysis for Azure Quickstart files

## Azure Kubernetes Services (AKS)

Source Repository: https://github.com/Azure/azure-quickstart-templates

Scan engine: **Prancer Framework** (https://www.prancer.io)

Compliance Database: https://github.com/prancer-io/prancer-compliance-test/tree/master/azure/iac

## Compliance run Meta Data
{{ data.meta }}

## Results
{% for item in data.results %}
### Test ID - {{ item.id }}
Title: {{ item.title }}\
Test Result: **{{ item.result }}**\
Description : {{ item.description }}\

#### Test Details
- eval: {{ item.eval }}
- id : {{ item.id }}

#### Snapshots
{{ item.snapshots }}

- masterTestId: {{ item.masterTestId }}
- masterSnapshotId: {{ item.masterSnapshotId }}
- type: {{ item.type }}
- rule: {{ item.rule }}
- severity: {{ item.severity }}

tags
{{ item.tags }}
----------------------------------------------------------------

{% endfor %}