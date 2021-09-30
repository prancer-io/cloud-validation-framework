from yaml.loader import FullLoader
from processor.logging.log_handler import getlogger
from processor.template_processor.base.base_template_processor import TemplateProcessor
from processor.helper.yaml.yaml_utils import yaml_from_file

logger = getlogger()

class KccTemplateProcessor(TemplateProcessor):
    """
    Base Template Processor for process template 
    """

    def __init__(self, node, **kwargs):
        super().__init__(node, tosave=False, **kwargs)
    
    def is_template_file(self, file_path):
        """
        check for valid template file for parse arm template
        """
        if len(file_path.split(".")) > 0 and file_path.split(".")[-1] == "yaml":
            json_data = yaml_from_file(file_path, loader=FullLoader)
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
                template_json = yaml_from_file(file_path,loader=FullLoader)
                if template_json:
                    self.contentType = 'yaml'
                    if template_json.get("kind"):
                        self.resource_types = [template_json.get("kind").lower()]
        return template_json