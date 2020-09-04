"""
Define an interface for parsing azure template and its parameter files.
"""
import copy
import glob
import re
import os
from processor.logging.log_handler import getlogger
from processor.templates.base.template_parser import TemplateParser
from processor.helper.file.file_utils import exists_file, exists_dir

logger = getlogger()

class TerraformTemplateParser(TemplateParser):
    """
    Terraform Parser class for process terraform template
    """
    def __init__(self, template_file, tosave=False, **kwargs):
        super().__init__(template_file, tosave=False, **kwargs)
        self.imports = []
        self.schema_filter = {
            "var" : self.process_variable,
            "data" : self.process_data,
            "other" : self.process_other,
        }
        self.function_filter = {
            "length" : self.process_length,
        }
        self.default_gparams = kwargs.get("default_gparams", {})
        self.gdata = {}
        self.resource = {}
        self.functions = [{
            "key" : "length",
            "value" : "^(length[(](.*?)[)])*$"
        }]

    def is_template_file(self, file_path):
        """
        check for valid template file for parse terraform template
        """
        if len(file_path.split("/")) > 0 and file_path.split("/")[-1]=="main.tf":
            return True
        return False
    
    def is_parameter_file(self, file_path):
        """
        check for valid variable file for parse terraform template
        """
        if len(file_path.split(".")) > 0 and file_path.split(".")[-1] in ["tf", "tfvars"]:
            json_data = self.terraform_to_json(file_path)
            return True if (json_data and not "resource" in json_data) else False
        elif len(file_path.split(".")) > 1 and [ele for ele in [".tfvars.json", ".tf.json"] if(ele in file_path)]:
            json_data = self.json_data_from_file(file_path)
            return True if (json_data and not "resource" in json_data) else False
        return False

    def process_other(self, resource):
        """
        return default value of the variable if variable is set in terraform files
        """
        return self.parse_field_value(resource, self.resource)

    def process_variable(self, resource):
        """
        return default value of the variable if variable is set in terraform files
        """
        status, value = self.parse_field_value(resource, self.default_gparams)
        if not value:
            status, value = self.parse_field_value(resource, self.gparams)
        if not value:
            status, value = self.parse_field_value(resource, self.resource)
        return status, value
    
    def process_data(self, resource):
        """
        return value of the data if the given data is contains in terraform template file
        """
        return self.parse_field_value(resource, self.gdata)
    
    def parse_field_value(self, resource, from_data):
        resource_list = resource.split(".")
        value = copy.deepcopy(from_data)
        for resource in resource_list:
            # process variables like this: var.network_http["cidr"]
            pattern = re.compile(r'\[["|\'](.*?)["|\']\]')
            map_keys = re.findall(pattern, resource)
            if map_keys and len(resource.split("[")) > 1:
                value = value.get(resource.split("[")[0])
                for key in map_keys:
                    if not value or not isinstance(value, dict):
                        break
                    value = value.get(key)
                if not value:
                    break
                continue
            value = value.get(resource)
            if not value:
                break        
        if value:
            return True, value
        else:
            return False, value
    
    def get_template(self):
        """
        return the template json data
        """
        json_data = None
        if len(self.template_file.split(".")) > 0 and self.template_file.split(".")[-1]=="tf":
            json_data = self.terraform_to_json(self.template_file)
        elif len(self.template_file.split(".")) > 1 and ".tf.json" in self.template_file:
            json_data = self.json_data_from_file(self.template_file)
        return json_data
    
    def get_paramter_json_list(self):
        """
        process parameter files and returns parameters json list
        """
        parameter_json_list = []
        for parameter in self.parameter_file:
            if len(parameter.split(".")) > 0 and parameter.split(".")[-1] in ["tf", "tfvars"]:
                json_data = self.terraform_to_json(parameter)
                if json_data:
                    parameter_json_list.append({parameter.split(".")[-1] : json_data})
            elif len(parameter.split(".")) > 1 and [ele for ele in [".tfvars.json", ".tf.json"] if(ele in parameter)]:
                json_data = self.json_data_from_file(parameter)
                if json_data:
                    splited_list = parameter.split(".")
                    parameter_json_list.append({'.'.join(splited_list[len(splited_list)-2:]) : json_data})
        return parameter_json_list

    def generate_template_json(self):
        """
        generate the template json from template and parameter files
        """
        template_json = self.get_template()
        parameter_jsons = self.get_paramter_json_list()
        gen_template_json = None
        if template_json:
            gen_template_json = copy.deepcopy(template_json)
            for parameter_json in parameter_jsons:
                for file_type, variable_json in parameter_json.items():
                    if file_type in ["tfvars", "tfvars.json"]:
                        for key, value in variable_json.items():
                            self.gparams[key] = value
                    else:
                        if "variable" in variable_json:
                            for key, value in variable_json["variable"].items():
                                if "default" in value:
                                    self.gparams[key] = value["default"] 

            if "variable" in template_json:
                for key, value in template_json["variable"].items():
                    if "default" in value:
                        self.gparams[key] = value["default"]

            new_resources = {}
            if "module" in template_json:
                for key, value in template_json["module"].items():
                    if "source" in value:
                        default_gparams = {}
                        for k, v in value.items():
                            if k != "source":
                                default_gparams[k] = v

                        full_path_list = self.template_file.split("/")[:-1]
                        full_path = ("/".join(full_path_list)).replace("//","/")
                        module_file_path = ("%s/%s" % (full_path, value["source"])).replace("//","/")

                        logger.info("Finding module : %s", value["source"])
                        if exists_dir(module_file_path):
                            list_of_file = os.listdir(module_file_path)

                            template_file_path = ""
                            parameter_file_list = []
                            for entry in list_of_file:
                                new_file_path = ('%s/%s' % (module_file_path, entry)).replace('//', '/')
                                if exists_file(new_file_path):
                                    if self.is_template_file(new_file_path):
                                        template_file_path =  new_file_path
                                    elif self.is_parameter_file(new_file_path):
                                        parameter_file_list.append(new_file_path)
                                    
                            if template_file_path and parameter_file_list:
                                terraform_template_parser = TerraformTemplateParser(
                                    template_file_path,
                                    parameter_file=parameter_file_list,
                                    **{"default_gparams" : default_gparams})
                                new_template_json = terraform_template_parser.parse()
                                if new_template_json:
                                    for resource, resource_item in new_template_json.items():
                                        if resource not in new_resources:
                                            new_resources[resource] = resource_item
                                        else:
                                            new_resources[resource].update(resource_item)
                        else:
                            logger.error("module does not exist : %s ", value["source"])
                            
                if "module" in gen_template_json:
                    del gen_template_json["module"]
                    for key, value in new_resources.items():
                        if key in template_json and isinstance(template_json[key], dict):
                            template_json[key].update(value)
                        elif key not in template_json:
                            template_json[key] = value

            if 'data' in template_json:
                data_resource = {}
                logger.info("Before Process data")
                logger.info(template_json['data'])
                for data_key, data_value in template_json['data'].items():
                    processed_data = self.process_resource(data_value)
                    self.gdata[data_key] = processed_data
                    data_resource[data_key] = processed_data
                gen_template_json['data'] = data_resource
                logger.info("Processed data")
                logger.info(gen_template_json['data'])
            
            if 'resource' in template_json:
                self.resource = {}
                for resource_name, properties in template_json['resource'].items():
                    processed_resource = self.process_resource(properties)
                    self.resource[resource_name] = processed_resource
                gen_template_json['resource'] = self.resource
            
        return gen_template_json

    def process_resource(self, resource):
        """ 
        process the resource json and return the resource with updated values
        """
        new_resource = ""
        if  isinstance(resource, list):
            new_resource_list = [] 
            for value in resource:
                new_resource_list.append(self.process_resource(value))
            new_resource = new_resource_list
        
        elif isinstance(resource, dict):
            new_resource = {}
            for key, value in resource.items():
                processed_resource = self.process_resource(value)
                new_resource[key] = processed_resource
        
        elif isinstance(resource, str):
            # match the substrings for replace the value
            # pattern = re.compile(r'(var\..\w*)')
            # exmatch = re.findall(pattern, resource)
            logger.info(self.gparams)

            new_resource = resource
            exmatch = re.search(r'\${([^}]*)}', resource, re.I)
            if exmatch:
                matched_str = exmatch.group(0)[2:-1]
                splited_list = matched_str.split(".") 
                if len(splited_list) > 1:
                    if splited_list[0] in self.schema_filter:
                        result, new_value = self.schema_filter[splited_list[0]](".".join(splited_list[1:]))
                        if result:
                            new_resource = new_value
                    else:
                        result, new_value = self.schema_filter["other"](".".join(splited_list))
                        if result:
                            new_resource = new_value
        else:
            new_resource = resource
        
        return new_resource
