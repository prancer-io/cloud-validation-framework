"""
Define an interface for parsing aws template and its parameter files.
"""
import json
import copy
import re
import os
import yaml
from cfn_flip import flip, to_yaml, to_json
from processor.helper.json.json_utils import json_from_file, save_json_to_file
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.helper.yaml.yaml_utils import yaml_from_file
from processor.templates.base.template_parser import TemplateParser

logger = getlogger()

class AWSTemplateParser(TemplateParser):
    """
    AWS Parser class for process AWS cloudformation template
    """
    def __init__(self, template_file, tosave=False, **kwargs):
        super().__init__(template_file, tosave=False, **kwargs)
        self.mappings = {}
        self.intrinsic_functions = {
            "FindInMap" : self.handle_find_in_map,
            "Join" : self.handle_join
        }
    
    def yaml_to_json(self, yaml_file):
        """
        takes the yaml file path and converts the returns the converted JSON object
        """
        template_json = None
        with open(yaml_file) as yml_file:
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
        elif self.get_template().endswith(".json"):
            template_json = json_from_file(self.get_template(), object_pairs_hook=None)
            # template_json = self.json_from_file(self.get_template())

        logger.info(self.get_template())
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
                        logger.info(self.gparams)
            if 'Mappings' in template_json:
                self.mappings = template_json['Mappings']
            if 'Resources' in template_json:
                new_resources = []
                for key, resource in template_json['Resources'].items():
                    new_resource = self.process_resource(resource)
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
