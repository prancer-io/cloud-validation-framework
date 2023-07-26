from processor.helper.config.rundata_utils import get_from_currentdata, put_in_currentdata
from processor.connector.special_crawler.base_crawler import BaseCrawler
from processor.helper.httpapi.http_utils import http_get_request
from processor.helper.httpapi.restapi_azure import get_access_token, GRAPH_TOKEN

class AzureCrawler(BaseCrawler):

    def __init__(self, resources, **kwargs):
        super().__init__(resources, **kwargs)
        self.token = kwargs.get("token")
        self.apiversions = kwargs.get("apiversions")
        self.subscription_id = kwargs.get("subscription_id")
        self.version = kwargs.get("version")
        self.scope = kwargs.get("scope")

        self.special_node_type_crwler = [
            "microsoft.graph.userRegistrationDetails",
            "microsoft.graph.identitySecurityDefaultsEnforcementPolicy",
            "microsoft.graph.authorizationPolicy"
        ]

        self.special_resource_types = {
            "Microsoft.Authorization/roleDefinitions": self.crawl_role_definitions,
            "Microsoft.Authorization/roleAssignments": self.crawl_role_assignments,
            "Microsoft.Storage/storageAccounts/blobServices/containers": self.crawl_blobservice_containers,
            "microsoft.graph.userRegistrationDetails": self.crawl_user_registration_details,
            "microsoft.graph.identitySecurityDefaultsEnforcementPolicy": self.crawl_default_enforcement_policy,
            "microsoft.graph.authorizationPolicy": self.crawl_authorization_policy,
        }
    
    def check_for_special_crawl(self, resource_type):
        """ 
        check the resource type need special crawling or not. if it need special crawling then 
        it will process the special crawler and returns the updated resources
        """
        if resource_type in self.special_resource_types:
            crawl_function = self.special_resource_types.get(resource_type)
            crawl_function(resource_type)
        else:
            self.crawl_child_resources(resource_type)
        return self.resources
    
    def get_version_of_resource_type(self, resource_type):
        """Url version of the resource."""
        if not self.version and self.apiversions:
            if resource_type in self.apiversions:
                self.version = self.apiversions[resource_type]['version']
        return self.version
    
    def call_azure_api(self, url):
        hdrs = {
            'Authorization': 'Bearer %s' % self.token
        }
        status, data = http_get_request(url, hdrs, name='\tRESOURCE:')
        if status and isinstance(status, int) and status == 200:
            for resource in data.get("value", []):
                put_in_currentdata('resources', resource)
            self.resources += data.get("value", [])
            
    def crawl_child_resources(self, child_resource_type):
        """
        crawl child resources
        """
        version = self.get_version_of_resource_type(child_resource_type)
        child_resource_type_list = child_resource_type.split("/")
        if len(child_resource_type_list) > 2:
            child_resource = "/".join(child_resource_type_list[2:])
            main_resource = "/".join(child_resource_type_list[:2])
            if version:
                for resource in self.resources:
                    if resource.get("type") == main_resource:
                        url = 'https://management.azure.com%s/%s?api-version=%s' % (resource.get("id"), child_resource, version)
                        self.call_azure_api(url)
        return self.resources
    
    def crawl_role_definitions(self, resource_type):
        """
        crawl "Microsoft.Authorization/roleDefinitions" resource type
        """
        version = self.get_version_of_resource_type(resource_type)
        if version:
            self.scope = self.scope if self.scope else "subscriptions/%s" % self.subscription_id
            url = 'https://management.azure.com/%s/providers/%s?api-version=%s' % (self.scope, resource_type, version)
            self.call_azure_api(url)
    
    def crawl_role_assignments(self, resource_type):
        """
        crawl "Microsoft.Authorization/roleAssignments" resource type
        """
        version = self.get_version_of_resource_type(resource_type)
        if version:
            self.scope = self.scope if self.scope else "subscriptions/%s" % self.subscription_id
            url = 'https://management.azure.com/%s/providers/%s?api-version=%s' % (self.scope, resource_type, version)
            self.call_azure_api(url)

    def crawl_blobservice_containers(self, resource_type):
        """
        crawl "Microsoft.Storage/storageAccounts/blobServices/containers" resource type
        """        
        version = self.get_version_of_resource_type(resource_type)
        if version:
            for resource in self.resources:
                if resource['type'] == "Microsoft.Storage/storageAccounts":
                    hdrs = {
                        'Authorization': 'Bearer %s' % self.token
                    }
                    url = 'https://management.azure.com%s/blobServices/default/containers?api-version=%s' % (resource['id'], version)
                    status, data = http_get_request(url, hdrs, name='\tRESOURCE:')
                    if status and isinstance(status, int) and status == 200:
                        for resource in data.get("value", []):
                            put_in_currentdata('resources', resource)
                        self.resources += data.get("value", [])

    def crawl_user_registration_details(self, resource_type):
        """
        crawl "microsoft.graph.userRegistrationDetails" resource type
        """        
        version = self.get_version_of_resource_type(resource_type)
        graph_token = get_access_token("https://graph.microsoft.com", token_key=GRAPH_TOKEN)
        if version:
            hdrs = {
                'Authorization': 'Bearer %s' % graph_token
            }
            url = 'https://graph.microsoft.com/%s/reports/authenticationMethods/userRegistrationDetails' % version
            status, data = http_get_request(url, hdrs, name='\tRESOURCE:')
            self.resources = []
            if status and isinstance(status, int) and status == 200:
                for resource in data.get("value", []):
                    resource["id"] = "/%s/reports/authenticationMethods/userRegistrationDetails/%s" % (
                        version, resource.get("id", ""))
                self.resources = data.get("value", [])
    
    def crawl_default_enforcement_policy(self, resource_type):
        """
        crawl "microsoft.graph.identitySecurityDefaultsEnforcementPolicy" resource type
        """        
        version = self.get_version_of_resource_type(resource_type)
        graph_token = get_access_token("https://graph.microsoft.com", token_key=GRAPH_TOKEN)
        if version:
            hdrs = {
                'Authorization': 'Bearer %s' % graph_token
            }
            url = 'https://graph.microsoft.com/%s/policies/identitySecurityDefaultsEnforcementPolicy' % version
            status, resource = http_get_request(url, hdrs, name='\tRESOURCE:')
            self.resources = []
            if status and isinstance(status, int) and status == 200:
                resource["id"] = "/%s/policies/identitySecurityDefaultsEnforcementPolicy" % (version)
                self.resources = [resource]
    
    def crawl_authorization_policy(self, resource_type):
        """
        crawl "microsoft.graph.authorizationPolicy" resource type
        """        
        version = self.get_version_of_resource_type(resource_type)
        graph_token = get_access_token("https://graph.microsoft.com", token_key=GRAPH_TOKEN)
        if version:
            hdrs = {
                'Authorization': 'Bearer %s' % graph_token
            }
            url = 'https://graph.microsoft.com/%s/policies/authorizationPolicy' % version
            status, resource = http_get_request(url, hdrs, name='\tRESOURCE:')
            self.resources = []
            if status and isinstance(status, int) and status == 200:
                resource["id"] = "/%s/policies/authorizationPolicy" % (version)
                self.resources = [resource]