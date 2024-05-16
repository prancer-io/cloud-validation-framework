from processor.logging.log_handler import getlogger
from processor.connector.special_crawler.base_crawler import BaseCrawler
from processor.helper.xml.xml_utils import xml_to_json
import requests
import zipfile
import io
import re

logger = getlogger()

class GoogleCrawler(BaseCrawler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.response_data = None
        self.status = False
        self.project_id = kwargs.get("project_id")
        self.access_token = kwargs.get("access_token")
        self.special_resource_types = {
            "apigee/organizations.apis.deployments.list" : self.crawl_apigee_deployments,
        }
        self.data_processing_resource_types = {
            "apigee/organizations.apis.revisions.get" : self.process_apigee_version_data,
        }

    def get_header(self):
        return {
            "Authorization" : ("Bearer %s" % self.access_token)
        }

    def check_for_special_crawl(self, resource_type):
        """ 
        check the resource type need special crawling or not. if it need special crawling then 
        it will process the special crawler and returns the updated resources
        """
        if resource_type in self.special_resource_types:
            self.status = True
            crawl_function = self.special_resource_types.get(resource_type)
            self.response_data = crawl_function()

        return self.status, self.response_data
    
    def check_for_data_process(self, path, resource_type):
        """ 
        check the resource type need processing on the data. if it need processing then 
        it will process it and returns the updated resource data
        """
        self.path = path
        if resource_type in self.data_processing_resource_types:
            self.status = True
            process_data_function = self.data_processing_resource_types.get(resource_type)
            self.response_data = process_data_function()

        return self.status, self.response_data

    def policy_xml_to_json(self, xml_contnet):
        json_content = xml_to_json(xml_contnet)
        json_data = {}
        for key, value in json_content.items():
            json_data["name"] = key
            json_data["data"] = value
        return json_data

    def process_apigee_version_data(self):
        response_data = {}
        match = re.search(r"organizations/([^/]+)/apis/([^/]+)/revisions/([^/]+)", self.path)
        if match:
            organization = match.group(1)
            api = match.group(2)
            revision = match.group(3)
        else:
            logger.error("Invalid path for process apigee version")
            return

        request_url = f"https://apigee.googleapis.com/{self.path}?format=bundle"
        response = requests.get(url=request_url, headers=self.get_header())

        if response.status_code == 200:
            bundle_zip = io.BytesIO(response.content)
            policies_json = []
            pattern = r'.+/policies/[^/]+\.xml'
            with zipfile.ZipFile(bundle_zip, 'r') as zip_ref:
                for file in zip_ref.filelist:
                    matches = re.findall(pattern, file.filename)
                    if matches:
                        with zip_ref.open(file.filename) as xml_file:
                            xml_content = xml_file.read()
                            json_content = self.policy_xml_to_json(xml_content)
                            policies_json.append(json_content)
                        
            response_data = {
                "organization" : organization,
                "api" : api,
                "revision" : revision,
                "policies" : policies_json
            }
            return response_data
        else:
            logger.error(f"Failed to retrieve API bundle. Status code: {response.status_code}, Error: {response.content}")
            return response_data

    def get_apigee_organizations(self):
        organizations = []
        request_url = "https://apigee.googleapis.com/v1/organizations"
        response = requests.get(url=request_url, headers=self.get_header())
        if response.status_code != 200:
            logger.error(f"Failed to get the organization list. Status code: {response.status_code}, Error: {response.content}")
            return organizations

        data = response.json()
        organizations = data.get("organizations", [])
        return organizations
    
    def get_apigee_apis(self, organization):
        apis = []
        request_url = f"https://apigee.googleapis.com/v1/organizations/{organization}/apis"
        response = requests.get(url=request_url, headers=self.get_header())
        if response.status_code != 200:
            logger.error(f"Failed to get the apigee apis. Status code: {response.status_code}, Error: {response.content}")
            return apis

        data = response.json()
        apis = data.get("proxies", [])
        return apis
    
    def get_apigee_deployments(self, organization, api):
        deployments = []
        request_url = f"https://apigee.googleapis.com/v1/organizations/{organization}/apis/{api}/deployments"
        response = requests.get(url=request_url, headers=self.get_header())
        if response.status_code != 200:
            logger.error(f"Failed to get the apigee deployments. Status code: {response.status_code}, Error: {response.content}")
            return deployments

        data = response.json()
        deployments = data.get("deployments", [])
        return deployments

    def crawl_apigee_deployments(self):
        """
        crawl "apigee/organizations.apis.deployments.list" resource type
        """
        deployment_list = []
        organizations = self.get_apigee_organizations()        
        for organization in organizations:
            if organization.get("projectId") != self.project_id:
                continue
            organization_name = organization.get("organization")
            apigee_apis = self.get_apigee_apis(organization_name)            
            for api in apigee_apis:
                api_name = api.get("name")
                deployments = self.get_apigee_deployments(organization_name, api_name)
                for deployment in deployments:
                    revision = deployment.get("revision")
                    deployment["selfLink"] = f"/organizations/{organization_name}/apis/{api_name}/revisions/{revision}"
                    deployment_list.append(deployment)
        response_data = {
            "items" : deployment_list
        }
        return response_data
                    

        