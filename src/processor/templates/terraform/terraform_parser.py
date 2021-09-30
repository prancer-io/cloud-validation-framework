"""
Define an interface for parsing azure template and its parameter files.
"""
import copy
import glob
import re
import os
import inspect
import ast
import hcl2
from processor.logging.log_handler import getlogger
from processor.templates.base.template_parser import TemplateParser
from processor.helper.file.file_utils import exists_file, exists_dir
from processor.templates.terraform.helper.function.terraform_functions import default_functions
from processor.templates.terraform.helper.expression.terraform_expressions import expression_list
from processor.helper.json.json_utils import json_from_file, json_from_string
from processor.helper.hcl.hcl_utils import hcl_to_json
from processor.templates.terraform.helper.module_parser import ModuleParser

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
        self.default_gparams = kwargs.get("default_gparams", {})
        self.gdata = {}
        self.resource = {}
        self.module_params = {
            "module" : {}
        }
        self.temp_params = {}
        self.count = None
        self.process_module = kwargs.get("process_module", False)
        self.replace_values = {
            "true" : True,
            "false" : False,
            "True" : True,
            "False" : False,
            "&&" : "and",
            "||" : "or",
            "None" : None,
            "!" : "not",
        }
        self.replace_value_str = ["and", "or", "not"]
        self.template_file_list = [self.template_file]
        self.parameter_file_list = self.parameter_file if self.parameter_file else []
        self.connector_data = kwargs.get("connector_data", False)
        self.exclude_directories = [".git"]
        self.template_references = {
            "main_templates" : [],
            "module_templates" : []
        }

    def is_template_file(self, file_path):
        """
        check for valid template file for parse terraform template
        """
        if len(file_path.split(".")) > 0 and file_path.split(".")[-1] == "tf":
            json_data = hcl_to_json(file_path)
            return True if (json_data and ("resource" in json_data or "module" in json_data)) else False
        elif len(file_path.split(".")) > 0 and file_path.split(".")[-1] == "json":
            json_data = json_from_file(file_path, escape_chars=['$'])
            return True if (json_data and ("resource" in json_data or "module" in json_data)) else False
    
    def is_parameter_file(self, file_path):
        """
        check for valid variable file for parse terraform template
        """
        if len(file_path.split(".")) > 0 and file_path.split(".")[-1] in ["tf", "tfvars"]:
            json_data = hcl_to_json(file_path)
            return True if (json_data and not "resource" in json_data) else False
        elif len(file_path.split(".")) > 1 and [ele for ele in [".tfvars.json", ".tf.json"] if(ele in file_path)]:
            json_data = json_from_file(file_path, escape_chars=['$'])
            return True if (json_data and not "resource" in json_data) else False
        return False

    def process_other(self, resource):
        """
        return default value of the variable if variable is set in terraform files
        """
        main_status = False

        status, value = self.parse_field_value(resource, self.resource)
        main_status = True if status else main_status
        if value is None:
            status, value = self.parse_field_value(resource, self.module_params)
            main_status = True if status else main_status
        if value is None:
            status, value = self.parse_field_value(resource, self.temp_params)
            main_status = True if status else main_status
        return main_status, value

    def process_variable(self, resource):
        """
        return default value of the variable if variable is set in terraform files
        """
        main_status = False
        status, value = self.parse_field_value(resource, self.default_gparams)
        main_status = True if status else main_status
        if value is None:
            status, value = self.parse_field_value(resource, self.gparams)
            main_status = True if status else main_status
        if value is None:
            status, value = self.parse_field_value(resource, self.resource)
            main_status = True if status else main_status
        return main_status, value
    
    def process_data(self, resource):
        """
        return value of the data if the given data is contains in terraform template file
        """
        return self.parse_field_value(resource, self.gdata)
    
    def parse_field_value(self, resource, from_data):
        resource_list = re.compile("\.(?![^[]*\])").split(resource)
        value = copy.deepcopy(from_data)
        is_valid = True
        for resource in resource_list:
            # process variables like this: var.network_http["cidr"]
            pattern = re.compile(r'\[["|\'](.*?)["|\']\]')
            map_keys = re.findall(pattern, resource)
            if not map_keys:
                pattern = re.compile(r'\[(.*?)\]')
                map_keys = re.findall(pattern, resource)
            if map_keys and len(resource.split("[")) > 1:
                res = resource.split("[")[0]
                if res in value:
                    value = value.get(res)
                else:
                    value = None
                    is_valid = False
                    break
                for key in map_keys:
                    if value is None or not isinstance(value, dict):
                        is_valid = False
                        break

                    if key in value:
                        value = value.get(key)
                    else:
                        value = None
                        is_valid = False
                if value is None:
                    break
                continue
            if isinstance(value, list) and resource == "*" and self.count is not None and self.count < len(value):
                value = value[self.count]
            elif isinstance(value, dict):            
                if resource in value:
                    value = value.get(resource)
                else:
                    value = None
                    is_valid = False
                if value is None:
                    break
            else:
                value = None
                is_valid = False
                break
        
        if is_valid:
            return True, value
        else:
            return False, value
    
    def get_template(self):
        """
        return the template json data
        """
        # used for terraform file remediation
        self.template_references["main_templates"].append({
            "main_file_path" : self.get_ralative_path(self.template_file)
        })

        json_data = None
        if len(self.template_file.split(".")) > 0 and self.template_file.split(".")[-1]=="tf":
            json_data = hcl_to_json(self.template_file)
            self.contentType = 'terraform'
        elif len(self.template_file.split(".")) > 1 and ".tf.json" in self.template_file:
            json_data = json_from_file(self.template_file, escape_chars=['$'])
        return json_data
    
    def get_paramter_json_list(self):
        """
        process parameter files and returns parameters json list
        """
        parameter_json_list = []
        for parameter in self.parameter_file:
            if len(parameter.split(".")) > 0 and parameter.split(".")[-1] in ["tf", "tfvars"]:
                json_data = hcl_to_json(parameter)
                if json_data:
                    parameter_json_list.append({parameter.split(".")[-1] : json_data})
            elif len(parameter.split(".")) > 1 and [ele for ele in [".tfvars.json", ".tf.json"] if(ele in parameter)]:
                json_data = json_from_file(parameter, escape_chars=['$'])
                if json_data:
                    splited_list = parameter.split(".")
                    parameter_json_list.append({'.'.join(splited_list[len(splited_list)-2:]) : json_data})
        return parameter_json_list
    
    def get_ralative_path(self, file_path):
        """
        takes full path of template or parameter file and returns the relative path by removing `temp` directory path
        """
        split_path = file_path.split("/")
        return "/%s" % "/".join(split_path[3:]).replace("//","/")

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
                            if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
                                value[0] = self.parse_string(value[0])
                            key = self.parse_string(key)
                            self.gparams[key] = value
                    else:
                        if "variable" in variable_json:
                            for var in variable_json["variable"]:
                                for key, value in var.items():
                                    if "default" in value:
                                        self.gparams[key] = value["default"] 

            if "variable" in template_json:
                for var in template_json["variable"]:
                    for key, value in var.items():
                        if "default" in value:
                            self.gparams[key] = value["default"]

            new_resources = {}
            if "module" in template_json:
                for mod in template_json["module"]:
                    for key, value in mod.items():
                        if "source" in value:
                            default_gparams = {}
                            self.module_params["module"][key] = {}
                            for k, v in value.items():
                                if k != "source":
                                    processed_data, processed = self.process_resource(v, count=self.count)
                                    default_gparams[k] = processed_data
                                    self.module_params["module"][key][k] = processed_data

                            full_path_list = self.template_file.split("/")[:-1]
                            template_file_path = ("/".join(full_path_list)).replace("//","/")
                            module_parser = ModuleParser(value["source"], template_file_path, connector_data=self.connector_data)
                            module_file_path = module_parser.process_source()

                            if not module_file_path:
                                continue
                            
                            logger.info("Finding module : %s", module_file_path)
                            if exists_dir(module_file_path):
                                list_of_file = os.listdir(module_file_path)

                                template_file_path_list = []
                                parameter_file_list = []
                                for entry in list_of_file:
                                    if any(exclude_dir in entry for exclude_dir in self.exclude_directories):
                                        continue
                                    new_file_path = ('%s/%s' % (module_file_path, entry)).replace('//', '/')
                                    self.template_references["module_templates"].append({
                                        "main_file_path" : self.get_ralative_path(self.template_file),
                                        "module_file_path" : self.get_ralative_path(new_file_path),
                                        "module_label" : key
                                    })
                                    if exists_file(new_file_path):
                                        if self.is_template_file(new_file_path):
                                            template_file_path_list.append(new_file_path)
                                        elif self.is_parameter_file(new_file_path):
                                            parameter_file_list.append(new_file_path)
                                
                                if template_file_path_list and parameter_file_list:
                                    for template_file_path in template_file_path_list:
                                        terraform_template_parser = TerraformTemplateParser(
                                            template_file_path,
                                            parameter_file=parameter_file_list,
                                            **{"default_gparams" : default_gparams, "process_module" : True })
                                        new_template_json = terraform_template_parser.parse()

                                        self.template_file_list = self.template_file_list + terraform_template_parser.template_file_list
                                        self.parameter_file_list = self.parameter_file_list + terraform_template_parser.parameter_file_list

                                        if new_template_json:
                                            for resource, resource_item in new_template_json.items():
                                                # set parameters from modules files to main resource file
                                                if resource == "resource":
                                                    for resource_key, resource_value in resource_item.items():
                                                        for resource_name, resource_properties in resource_value.items():
                                                            if isinstance(resource_properties, dict):
                                                                for default_key, default_value in default_gparams.items():
                                                                    if default_key not in resource_properties:
                                                                        resource_properties[default_key] = default_value
                                                            if isinstance(resource_properties, list):
                                                                for resource_property in resource_properties:
                                                                    for default_key, default_value in default_gparams.items():
                                                                        if default_key not in resource_property:
                                                                            resource_property[default_key] = default_value
                                                if resource not in new_resources:
                                                    new_resources[resource] = [resource_item]
                                                else:
                                                    new_resources[resource].append(resource_item)
                            else:
                                logger.error("module does not exist : %s ", value["source"])
                            
                if "module" in gen_template_json:
                    del gen_template_json["module"]

            if 'data' in template_json:
                data_resource = {}
                for data_item in template_json['data']:
                    for data_key, data_value in data_item.items():
                        processed_data, processed = self.process_resource(data_value, count=self.count)
                        self.gdata[data_key] = processed_data
                        data_resource[data_key] = processed_data
                gen_template_json['data'] = data_resource
            
            self.resource = {}
            resources = []
            if "resource" in new_resources and isinstance(new_resources["resource"], list):
                for resource in new_resources["resource"]:
                    for resource_name, properties in resource.items():
                        processed_resource, processed = self.process_resource(properties, count=self.count)
                        if not self.process_module:
                            if resource_name in self.resource:
                                self.resource[resource_name].append(processed_resource)
                            else:
                                self.resource[resource_name] = [processed_resource]
                        else:
                            self.resource[resource_name] = processed_resource

            if 'resource' in template_json:
                for res in template_json['resource']:
                    for resource_name, properties in res.items():
                        processed_resource, processed = self.process_resource(properties, count=self.count)
                        if not self.process_module:
                            if resource_name in self.resource:
                                self.resource[resource_name].append(processed_resource)
                            else:
                                self.resource[resource_name] = [processed_resource]
                        else:
                            self.resource[resource_name] = processed_resource

            if not self.process_module:
                for resource_name, processed_resource_list in self.resource.items():
                    for processed_resource in processed_resource_list:
                        if isinstance(processed_resource, dict):
                            for name, properties in processed_resource.items():
                                if isinstance(properties, list):
                                    for property in properties:
                                        self.resource_types.append(resource_name.lower())
                                        resources.append({
                                            "type" : resource_name,
                                            "name" : name,
                                            "properties" : property
                                        })    
                                else:
                                    self.resource_types.append(resource_name.lower())
                                    resources.append({
                                        "type" : resource_name,
                                        "name" : name,
                                        "properties" : properties
                                    })
                    gen_template_json['resources'] = resources

                    if 'resource' in gen_template_json:
                        del gen_template_json['resource']
            else:
                gen_template_json['resource'] = self.resource
            
        return gen_template_json
    
    def check_numeric_value(self, resource):
        """ check that resource is numeric value or not and return the numeric value """
        try:
            resource = int(resource)
            return True, resource
        except ValueError:
            pass

        try:
            resource = float(resource)
            return True, resource
        except ValueError:
            pass

        return False, resource
    
    def check_json_or_list_value(self, resource, count=None):
        """ check that string resource is json or list type or not and return the list or json value """
        json_data = json_from_string(resource.replace("\'","\""))
        if json_data:
            resource, processed = self.process_resource(json_data, count=count)
            return True, resource
        
        json_data = json_from_string(re.sub(r"(?<!\\)\"", "\\\"", resource).replace("\'","\""))
        if json_data:
            resource, processed = self.process_resource(json_data, count=count)
            return True, resource
        
        try:
            if resource.startswith('[') and resource.endswith(']'):
                list_data = ast.literal_eval(resource)
                resource, processed = self.process_resource(list_data, count=count)
                return True, resource
        except:
            pass

        return False, resource
    
    def parse_string(self, resource):
        if resource.startswith('"') and resource.endswith('"'):
            resource = resource[1:-1]
        return resource

    def split_parameters(self, value):
        try:
            value = "[%s]" % value
            value = value.replace("'", '"')
            parsed = hcl2.loads('split = %s \n' % value)
            
            params = []
            for split_str in parsed["split"]:
                if split_str != None:
                    split_str = str(split_str)
                    exmatch = re.search(r'^\${.*}$', split_str, re.I)
                    if exmatch:
                        match_values = re.search(r'(?<=\{).*(?=\})', split_str, re.I)
                        if match_values:
                            split_str = match_values.group(0)
                        else:
                            split_str = exmatch.group(0)[2:-1]
                
                params.append(split_str)
            return params 
        except Exception as e:
            logger.debug("Failed to split paramaters")
            logger.debug(value)
            return []

    def process_expression_parameters(self, param_str, count):
        
        groups = re.findall(r'([.a-zA-Z]+)[(].*[,].*[)]', param_str, re.I)
        if groups:
            for group in groups:
                updated_group, _ = self.process_resource(group, count)
                param_str.replace(group, updated_group)
        
        groups = re.findall(r'^[(].*[,].*[)]|.* ([(].*[)])', param_str, re.I)
        if groups:
            for group in groups:
                parameter_str = re.findall("(?<=\().*(?=\))", group)[0]
                updated_group = self.process_expression_parameters(parameter_str, count)
                param_str.replace(group, updated_group)
        
        return param_str

    def process_resource(self, resource, count=None):
        """ 
        process the resource json and return the resource with updated values
        """
        processed = True
        new_resource = ""
        if isinstance(resource, list):
            new_resource_list = [] 
            for value in resource:
                processed_resource, processed = self.process_resource(value, count=count)
                new_resource_list.append(processed_resource)
            new_resource = new_resource_list
        
        elif isinstance(resource, dict):
            new_resource = {}
            new_resource_list = []
            r_count = resource.get("count")
            if r_count:
                count_resource, processed = self.process_resource(r_count, count=count)
                if isinstance(count_resource, int):
                    for i in range(count_resource):
                        new_resource_dict = {}
                        process_resource = copy.deepcopy(resource)
                        process_resource["count"] = i
                        del process_resource["count"]
                        self.count = i
                        for key, value in process_resource.items():
                            if key == "dynamic" and value and isinstance(value, list) and isinstance(value[0], dict):
                                processed_resource, processed = self.process_resource({ "dynamic" : value }, count=i)
                                if processed_resource and isinstance(processed_resource, dict):
                                    for res, val in processed_resource.items():
                                        new_resource_dict[res] = val
                            else:
                                processed_resource, processed = self.process_resource(value, count=i)
                                new_resource_dict[key] = processed_resource
                        new_resource_list.append(new_resource_dict)
                    self.count = None
                    new_resource = new_resource_list
                else:
                    for key, value in resource.items():
                        processed_resource, processed = self.process_resource(value, count=count)
                        new_resource[key] = processed_resource
            else:
                for key, values in resource.items():
                    # if key == "dynamic" and isinstance(value, dict):
                    if key == "dynamic" and values and isinstance(values, list) and isinstance(values[0], dict):
                        for value in values:
                        # value = value[0]
                            loop_values = []
                            for main_key, loop_content in value.items():
                                var = main_key
                                resource_properties = []
                                if isinstance(loop_content, dict):
                                    for loop_content_key, loop_content_value in loop_content.items():
                                        if loop_content_key == "for_each":
                                            loop_values, processed = self.process_resource(loop_content_value, count=count)
                                        if loop_content_key == "iterator":
                                            var, processed = self.process_resource(loop_content_value, count=count)
                                        # if loop_content_key == "content" and isinstance(loop_content_value, dict):
                                        if loop_content_key == "content" and loop_content_value and \
                                            isinstance(loop_content_value, list) and isinstance(loop_content_value[0], dict):
                                            loop_content_value = loop_content_value[0]
                                            if isinstance(loop_values, list):
                                                for loop_value in loop_values:
                                                    resource_property = {}
                                                    for content_key, content_value in loop_content_value.items():
                                                        if isinstance(content_value, str):
                                                            self.temp_params[var] = {
                                                                "value" : loop_value
                                                            }
                                                            # content_value = content_value.replace(var+".value",str(loop_value))
                                                        content_value, processed = self.process_resource(content_value, count=count)
                                                        resource_property[content_key] = content_value
                                                        self.temp_params = {}
                                                    resource_properties.append(resource_property)
                                            elif isinstance(loop_values, dict):
                                                for loop_key, loop_value in loop_values.items():
                                                    resource_property = {}
                                                    for content_key, content_value in loop_content_value.items():
                                                        if isinstance(content_value, str):
                                                            self.temp_params[var] = {
                                                                "value" : loop_value,
                                                                "key" : loop_key
                                                            }
                                                            # content_value = content_value.replace(var+".value",str(loop_value))
                                                            # content_value = content_value.replace(var+".key",str(loop_key))
                                                        content_value, processed = self.process_resource(content_value, count=count)
                                                        resource_property[content_key] = content_value
                                                        self.temp_params = {}
                                                    resource_properties.append(resource_property)
                                new_resource[main_key] = resource_properties
                    else:
                        processed_resource, processed = self.process_resource(values, count=count)
                        new_resource[key] = processed_resource
        
        elif isinstance(resource, str):
            # match the substrings for replace the value
            # pattern = re.compile(r'(var\..\w*)')
            # exmatch = re.findall(pattern, resource)
            parsed_string = self.parse_string(resource)

            new_resource = copy.deepcopy(parsed_string)
            exmatch = re.search(r'\${([^}]*)}', new_resource, re.I)
            if exmatch:
                match_values = re.search(r'(?<=\{).*(?=\})', new_resource, re.I)
                if match_values:
                    matched_str = match_values.group(0)
                else:
                    matched_str = exmatch.group(0)[2:-1]
            else:
                matched_str = parsed_string

            matched_str = matched_str.strip()
            matched_str = self.parse_string(matched_str)

            result, res = self.check_numeric_value(matched_str)
            if result:
                new_resource = res
                return new_resource, processed

            result, res = self.check_json_or_list_value(matched_str, count=count)
            if result:
                new_resource = res
                return new_resource, processed

            for func in default_functions:
                m = re.match(func['expression'], matched_str)
                if not m:
                    continue

                parameter_str = re.findall("(?<=\().*(?=\))", m.group(0))[0]
                parameters = []
                process = True

                found_parameters = self.split_parameters(parameter_str.strip())

                for param in found_parameters:
                # for param in re.findall("(?:[^,()]|\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\))+", parameter_str.strip()):
                # for param in parameter_str.strip().split(","):
                    param_exmatch = re.search(r'(^[\'|\"]\${([^}]*)}[\'|\"]$)|(^\${([^}]*)}$)', param.strip(), re.I)
                    if param_exmatch:
                        match_values = re.search(r'(?<=\{).*(?=\})', param.strip(), re.I)
                        if match_values:
                            param = match_values.group(0)
                
                    processed_param, processed = self.process_resource("${" + param.strip() + "}", count)
                    if (isinstance(processed_param, str) and re.search(r'\${([^}]*)}', processed_param, re.I)):
                        process = False
                        parameters.append(param.strip())
                    # Check only for None return
                    elif processed_param == None and re.match(".*(\.\*\.).*", param.strip()):
                        process = False
                        parameters.append(param.strip())
                    else:
                        parameters.append(processed_param)

                args = inspect.getargspec(func['method']).args
                varargs = inspect.getargspec(func['method']).varargs
                keywords = inspect.getargspec(func['method']).keywords
                defaults = inspect.getargspec(func['method']).defaults

                if process and ((len(args) == len(parameters)) or \
                    (defaults and len(parameters) <= len(args) and len(parameters) >= (len(args) - len(defaults))) or \
                    varargs or keywords):
                    try:
                        new_resource = func['method'](*parameters)
                    except Exception as e:
                        logger.error("Failed to process %s : %s", new_resource, str(e))
                else:
                    parameters = [str(ele) for ele in parameters]
                    new_resource = func['method'].__name__ + "(" + ",".join(parameters) + ")"
                break 
            else:
                for func in expression_list:
                    m = re.match(func['expression'], matched_str)
                    if not m:
                        continue

                    parameter_str = m.group(0)
                    parameter_str = self.process_expression_parameters(parameter_str, count)
                    
                    string_params = {}
                    groups = re.findall(r'\".*?\"', parameter_str, re.I)
                    if groups:
                        i = 0
                        for group in groups:
                            updated_group, _ = self.process_resource(groups[i], count)
                            string_params["group%s" % (str(i))] = updated_group
                            parameter_str = parameter_str.replace(group, "group%s" % (str(i)))
                            i+=1
                    
                    # params = re.findall(r"[a-zA-Z0-9.()\[\]_*\"]+|(?:(?![a-zA-Z0-9.()\[\]_*\"]).)+", parameter_str)
                    params = re.findall(r"[a-zA-Z0-9.()\[\],-_*\"\'\{\$\}]+|(?:(?![ a-zA-Z0-9.()\[\]_*\"\'\{\$\}]).)+", parameter_str)

                    if params and len(params) > 1:
                        new_parameter_list = []
                        process_function = True
                        for param in params:
                            if param in string_params:
                                param = str(string_params[param])
                            processed_param, processed = self.process_resource("${" + param.strip() + "}", count=count)
                            if isinstance(processed_param, str) and (re.findall(r".*\(.*\)", processed_param) or re.findall(r"\${([^}]*)}", processed_param)):
                                process_function = False # parameter processing failed
                                new_parameter_list.append("\"" + param + "\"")
                            elif isinstance(processed_param, str) and re.findall(r"[a-zA-Z]", processed_param) and processed_param not in self.replace_value_str:
                                new_parameter_list.append("\"" + processed_param + "\"")
                            elif isinstance(processed_param, str) and len(processed_param) == 0:
                                new_parameter_list.append('""')
                            elif processed_param is None and len(param.strip().split(".")) > 1 and not processed:
                                process_function = False # variable value not set in vars.tf file
                                new_parameter_list.append("\"" + param + "\"")
                            else:
                                new_parameter_list.append(str(processed_param))

                        if process_function:
                            new_resource = func['method'](" ".join(new_parameter_list))
                        else:
                            new_resource = matched_str
                else:
                    splited_list = matched_str.split(".") 
                    if len(splited_list) > 1:
                        if splited_list[0] in self.schema_filter:
                            result, new_value = self.schema_filter[splited_list[0]](".".join(splited_list[1:]))
                            if result:
                                new_resource = new_value
                            else:
                                processed = False
                        else:
                            if matched_str == "count.index" and count is not None:
                                new_resource = count
                            else:
                                result, new_value = self.schema_filter["other"](".".join(splited_list))
                                if result:
                                    new_resource = new_value
                    else:
                        new_resource = matched_str
        else:
            new_resource = resource
        
        if isinstance(new_resource, str) and new_resource.strip() in self.replace_values:
            new_resource = self.replace_values[new_resource.strip()]

        return new_resource, processed
