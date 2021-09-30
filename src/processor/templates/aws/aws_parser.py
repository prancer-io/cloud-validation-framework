"""
Define an interface for parsing aws template and its parameter files.
"""
import json
import copy
from cfn_flip import to_json
from processor.helper.json.json_utils import json_from_file
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.templates.base.template_parser import TemplateParser

logger = getlogger()
allowed_extensions = ["json","yaml", "template", "txt"]

class AWSTemplateParser(TemplateParser):
    """
    AWS Parser class for process AWS cloudformation template
    """
    def __init__(self, template_file, tosave=False, **kwargs):
        super().__init__(template_file, tosave=False, **kwargs)
        self.mappings = {}
        self.intrinsic_functions = {
            "FindInMap" : self.handle_find_in_map,
            "Join" : self.handle_join,
            "If": self.handle_if,
            "Equals": self.handle_equals,
            "And": self.handle_and,
            "Or": self.handle_or,
            "Not": self.handle_not,
            "GetAtt": self.handle_get_att,
            "Select": self.handle_select,
            "Split": self.handle_split,
            "Sub": self.handle_sub,
        }
    
    def yaml_to_json(self, yaml_file):
        """
        takes the yaml file path and converts the returns the converted JSON object
        """
        template_json = None
        with open(yaml_file, encoding="utf-8") as yml_file:
            try:
                template_json = json.loads(to_json(yml_file.read()))
            except:
                file_name = yaml_file.split("/")[-1]
                logger.error("Failed to load yaml file, please check yaml file contains correct content: %s", file_name)
        return template_json
    
    def generate_template_json(self):
        """
        generate the template json from template and parameter files
        """
        gen_template_json = None
        template_json = None
        if self.get_template().endswith(".yaml") and exists_file(self.get_template()):
            template_json = self.yaml_to_json(self.get_template())
            self.contentType = 'yaml'
        elif self.get_template().endswith(".json") :
            template_json = json_from_file(self.get_template(), object_pairs_hook=None)
        elif self.get_template().endswith(".template") or self.get_template().endswith(".txt"):
            template_json = json_from_file(self.get_template(), object_pairs_hook=None)
            if template_json:
                self.contentType = "json"
            else:
                try:
                    template_json = self.yaml_to_json(self.get_template())
                    self.contentType = 'yaml'
                except:
                    pass

        self.template_json = template_json
        if not template_json:
            logger.error("Invalid path! No file found at : %s", self.get_template())
            return gen_template_json

        if "AWSTemplateFormatVersion" not in template_json:
            logger.error("Invalid file content : file does not contains 'AWSTemplateFormatVersion' field.")
            return gen_template_json

        if template_json:
            gen_template_json = copy.deepcopy(template_json)
            if 'Parameters' in template_json:
                self.gparams = template_json['Parameters']
                if self.parameter_file:
                    parameters = json_from_file(self.parameter_file, object_pairs_hook=None)
                    # parameters = self.json_from_file(self.parameter_file)
                    if parameters:
                        for param in parameters:
                            if "ParameterKey" in param and "ParameterValue" in param:
                                self.gparams[param["ParameterKey"]] = { "Default" : param["ParameterValue"] } 
            if 'Mappings' in template_json:
                self.mappings = template_json['Mappings']
            if 'Resources' in template_json:
                new_resources = []
                for key, resource in template_json['Resources'].items():
                    new_resource = self.process_resource(resource)
                    if "Type" in new_resource:
                        self.resource_types.append(new_resource.get("Type").lower())
                    new_resource["Name"] = key
                    new_resources.append(new_resource)
                    gen_template_json['Resources'] = new_resources
        return gen_template_json

    def process_function(self, resource):
        """
        performs the Intrinsic function on given resource
        """
        value = resource
        if isinstance(resource ,dict):
            if "Ref" in resource:
                value = self.handle_reference(value)
            else: 
                keys = value.keys()
                function = None
                for k in keys:
                    if k.startswith("Fn::"):
                        function = k
                if function:
                    function = function.split("Fn::")[1]
                    if function in self.intrinsic_functions:
                        value = self.intrinsic_functions[function](value)
                else:
                    value = self.process_resource(value)
        return value
    
    def process_resource(self, resource):
        """ 
        process the resource json and return the resource with updated values
        """
        new_resource = resource
        if isinstance(resource ,dict):
            new_resource = {}
            for key, value in resource.items():
                if isinstance(value, dict):
                    new_resource[key] = self.process_function(value)
                else:
                    result = self.process_resource(value)
                    new_resource[key] = result
        elif isinstance(resource ,list):
            new_resource = []
            for value in resource:
                value = self.process_function(value)
                if isinstance(value, str):
                    new_resource.append(value)
                else:
                    new_resource.append(self.process_resource(value))
        return new_resource
    
    def handle_reference(self, value):
        """
        Returns the default value for specified parameter reference
        """
        if value["Ref"] in self.gparams and "Default" in self.gparams[value["Ref"]]:
            value = self.gparams[value["Ref"]]["Default"]
        return value
    
    def handle_find_in_map(self, value):
        """
        Finding the appropriate value from the Mapping 
        """
        find_values = value["Fn::FindInMap"]

        for item in find_values:
            item = self.process_resource(item)

        if len(find_values) == 3 and all(isinstance(v, str) for v in find_values):
            map_name = find_values[0]
            top_level_key = find_values[1]
            second_level_key = find_values[2]

            if map_name in self.mappings and top_level_key in self.mappings[map_name] and \
                second_level_key in self.mappings[map_name][top_level_key]:
                value = self.mappings[map_name][top_level_key][second_level_key]        
        return value
    
    def handle_join(self, value):
        """
        Performes the `join` operation on set of values with specified delimiter.
        """
        join_values = value["Fn::Join"]
        for i in range(0, len(join_values)):
            join_values[i] = self.process_resource(join_values[i])
        
        if len(join_values) == 2 and all(isinstance(v, str) for v in join_values[1]):
            value = join_values[0].join(join_values[1])
        if not isinstance(value, str):
            value = self.process_resource(value)
        
        return value

    def handle_if(self, value):
        """
        perform the 'If' operation on values
        """
        condition, true_value, false_value = value["Fn::If"]
        new_condition = self.handle_condition(condition)
        true_value = self.process_resource(true_value)
        false_value = self.process_resource(false_value)

        
        if new_condition != condition:
            if new_condition == True:
                return true_value
            elif new_condition == False:
                return false_value
        else:
            return value

    def handle_equals(self, value):
        """
        Handle equals between 2 values
        """
        first_value, second_value = value.get("Fn::Equals")

        updated_first_value = self.process_handler_value(first_value)
        updated_second_value = self.process_handler_value(second_value)
        

        if updated_first_value == updated_second_value:
            return True
        else:
            return False
    
    def handle_and(self, value):
        """
        Handle AND condition within list
        """
        condition_list = value["Fn::And"]
        updated_condition_list = []
        for condition in condition_list:
            updated_condition = self.process_handler_value(condition)
            updated_condition_list.append(updated_condition)
            if not isinstance(updated_condition, bool):
                return value

        return all(updated_condition_list)
    
    def handle_or(self, value):
        """
        Handle Or condition within list
        """
        condition_list = value["Fn::Or"]
        updated_condition_list = []
        for condition in condition_list:
            updated_condition = self.process_handler_value(condition)
            updated_condition_list.append(updated_condition)
            if not isinstance(updated_condition, bool):
                return value

        return any(updated_condition_list)
    
        
    def handle_not(self, value):
        """
        Handle Not condition
        """
        not_value = value["Fn::Not"][0]
        updated_not_value = self.process_handler_value(not_value)

        if isinstance(updated_not_value, bool):
            return not updated_not_value
        else:
            return value
    
    def handle_get_att(self, value):
        """
        get attribute from local resource and update property
        """
        resource_name, attr_name = value["Fn::GetAtt"]
        attr_path_list = attr_name.split(".")
        for resource in self.template_json.get("Resources", []):
            try:
                if resource.get("Name") == resource_name:
                    resource_properties = resource.get("Properties",{})
                    resource_properties = self.process_handler_value(resource_properties)
                    for attr in attr_path_list:
                        resource_properties = resource_properties.get(attr,{})
                        if resource_properties == None:
                            return value
                    return resource_properties
            except:
                return value
        return value
    
    def handle_select(self, value):
        """
        select indexed value from list and update property
        """
        index, list_value = value["Fn::Select"]
        index = int(index)
        list_value = self.process_handler_value(list_value)
        if isinstance(list_value, list) and len(list_value)-1 >= index:
            return list_value[index]
        else:
            return value
    
    def handle_split(self, value):
        """
        split string and return list of values
        """
        delimiter, source_string = value["Fn::Split"]
        source_string = self.process_handler_value(source_string)
        if isinstance(source_string, str):
            return source_string.split(delimiter)
        else:
            return value
    
    def handle_sub(self, value):
        """
        substitute dict value in string
        """
        if isinstance(value["Fn::Sub"], list):
            string, sub_value_dict = value["Fn::Sub"]
            for key, val in sub_value_dict.items():
                val = self.process_handler_value(val)
                if string.find("${%s}"%(key)) != -1:
                    string = string.replace("${%s}"%(key),val)
                else:
                    return value
            return string
        else:
            return value
    
    def handle_condition(self, value):
        """
        handle "condition" by getting reference from 
        """
        resource_condition = self.template_json.get("Conditions")
        condition = resource_condition.get(value)
        if condition:
            updated_condition = self.process_function(condition)
            if condition != updated_condition:
                return updated_condition
            else:
                return value
        else:
            return value

    def process_handler_value(self, value):
        def all_keys(dict_obj):
            ''' This function generates all keys of
                a nested dictionary. 
            '''
            # Iterate over all keys of the dictionary
            for key , value in dict_obj.items():
                yield key
                # If value is of dictionary type then yield all keys
                # in that nested dictionary
                if isinstance(value, dict):
                    for k in all_keys(value):
                        yield k
        updated_value = value
        if isinstance(value, dict):
            process_function_value = False
            for key in value.keys():
                if key in ["Ref", "Fn::If", "Fn::Equals", "Fn:And", "Fn::Not", "Fn::Or", "Fn::Split", "Fn::Select", "Fn::GetAtt", "Fn::Sub"]:
                    process_function_value = True
            
            if process_function_value:
                updated_value = self.process_function(value)
            else:
                updated_value = self.process_resource(value)
            
        elif isinstance(value, list):
            updated_value = self.process_resource(value)
        
        else:
            updated_value = value
        
        return updated_value

if __name__ == '__main__':
    parameter_file = None
    template_file = '/tmp/templates/SQS_With_CloudWatch_Alarms.template'
    aws_template_parser = AWSTemplateParser(template_file, parameter_file=parameter_file)
    template_json = aws_template_parser.parse()
    print(json.dumps(template_json, indent=2))
