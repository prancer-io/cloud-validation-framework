from processor.connector.special_node_pull.base_node_pull import BaseNodePull
from processor.helper.httpapi.http_utils import http_get_request

NODE_PULL_URL = {
    "microsoft.graph.userRegistrationDetails" : "graph.microsoft.com",
    "microsoft.graph.identitySecurityDefaultsEnforcementPolicy" : "graph.microsoft.com",
    "microsoft.graph.authorizationPolicy" : "graph.microsoft.com",
}

class AzureNodePull(BaseNodePull):
    
    def __init__(self, resource, **kwargs):
        super().__init__(resource, **kwargs)
        self.token = kwargs.get("token")
        self.apiversions = kwargs.get("apiversions")

        self.special_resource_types = {
            "Microsoft.Authorization/roleAssignments": self.pull_role_assignments,
            "microsoft.graph.userRegistrationDetails" : self.pull_user_registration,
            "microsoft.graph.identitySecurityDefaultsEnforcementPolicy" : self.pull_default_enforcement_policy,
            "microsoft.graph.authorizationPolicy" : self.pull_authorization_policy,
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
            return data
        return {}
    
    def pull_role_assignments(self):
        """
        pull "Microsoft.Authorization/roleAssignments" resource type
        """
        role_definition_id = self.resource.get("properties", {}).get("roleDefinitionId")
        version = self.get_version_of_resource_type("Microsoft.Authorization/roleDefinitions")
        if version and role_definition_id:
            url = 'https://management.azure.com%s?api-version=%s' % (role_definition_id, version)
            data = self.call_azure_api(url)
            self.resource["properties"]["roleDefinition"] = data
    
    def pull_user_registration(self):
        """
        pull "microsoft.graph.userRegistrationDetails" resource type
        """
        resource = {}
        resource["type"] = "microsoft.graph.userRegistrationDetails"
        resource["properties"] = self.resource
        resource["name"] = resource["properties"].get("id")
        self.resource = resource
    
    def pull_default_enforcement_policy(self):
        """
        pull "microsoft.graph.identitySecurityDefaultsEnforcementPolicy" resource type
        """
        resource = {}
        resource["type"] = "microsoft.graph.identitySecurityDefaultsEnforcementPolicy"
        resource["properties"] = self.resource
        resource["name"] = resource["properties"].get("id")
        self.resource = resource
    
    def pull_authorization_policy(self):
        """
        pull "microsoft.graph.authorizationPolicy" resource type
        """
        resource = {}
        resource["type"] = "microsoft.graph.authorizationPolicy"
        resource["properties"] = self.resource
        resource["name"] = resource["properties"].get("id")
        self.resource = resource