## Kubernetes snapshot configuration

We have to setup snapshot configuration file for getting snapshot from kubernetes cluster information.
Here is the snapshot configuration file template for kubernetes post deployment:

```json
{
    "fileType": "<file-type>",
    "snapshots": [
        {
            "source": "<structure-file>",
            "serviceAccount": "<service-account>",
            "namespace": "<namespace>",
            "nodes": [
                {
                    "snapshotId": "<snapshotId>",
                    "type": "<type>",
                    "paths": [
                        "<path>"
                    ],
                    "collection": "<collection>"
                }
            ]
        }
    ]
}
```

| Key           |Value Description |
| ------------- |:-------------:   |
|file-type|snapshot|
|structure-file|is the name of structure file without json tag|
|service-account|the service account which has access to the snapshot namespace|
|namespace|the namespace which we want to get information from that|
|snapshotId|should be unique for each node|
|type|the type of kubernetes object we want to get snapshot from them|
|path|api path of that object should get snapshot|
|collection|mongo collection that we want to save snapshot if use **prancer** as full db mode|

example file :

```json
{
    "fileType": "snapshot",
    "snapshots": [
        {
            "source": "k8sConnector",
            "serviceAccount": "prancer_ro",
            "namespace": "default",
            "nodes": [
                {
                    "snapshotId": "K8SSNP_100",
                    "type": "pod",
                    "paths": [
                        "api/v1/namespaces/default/pods/backend-deployment-77dc8cc6b5-ldnl9"
                    ],
                    "collection": "pod",
                },
                {
                    "snapshotId": "K8SSNP_101",
                    "type": "pod",
                    "paths": [
                        "api/v1/namespaces/default/pods/backend-deployment-77dc8cc6b5-n6ttz"
                    ],
                    "collection": "pod",
                },
                {
                    "snapshotId": "K8SSNP_102",
                    "type": "deployment",
                    "paths": [
                        "apis/apps/v1/namespaces/default/deployments/backend-deployment"
                    ],
                    "collection": "deployments",
                }
            ]
        },
        {
            "source": "k8sConnector",
            "serviceAccount": "prancer_ro",
            "namespace": "default",
            "nodes": [
                {
                    "snapshotId": "K8SSNP_201",
                    "type": "pod",
                    "paths": [
                        "api/v1/namespaces/default/pods/backend-deployment-77dc8cc6b5-ldnl9"
                    ],
                    "collection": "pod",
                },
                {
                    "snapshotId": "K8SSNP_202",
                    "type": "replicaset",
                    "paths": [
                        "apis/apps/v1/namespaces/default/replicasets/backend-deployment-77dc8cc6b5"
                    ],
                    "collection": "replicaset"
                    
                }, 
                {
                    "snapshotId": "K8SSNP_203",
                    "type": "service",
                    "paths": [
                        "api/v1/namespaces/default/services/backend-lb-service"
                    ],
                    "collection": "replicaset"
                    
                },
                {
                    "snapshotId": "K8SSNP_204",
                    "type": "rolebinding",
                    "paths": [
                        "apis/rbac.authorization.k8s.io/v1beta1/namespaces/default/rolebindings/read-pods"
                    ],
                    "collection": "rolebinding"
                    
                }
            
            ]
        },{
            "source": "k8sConnector",
            "serviceAccount": "prancer_ro",
            "namespace": "network-test",
            "nodes":[
                {
                    "snapshotId": "K8SSNP_301",
                    "type": "networkpolicy",
                    "paths": [
                        "apis/networking.k8s.io/v1/namespaces/network-test/networkpolicies/test-network-policy"
                    ],
                    "collection": "network-test"
                    
                },
                {
                    "snapshotId": "K8SSNP_302",
                    "type": "podsecuritypolicy",
                    "paths": [
                        "apis/policy/v1beta1/podsecuritypolicies/calico-kube-controllers"
                    ],
                    "collection": "podSecurityPolicy"
                    
                }
                

            ]
        },{
            "source": "k8sConnector",
            "serviceAccount": "prancer_ro",
            "namespace": "backend-test",
            "nodes":[
                {
                    "snapshotId": "K8SSNP_401",
                    "type": "serviceaccount",
                    "paths": [
                        "api/v1/namespaces/backend-test/serviceaccounts/default"
                    ],
                    "collection": "backend-test"
                    
                }
            ]
        }

    ]
}
```

## Kubernetes master snapshot configuration 
We have to setup master snapshot configuration file for getting snapshot from kubernetes cluster information.
Here is the master snapshot configuration file template for kubernetes post deployment:

```json
{
    "fileType": "<file-type>",
    "snapshots": [
        {
            "source": "<structure-file>",
            "serviceAccount": "<service-account>",
            "namespace": [
                <namespace>
            ],
            "nodes": [
                {
                    
                    "masterSnapshotId": "<master-snapshot>",
                    "type": "<type>",
                    "paths": [
                        <paths>
                    ],
                    "collection": "<collection>"
                }
            ]
        } 
    ]
}
```

| Key           |Value Description |
| ------------- |:-------------:   |
|file-type|masterSnapshot|
|structure-file|is the name of structure file without json tag|
|service-account|the service account which has access to the snapshot namespace|
|namespace|the namespaces which we want to get information from them|
|masterSnapshotId|should be unique for each node|
|type|the type of kubernetes object we want to get snapshot from them|
|path|api path of that object should get snapshot|
|collection|mongo collection that we want to save snapshot if use **prancer** as full db mode|

example file:

```json
{
    "fileType": "masterSnapshot",
    "snapshots": [
        {
            "source": "k8sConnector",
            "serviceAccount": "prancer_ro",
            "namespace": [
                "default","backend-test"
            ],
            "nodes": [
                {
                    
                    "masterSnapshotId": "K8SSNP_POD_",
                    "type": "pod",
                    "paths": [
                        "api/v1"
                    ],
                    "collection": "pod"
                }
            ]
        },
        {
            "source": "k8sConnector",
            "serviceAccount": "prancer_ro",
            "namespace": [
                "default"
            ],
            "nodes": [
                {
                    
                    "masterSnapshotId": "K8SSNP_POD2_",
                    "type": "pod",
                    "paths": [
                        "api/v1"
                    ],
                    "collection": "pod"
                }
            ]
        },
        {
            "source": "k8sConnector",
            "serviceAccount": "prancer_ro",
            "namespace": [
                "default","backend-test"
            ],
            "nodes": [
                {
                    
                    "masterSnapshotId": "K8SSNP_SERVICEACC_",
                    "type": "serviceaccount",
                    "paths": [
                        "api/v1"
                    ],
                    "collection": "serviceaccount"
                }
            ]
        },
        {
            "source": "k8sConnector",
            "serviceAccount": "prancer_ro",
            "namespace": [
                "default","backend-test"
            ],
            "nodes": [
                {
                    
                    "masterSnapshotId": "K8SSNP_ROLEBINDING_",
                    "type": "rolebinding",
                    "paths": [
                        "api/v1"
                    ],
                    "collection": "rolebinding"
                }
            ]
        }
        
    ]
}
```
