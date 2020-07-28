"""
Define an interface for parsing azure template and its parameter files.
"""
import json
import copy
import os
import glob
import re
import tempfile
import importlib
import sys
from jinja2 import Environment, FileSystemLoader, Undefined, make_logging_undefined
from processor.helper.file.file_utils import save_file, exists_file
from processor.helper.json.json_utils import get_field_value, json_from_file, save_json_to_file
from processor.logging.log_handler import getlogger
from processor.templates.base.template_parser import TemplateParser
from processor.templates.google.util import ResourceContext, SilentUndefined

logger = getlogger()

class GoogleTemplateParser(TemplateParser):
    """
    Google Parser class for process deployment manager template
    """
    def __init__(self, template_file, tosave=False, **kwargs):
        super().__init__(template_file, tosave=False, **kwargs)
        self.imports = []
        self.schema_filter = {
            "integer" : int,
            "boolean" : bool
        }
        self.python_import = False
    
    def update_properties_from_schema_file(self, jinja_file_path):
        """
        search for the schema file and if exist then update the properties with default value
        """
        logger.info("Finding schema file for jinja: %s", jinja_file_path)
        schema_file_path = ("%s.%s") % (jinja_file_path, "schema")
        if exists_file(schema_file_path):
            self.check_imports(schema_file_path)
            f = open(schema_file_path, "r")
            scehma_file = tempfile.mkdtemp()
            yaml_file_path = ("%s/%s") % (scehma_file, "scehma_file.yaml")
            save_file(yaml_file_path, f.read())
            
            schema_json = self.yaml_to_json(yaml_file_path)
            if "properties" in schema_json:
                for key, value in schema_json["properties"].items():
                    if key not in self.gparams and "default" in value:
                        if "type" in value:
                            if value['type'] in self.schema_filter:
                                self.gparams[key] = self.schema_filter[value['type']](value["default"])
                        else:
                            self.gparams[key] = value["default"]
    
    def check_imports(self, json_data):
        """
        check import file and update the import list
        """
        if "imports" in json_data:
            for import_file in json_data["imports"]:
                self.imports.append(import_file)

    def generate_template_json(self):
        """
        generate the template json from template and parameter files
        """
        template_json = self.yaml_to_json(self.get_template())
        gen_template_json = None
        if template_json:
            gen_template_json = copy.deepcopy(template_json)
            self.check_imports(template_json)
            if 'resources' in template_json:
                new_resources = []
                for resource in template_json['resources']:
                    if 'properties' in resource and resource['properties']:
                        self.gparams = resource['properties']
                    else:
                        self.gparams = {}
            
                    processed_resources = self.process_resource(resource)
                    new_resources = new_resources + processed_resources
                
                if not self.python_import:
                    gen_template_json['resources'] = new_resources
                else:
                    gen_template_json = None     
        return gen_template_json

    def process_resource(self, resource):
        """ 
        process the resource json and return the resource with updated values
        """
        new_resources = [resource]
        if "type" in resource and (".jinja" in resource["type"] or ".py" in resource["type"]) and not self.python_import:

            import_file_path = resource["type"]
            for import_file in self.imports:
                if "name" in import_file and import_file["name"] == resource["type"]:
                    import_file_path = import_file["path"]

            full_path_list = self.get_template().split("/")[:-1]
            full_path = ("/".join(full_path_list)).replace("//","/")
            resource_file_path = ("%s/%s" % (full_path, import_file_path)).replace("//","/")

            temp_file_path = "/".join(resource_file_path.split("/")[3:])
            logger.info("Fetch resource from `%s` file", temp_file_path)
            
            if exists_file(resource_file_path):
                self.update_properties_from_schema_file(resource_file_path)

                if ".jinja" in import_file_path:
                    if len(import_file_path.split("/")) > 1:
                        import_file_path_list = import_file_path.split("/")
                        import_file_path = import_file_path_list[-1]
                        full_path = (full_path + "/" + "/".join(import_file_path_list[:-1])).replace("//","/")
                    
                    LoggingUndefined = make_logging_undefined(logger=logger,base=SilentUndefined)
                    env = Environment(loader=FileSystemLoader(full_path), undefined=LoggingUndefined)
                    template = env.get_template(import_file_path)
                    render_data = {
                        "properties" : self.gparams
                    }

                    try:
                        template_render = template.render(**render_data)
                        resource_file = tempfile.mkdtemp()
                        yaml_file_path = ("%s/%s") % (resource_file, "resource_file.yaml")
                        save_file(yaml_file_path, template_render)
                        resource_json = self.yaml_to_json(yaml_file_path)
                    except:
                        resource_json = None

                    if resource_json:
                        self.check_imports(resource_json)
                        if "resources" in resource_json:
                            new_resource_list = []
                            for resource in resource_json["resources"]:
                                if 'properties' in resource and resource["properties"]:
                                    self.gparams.update(resource["properties"])
                                new_resource_list = new_resource_list + self.process_resource(resource)
                            new_resources = new_resource_list

                elif ".py" in import_file_path and exists_file(resource_file_path):
                    # skip the template if any of the resource require to process python file
                    self.python_import = True
                    return new_resources

                    pathname, filename = os.path.split(resource_file_path)
                    sys.path.append(os.path.abspath(pathname))
                    modname = os.path.splitext(filename)[0]

                    try:
                        resource_module = importlib.import_module(modname)
                    except:
                        logger.error("Failed to load module: ", modname)
                        return new_resources

                    resource_context = ResourceContext(self.gparams)
                    genreate_config = getattr(resource_module, "generate_config", None)
                    if not genreate_config:
                        genreate_config = getattr(resource_module, "GenerateConfig", None)
                    if not genreate_config:
                        logger.error("`genreate_config` or `GenerateConfig` method not defined in %s", resource["type"])
                        return new_resources

                    try:
                        resource_json = genreate_config(resource_context)
                        if resource_json:
                            self.check_imports(resource_json)
                            if "resources" in resource_json:
                                new_resource_list = []
                                for resource in resource_json["resources"]:
                                    if 'properties' in resource and resource["properties"]:
                                        self.gparams.update(resource["properties"])
                                    new_resource_list = new_resource_list + self.process_resource(resource)
                                new_resources = new_resource_list
                    except Exception as e:
                        logger.error("Failed to fetch resource. Missing parmater : %s", str(e))
        return new_resources