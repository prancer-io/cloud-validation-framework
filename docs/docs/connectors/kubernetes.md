# Kubernetes structure file

The **Kubernetes** connector allows you to inspect your **Kubernetes** cluster using their API. The connector is a wrapper around the **Kubernetes** ReST API.

Here is a sample of the Kubernetes structure file:

```json
{
    "filetype": "<file-type>",
    "type": "<type-of-structure>",
    "companyName": "<company-name>",
    "clusterName": "<cluster-name>",
    "clusterUrl": "<cluster-url>",
    "namespaces": [
        {
            "namespace": "<namesnpace>",
            "serviceAccounts": [
                {
                    "name": "<service-account-name>",
                    "secret":"<secret>"
                }
            ]
        }
    ]
}
```

| Key           |Value Description |
| ------------- |:-------------:   |
|filetype |structure|
|type|kubernetes|
|company-name|your company name|
|cluster-name|your cluster name|
|cluster-url|use url like this `https://<IP>:6443` or you can use domain|
|namespace|use namespace which we need to connect for getting data|
|service-account-name|the service account name which has access to namespace|
|secret|the token of secret|

sample file:

```json
{
    "filetype": "structure",
    "type": "kubernetes",
    "companyName": "Company Name",
    "clusterName": "prancer-prod-prod-eastus2-aksprod01",
    "clusterUrl": "https://prancer-kube:6443",
    "namespaces": [
        {
            "namespace": "default",
            "serviceAccounts": [
                {
                    "name": "prancer_ro",
                    "secret":"<someToken>"
                }
            ]
        }
    ]
}
```
