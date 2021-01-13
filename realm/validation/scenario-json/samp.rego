package oparule

default check_name = false
check_name  {
    resource := input.metadata.name
    resource == "myapp-pod"
}
