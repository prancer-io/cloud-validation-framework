## HelmChart master snapshot configuration 
HelmChart is only available for master snapshot configuration file. because when helm binary process helm chart template it will go to generate one multiple yaml file which is support by prancer.
prancer will  minify the generated multiple yaml file which created by helm binary to multiple single yaml file.

Here is the master snapshot configuration file template for helm chart :
```
{
    "fileType": "masterSnapshot",
    "snapshots": [
        {
            "source": "<structure name>",
            "nodes": [
                {
                    "masterSnapshotId": "<master snapshot id>",
                    "type": "helmChart",
                    "collection": "<db collection>",
                    "paths":[
                        <helm folder path>  
                    ] 
                }
            ]
        }
    ]
}


```   

sample file :

```
{
    "fileType": "masterSnapshot",
    "snapshots": [
        {
            "source": "test-gitConnector",
            "nodes": [
                {
                    "masterSnapshotId": "helm_",
                    "type": "helmChart",
                    "collection": "multiple",
                    "paths":[
                        "helm/"  
                    ] 
                }
            ]
        }
    ]
}
```