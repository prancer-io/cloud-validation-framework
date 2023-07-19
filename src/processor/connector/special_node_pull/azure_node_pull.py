from processor.connector.special_node_pull.base_node_pull import BaseNodePull
from processor.helper.httpapi.http_utils import http_get_request

class AzureNodePull(BaseNodePull):
    
    def __init__(self, resources, **kwargs):
        super().__init__(resources, **kwargs)
        self.token = kwargs.get("token")
        self.apiversions = kwargs.get("apiversions")

        self.special_resource_types = {
            "Microsoft.Authorization/roleAssignments": self.pull_role_assignments,
        }
    
    def get_version_of_resource_type(self, resource_type):
        """Url version of the resource."""
        if self.apiversions:
            if resource_type in self.apiversions:
                self.version = self.apiversions[resource_type]['version']
        return self.version
    
    def check_for_node_pull(self, resource_type):
        if resource_type in self.special_resource_types:
            pull_function = self.special_resource_types.get(resource_type)
            pull_function()
        return self.resource
    
    def call_azure_api(self, url):
        hdrs = {
            'Authorization': 'Bearer %s' % self.token
        }
        status, data = http_get_request(url, hdrs, name='\tRESOURCE:')
        if status and isinstance(status, int) and status == 200:
            self.resource["roleDefinition"] = data
    
    def pull_role_assignments(self):
        """
        pull "Microsoft.Authorization/roleAssignments" resource type
        """
        role_definition_id = self.resource.get("properties", {}).get("roleDefinitionId")
        version = self.get_version_of_resource_type("Microsoft.Authorization/roleDefinitions")
        if version and role_definition_id:
            url = 'https://management.azure.com%s?api-version=%s' % (role_definition_id, version)
            self.call_azure_api(url)