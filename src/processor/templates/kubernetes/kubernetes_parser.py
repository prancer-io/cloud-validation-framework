import json
import os
import hcl
from yaml.loader import FullLoader
from cfn_flip import flip, to_yaml, to_json
from processor.logging.log_handler import getlogger
from processor.helper.yaml.yaml_utils import yaml_from_file
from processor.helper.json.json_utils import save_json_to_file,json_from_file
from processor.templates.base.template_parser import TemplateParser

logger = getlogger()

class KubernetesTemplateParser(TemplateParser):
    """
    Base Parser class for parse cloud templates
    """

    def __init__(self, template_file, tosave=False, **kwargs):
       """
       """
       super().__init__(template_file, tosave=False, **kwargs)
       self.type = {}

    
    def parse(self,file_path):
        """
        docstring
        """
        template_json = None
        with open(file_path) as scanned_file:
            try:
                template_json = json.loads(to_json(scanned_file.read()))
            except:
                file_name = file_path.split("/")[-1]
                logger.error("\t\t ERROR:  please check yaml file contains correct content: %s", file_name)
        return template_json
    
    def kind_detector(self):
        """
        docstring
        """
        return "simple"    