## Kubernetes structure file 
Here is sample of kubernetes structure file:
```
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
|cluster-url|use url like this https://<ip>:6443 or you can use domain|
|namespace|use namespace which we need to connect for getting data|
|service-account-name|the service account name which has access to namespace|
|secret|the token of secret|


sample file:
```
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
                    "secret":"eyJhbGciOiJSUzI1NiIsImtpZCI6ImpvS2RmQ3dfZ05URGY4TjRSZElvMno1OU9L"
                }
            ]
        }
    ]
}
```
