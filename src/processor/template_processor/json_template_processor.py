import json
import re
import os
from yaml.loader import FullLoader
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import json_from_file, get_field_value
from processor.template_processor.base.base_template_processor import TemplateProcessor
from processor.templates.google.google_parser import GoogleTemplateParser
from processor.helper.file.file_utils import exists_file
from processor.helper.config.config_utils import get_test_json_dir, framework_dir
from processor.helper.yaml.yaml_utils import yaml_from_file
from cfn_flip import flip, to_yaml, to_json

logger = getlogger()

class JsonTemplateProcessor(TemplateProcessor):
    """
    Base Template Processor for process template 
    """

    def __init__(self, node, **kwargs):
        super().__init__(node, tosave=False, **kwargs)
    
    def is_template_file(self, file_path):
        """
        check for valid template file for parse arm template
        """
        if len(file_path.split(".")) > 0 and file_path.split(".")[-1] == "json":
            json_data = json_from_file(file_path)
            return True if (json_data) else False
        return False

    def process_template(self, paths):
        """
        process the files stored at specified paths and returns the template
        """
        template_json = None
        
        if paths and isinstance(paths, list):
            template_file_path = ""
            deployment_file_path = ""

            for path in paths:
                file_path = '%s/%s' % (self.dir_path, path)
                logger.info("Fetching data : %s ", path)
                if self.is_template_file(file_path):
                    template_file_path = file_path

            self.template_file = template_file_path
            if template_file_path:
                template_json = json_from_file(file_path)
        return template_json