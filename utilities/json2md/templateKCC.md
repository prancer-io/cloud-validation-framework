# Automated Vulnerability Scan result and Static Code Analysis for Kubernetes Config Connector (KCC) files

Source Repository: https://github.com/GoogleCloudPlatform/k8s-config-connector/
Compliance help: https://cloud.google.com/security-command-center/docs/concepts-vulnerabilities-findings

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