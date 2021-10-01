import json
import re
import os
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import json_from_file, get_field_value
from processor.template_processor.base.base_template_processor import TemplateProcessor
from processor.templates.azure.azure_parser import AzureTemplateParser
from processor.helper.file.file_utils import exists_file
from processor.helper.config.config_utils import config_value, get_test_json_dir, framework_dir
from cfn_flip import flip, to_yaml, to_json

logger = getlogger()

class AzureTemplateProcessor(TemplateProcessor):
    """
    Base Template Processor for process template 
    """

    def __init__(self, node, **kwargs):
        super().__init__(node, tosave=False, **kwargs)

    def invoke_az_cli(self, args_str):
        """ 
        Invoke azure cli command
        """
        try:
            from azure.cli.core import get_default_cli
        except:
            logger.error("dependancy `azure-cli` is not installed! Install the dependancy and try it again.")
            return {"error" : "dependancy `azure-cli` is not installed! Install the dependancy and try it again."}

        login_user = os.environ.get('AD_LOGIN_USER', None)
        login_password = os.environ.get('AD_LOGIN_PASSWORD', None)

        if not login_user or not login_password:
            logger.error("`loginUser` or `loginPassword` field is not set in environment")
            return {"error" : "`loginUser` or `loginPassword` field is not set in environment"}
            
        azexe = os.environ.get('AZEXE', 'az')
        os.system(azexe + " login -u " + login_user + " -p " + login_password)

        args = args_str.split()
        cli = get_default_cli()
        cli.invoke(args)
        logger.info('Invoked Azure CLI command :: az %s' % args)
        if cli.result.result:
            os.system(azexe + " logout")
            return cli.result.result
        elif cli.result.error:
            raise cli.result.error
        return True

    def is_parameter_file(self, file_path):
        """
        check for valid parameter file for parse cloudformation template
        """
        if len(file_path.split(".")) > 0 and file_path.split(".")[-1] == "json":
            json_data = json_from_file(file_path)
            if json_data and '$schema' in json_data and json_data['$schema']:
                match =  re.match(r'.*/deploymentParameters.json#', json_data['$schema'], re.I)
                return True if match else False
        return False

    def is_template_file(self, file_path):
        """
        check for valid template file for parse arm template
        """
        if len(file_path.split(".")) > 0 and file_path.split(".")[-1] == "json":
            json_data = json_from_file(file_path)
            if json_data and '$schema' in json_data and json_data['$schema']:
                match =  re.match(r'.*/deploymentTemplate.json#$', json_data['$schema'], re.I)
                return True if match else False
        return False

    def process_template(self, paths):
        """
        process the files stored at specified paths and returns the template
        """
        location = get_field_value(self.node, 'location')
        azure_cli_flag = config_value("AZURE", "azureCli")

        template_json = None
        if paths and isinstance(paths, list):
            template_file_path = ""
            deployment_file_path = ""

            if azure_cli_flag and azure_cli_flag == "true" and not location:
                logger.error("Invalid json : 'location' field is required in node")
                return template_json
                
            for json_file in paths:
                json_file = '%s.json' % json_file if json_file and not \
                    json_file.endswith('.json') else json_file
                json_file_path = '%s/%s' % (self.dir_path, json_file)
                logger.info("Fetching data : %s ", json_file)
                json_data = json_from_file(json_file_path)
                if not json_data:
                    logger.error("Invalid template file path %s, or file does not contains the valid json format." % json_file)
                    return template_json
                elif "$schema" not in json_data:
                    logger.error(
                        "Invalid json : does not contains '$schema' field in json.")
                    return template_json
                else:
                    if "deploymentTemplate.json" in json_data['$schema'].split("/")[-1]:
                        template_file_path = json_file_path
                    elif "deploymentParameters.json" in json_data['$schema'].split("/")[-1]:
                        deployment_file_path = json_file_path
                    else:
                        logger.error("Invalid json : $schema does not contains the correct value")
            
            if template_file_path:
                if azure_cli_flag and azure_cli_flag == "true":
                    if deployment_file_path:
                        template_json = self.invoke_az_cli("deployment validate --location " + location +
                            " --template-file " + template_file_path
                            + " --parameters @" + deployment_file_path)
                    else:
                        template_json = self.invoke_az_cli("deployment validate --location " + location +
                            " --template-file " + template_file_path)
                else:
                    try:
                        self.template_files = [template_file_path]
                        self.parameter_files = [deployment_file_path] if deployment_file_path else []
                        
                        azure_template_parser = AzureTemplateParser(template_file_path, parameter_file=self.parameter_files)
                        template_json = azure_template_parser.parse()
                        self.contentType = azure_template_parser.contentType
                        self.resource_types = azure_template_parser.resource_types
                    except:
                        template_json = None
        return template_json