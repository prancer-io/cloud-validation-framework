
class BaseNodePull:
    def __init__(self, resource, **kwargs):
        self.resource = resource
        self.resource_type = ""

    def check_for_node_pull(self, resource_type):
        """ 
        check the resource type need to clone the child nodes or not
        """
        return self.resource