import json
import os
import re
from yaml.loader import FullLoader
from processor.logging.log_handler import getlogger
from processor.helper.yaml.yaml_utils import yaml_from_file
from processor.helper.json.json_utils import save_json_to_file

logger = getlogger()

class TemplateParser:
    """
    Base Parser class for parse cloud templates
    """

    def __init__(self, template_file, tosave=False, **kwargs):
        """
        parameters:
            template_file: path to the template file
            tosave: defines to save generated json file or not
            parameter_file: files to parameter file
            gparams: stores the parameters object require for process the template
        """
        self.template_file = template_file
        self.tosave = tosave
        self.parameter_file = kwargs.get("parameter_file", None)
        self.gparams = {}
        self.template_json = {}
        self.contentType = 'json'
        self.resource_types = []

    def get_template(self):
        """
        return the template file path
        """
        return self.template_file

    def get_parameter(self):
        """
        return the parameter file path
        """
        return self.parameter_file
    
    def generate_template_json(self):
        """
        generate the template json from template and parameter file
        """
        return None

    def parse(self):
        """
        parse the template and return the generated template JSON.
        """
        gen_template_json = self.generate_template_json()
        if self.tosave:
            file_name = os.path.splitext(self.get_template())[0] + '_gen.json'
            save_json_to_file(gen_template_json, file_name)
        return gen_template_json

    def yaml_to_json(self, yaml_file):
        """
        takes the yaml file path and converts the returns the converted JSON object
        """
        json_data = yaml_from_file(yaml_file, loader=FullLoader)
        return json_data
    
    def json_from_file(self, json_file):
        """
        takes the json file path and returns the JSON object
        """
        try:
            with open(json_file) as infile:
                file_data = infile.read()
        except UnicodeDecodeError:
            with open(json_file, 'r', encoding='utf-8') as infile:
                file_data = infile.read()
            
        return json.loads(file_data)
    
    def process_resource(self, resource):
        """
        process the resource json and return the resource with updated values
        """
        return resource
    

    def find_functions_all(self, data):
        final_list = []
        regex = r"[a-zA-Z]+\(.*,.*"
        findings = re.findall(regex, data)
        for finding in findings:
            parantheses_count = 0
            parantheses_found = False
            for count, character in enumerate(finding):
                if character == "(":
                    parantheses_count += 1
                    parantheses_found = True
                elif character == ")":
                    parantheses_count -= 1
                
                if parantheses_found and parantheses_count == 0:
                    remaining_string = finding[count:]
                    found_string = finding[:count+1]
                    final_list.append(found_string)
                    final_list.extend(self.find_functions_all(remaining_string))
                    break
        
        return final_list
