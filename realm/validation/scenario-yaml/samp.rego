package opa.result

default check_name = false
check_name  {
    resource := data.metadata.name
    resource == "myapp-pod"
}
