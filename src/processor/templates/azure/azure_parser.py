"""
Define an interface for parsing azure template and its parameter files.
"""
import json
import copy
import os
import glob
import re
from processor.helper.json.json_utils import get_field_value, json_from_file, save_json_to_file
from processor.logging.log_handler import getlogger
from processor.templates.base.template_parser import TemplateParser

logger = getlogger()

class AzureTemplateParser(TemplateParser):
    """
    Azure Parser class for process Azure arm template
    """
    def __init__(self, template_file, tosave=False, **kwargs):
        super().__init__(template_file, tosave=False, **kwargs)
        self.gvariables = {}
        self.function_handlers = {
            "parameters": self.handle_params,
            "variables": self.handle_variables,
            "concat": self.handle_concat,
            "equals": self.handle_equals,
            "length": lambda x: (True, len(x))
        }
    
    def generate_template_json(self):
        """
        generate the template json from template and parameter files
        """
        stars = '*' * 25
        template_json = json_from_file(self.get_template())
        self.replace_spacial_characters(template_json)
        gen_template_json = None
        if template_json:
            gen_template_json = copy.deepcopy(template_json)
            if 'parameters' not in template_json:
                template_json['parameters'] = {}
            self.gparams = template_json['parameters']
            for param in self.get_parameter():
                param_json = json_from_file(param)
                if 'parameters' in  param_json and param_json['parameters']:
                    for key, value in param_json['parameters'].items():
                        # if key in template_json['parameters']:
                        if "value" in value:
                            if key not in template_json['parameters']:
                                template_json['parameters'][key] = {'value': value['value']}
                            else:
                                template_json['parameters'][key]['value'] = value['value']
                        else:
                            logger.error("From parameter %s was not replaced.", key)
                gen_template_json['parameters'] = self.gparams
            # print('%s Updated Parameters %s' % (stars, stars))
            # print(json.dumps(template_json['parameters'], indent=2))
            if 'variables' in template_json:
                self.gvariables = template_json['variables']
                new_resource = self.process_resource(template_json['variables'])
                # print('%s Original Variables %s' % (stars, stars))
                # print(json.dumps(template_json['variables'], indent=2))
                # print('%s Updated Variables %s' % (stars, stars))
                # print(json.dumps(new_resource, indent=2))
                # Second pass, becoz some variables have been defined in terms of parameters, functions like concat, substr
                self.gvariables = self.process_resource(new_resource)
                gen_template_json['variables'] = self.gvariables
            if 'resources' in template_json:
                new_resources = []
                for resource in template_json['resources']:
                    is_copy, copy_resources = self.handle_copy(resource)
                    if is_copy:
                        for resourc in copy_resources:
                            new_resource = self.process_resource(resourc)
                            new_resources.append(new_resource)
                    else:
                        new_resource = self.process_resource(resource)
                        new_resources.append(new_resource)
                    # print('%s Original Resource %s' % (stars, stars))
                    # print(json.dumps(resource, indent=2))
                    # print('%s Updated Resource %s' % (stars, stars))
                    # print(json.dumps(new_resource, indent=2))
                gen_template_json['resources'] = new_resources
        return gen_template_json

    def process_resource(self, resource):
        """ 
        process the resource json and return the resource with updated values
        """
        new_resource = resource
        if isinstance(resource ,dict):
            new_resource = {}
            for key, value in resource.items():
                if key == "accessPolicies":
                    print("Here")
                # if key == 'dnsNameForPublicIP':
                #     print("Here")
                if isinstance(value, str):
                    new_resource[key] = value
                    eval_expr = self.eval_expression(value)
                    if eval_expr:
                        func_name, func_params = self.func_details(eval_expr)
                        if func_name in self.function_handlers:
                            success, updated_value = self.function_handlers[func_name](func_params)
                            # print('*' * 50)
                            # print(value)
                            # print(updated_value)
                            # print('#' * 50)
                            new_resource[key] = updated_value if success else value
                else:
                    new_resource[key] = self.process_resource(value)
        elif isinstance(resource ,list):
            success = True
            new_resource = []
            for value in resource:
                if isinstance(value, str):
                    eval_expr = self.eval_expression(value)
                    if eval_expr:
                        func_name, func_params = self.func_details(eval_expr)
                        if func_name in self.function_handlers:
                            lsuccess, updated_value = self.function_handlers[func_name](func_params)
                            # print('*' * 50)
                            # print(value)
                            # print(updated_value)
                            # print('#' * 50)
                            if not lsuccess:
                                success = lsuccess
                            new_resource.append(updated_value)
                        else:
                            new_resource.append(value)
                    else:
                        new_resource.append(value)
                else:
                    new_resource.append(self.process_resource(value))
            if not success:
                new_resource = resource
        return new_resource
    
    def my_split(self, value):
        vals = []
        t = []
        count = 0
        for i in value:
            t.append(i)
            if i == '(':
                count += 1
            elif i == ')':
                count -= 1
            elif i == ',':
                if count == 0:
                    t.pop()
                    vals.append(''.join(t))
                    t = []
        if t:
            vals.append(''.join(t))
        return vals

    def do_parentheses_match(self, input_string):
        s = []
        balanced = True
        index = 0
        while index < len(input_string) and balanced:
            token = input_string[index]
            if token == "(":
                s.append(token)
            elif token == ")":
                if len(s) == 0:
                    balanced = False
                else:
                    s.pop()
            index += 1
        return balanced and len(s) == 0

    def handle_variables(self, variables_expr):
        # print(json.dumps(gvariables, indent=2))
        # print('@' * 50)
        # print(variables_expr)
        val = variables_expr.strip().replace("'", "")
        # if val == 'diagStorageAccName':
        #     print(val)
        if val in self.gvariables:
            # print(json.dumps(gvariables[val], indent=2))
            # return True, gvariables[val]
            success = False
            value = self.gvariables[val]
            if isinstance(value, str):
                eval_expr = self.eval_expression(value)
                if eval_expr:
                    func_name, func_params = self.func_details(eval_expr)
                    if func_name in self.function_handlers:
                        success, updated_value = self.function_handlers[func_name](func_params)
                        return success, updated_value
            return True, value
        else:
            print("%s variable does not exist" % val)
        return True, val


    def handle_params(self, params_expr):
        # print(json.dumps(gparams, indent=2))
        # print('@' * 50)
        # print(params_expr)
        ex_params = None
        exmatch = re.match(r'^(\(.*\))(.*)', params_expr, re.I)
        if exmatch:
            field, ex_params = exmatch.groups()
            val = field[1:-1].strip().replace("'", "")
        else:
            val = params_expr.strip().replace("'", "")
        # print(val)
        if val in self.gparams:
            # print(json.dumps(gparams[val], indent=2))
            if 'value' in self.gparams[val]:
                if ex_params:
                    return True, get_field_value(self.gparams[val]['value'], ex_params)
                return True, self.gparams[val]['value']
            elif 'defaultValue' in self.gparams[val]:
                if ex_params:
                    return True, get_field_value(self.gparams[val]['defaultValue'], ex_params)
                return True, self.gparams[val]['defaultValue']
        else:
            print("%s does not exist" % val)
        return True, val

    def handle_concat(self, concat_expr):
        # values = concat_expr.split(',')
        values = self.my_split(concat_expr)
        if values:
            success = True
            updated_values = []
            for value in values:
                func_name, func_params = self.func_details(value.strip())
                if func_name and func_params: 
                    # print(value)
                    # print(func_name, func_params)
                    lsuccess, updated_value = self.eval_func(func_name, func_params)
                    # print(updated_value)
                    if not lsuccess:
                        success = False
                    updated_values.append(updated_value if updated_value else value)
                else:
                    updated_values.append(value.strip().replace("'", ""))
            # print(updated_values)
            return(success, ''.join(str(value) for value in updated_values) if success else concat_expr)
        return False, concat_expr

    def handle_equals(self, equals_expr):
        values = equals_expr.split(',')
        if values and len(values) == 2:
            updated_values = []
            for value in values:
                func_name, func_params = self.func_details(value)
                if func_name and func_params: 
                    updated_value = self.eval_func(func_name, func_params)
                    updated_values.append(updated_value if updated_value else value)
                else:
                    updated_values.append(value.strip().replace("'", ""))
            # print(updated_values)
            return(True, updated_values[0] == updated_values[1])
        return True, False


    def eval_func(self, func_name, func_details):
        if func_name in self.function_handlers:
            return self.function_handlers[func_name](func_details)
        return False, None
    
    def version_str(self, version):
        """Convert numeric version to string eg: 0.1 => 0_1"""
        value = version.replace('.', '_') if version else version
        return value

    def is_parameter_file(self, filename):
        json_data = json_from_file(filename)
        if json_data and '$schema' in json_data and json_data['$schema']:
            match =  re.match(r'.*deploymentParameters.json#', json_data['$schema'], re.I)
            return True if match else False
        return None
            
    def is_template_file(self, filename):
        if filename and filename.endswith('_gen.json'):
            return False
        json_data = json_from_file(filename)
        if json_data and '$schema' in json_data and json_data['$schema']:
            match =  re.match(r'.*deploymentTemplate.json#$', json_data['$schema'], re.I)
            return True if match else False
        return None
            
    def eval_expression(self, value):
        match = re.match(r'\[(.*)\]', value, re.I)
        if match:
            return match.groups()[0]
        return None

    def func_details(self, value):
        # match = re.match(r'([a-z0-9A-Z]{0,})\((.*)\)', value, re.I)
        match = re.match(r'([a-z0-9A-Z]{0,})(\(.*)', value, re.I)
        if match:
            # Support only plain braces, no indexing
            params = match.groups()[1]
            parammatch = re.match(r'^\(.*\)$', params, re.I)
            exmatch = re.match(r'^(\(.*\))(.*)', params, re.I)
            if parammatch:
                if ('[' not in params or ']' not in params):
                    return match.groups()[0], params[1:-1]
            elif exmatch:
                #if ('[' not in params or ']' not in params):
                return match.groups()[0], params
        return None, None

    def replace_spacial_characters(self, gen_template_json):
        if gen_template_json.get('$schema', None):
            gen_template_json["\uFF04schema"] = gen_template_json["$schema"]
            del gen_template_json["$schema"]

        for key, value in gen_template_json.items():
            if isinstance(value, dict):
                self.replace_spacial_characters(value)
            elif isinstance(value, list):
                for val in value:
                    if isinstance(val, dict):
                        self.replace_spacial_characters(val)

    def handle_copy(self, resource):
        is_copy =  None
        value = None
        if 'copy' in resource:
            eval_expr = self.eval_expression(resource['copy']['count'])
            if eval_expr:
                func_name, func_params = self.func_details(eval_expr)
                if func_name in self.function_handlers:
                    ifunc_name, ifunc_params = self.func_details(func_params)
                    if ifunc_name in self.function_handlers:
                        _, ivalue = self.function_handlers[ifunc_name](ifunc_params)
                        if ivalue:
                            _, value = self.function_handlers[func_name](ivalue)
                            is_copy = resource['copy']['name']
            if is_copy and isinstance(value, int):
                resources = []
                for i in range(value):
                    resource_str = json.dumps(resource)
                    match_str = "copyIndex('%s')" % is_copy
                    resource_str = resource_str.replace(match_str, '%d' % i)
                    new_resource = json.loads(resource_str)
                    del new_resource['copy']
                    resources.append(new_resource)
                return True, resources
        return False, resource