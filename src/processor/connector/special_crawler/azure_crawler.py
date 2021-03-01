from processor.helper.config.rundata_utils import get_from_currentdata, put_in_currentdata
from processor.connector.special_crawler.base_crawler import BaseCrawler
from processor.helper.httpapi.http_utils import http_get_request

class AzureCrawler(BaseCrawler):

    def __init__(self, resources, **kwargs):
        super().__init__(resources, **kwargs)
        self.token = kwargs.get("token")
        self.apiversions = kwargs.get("apiversions")
        self.subscription_id = kwargs.get("subscription_id")

        self.special_resource_types = {
            "Microsoft.Sql/servers/securityAlertPolicies" : self.crawl_server_security_alert_policies,
            "Microsoft.Sql/servers/auditingSettings" : self.crawl_server_audit_settings,
            "Microsoft.Authorization/roleDefinitions": self.crawl_role_definitions
        }
    
    def check_for_special_crawl(self, resource_type):
        """ 
        check the resource type need special crawling or not. if it need special crawling then 
        it will process the special crawler and returns the updated resources
        """
        if resource_type in self.special_resource_types:
            crawl_function = self.special_resource_types.get(resource_type)
            crawl_function(resource_type)
        return self.resources
    
    def get_version_of_resource_type(self, resource_type):
        """Url version of the resource."""
        version = None
        if self.apiversions:
            if resource_type in self.apiversions:
                version = self.apiversions[resource_type]['version']
        return version
    
    def call_azure_api(self, url):
        hdrs = {
            'Authorization': 'Bearer %s' % self.token
        }
        status, data = http_get_request(url, hdrs, name='\tRESOURCE:')
        if status and isinstance(status, int) and status == 200:
            for resource in data.get("value", []):
                put_in_currentdata('resources', resource)
            self.resources += data.get("value", [])

    def crawl_server_security_alert_policies(self, resource_type):
        """
        crawl "Microsoft.Sql/servers/securityAlertPolicies" resource type
        """
        version = self.get_version_of_resource_type(resource_type)
        if version:
            for resource in self.resources:
                if resource.get("type") == "Microsoft.Sql/servers":
                    url = 'https://management.azure.com%s/%s?api-version=%s' % (resource.get("id"), "securityAlertPolicies", version)
                    self.call_azure_api(url)

    def crawl_server_audit_settings(self, resource_type):
        """
        crawl "Microsoft.Sql/servers/auditingSettings" resource type
        """
        version = self.get_version_of_resource_type(resource_type)
        if version:
            for resource in self.resources:
                if resource.get("type") == "Microsoft.Sql/servers":
                    url = 'https://management.azure.com%s/%s?api-version=%s' % (resource.get("id"), "auditingSettings", version)
                    self.call_azure_api(url)
    
    def crawl_role_definitions(self, resource_type):
        """
        crawl "Microsoft.Authorization/roleDefinitions" resource type
        """
        version = self.get_version_of_resource_type(resource_type)
        if version:
            url = 'https://management.azure.com/subscriptions/%s/providers/%s?api-version=%s' % (self.subscription_id, resource_type, version)
            self.call_azure_api(url)