from yaml.loader import FullLoader
from processor.logging.log_handler import getlogger
from processor.template_processor.base.base_template_processor import TemplateProcessor
from processor.templates.kubernetes.kubernetes_parser import KubernetesTemplateParser
from processor.helper.file.file_utils import exists_file
from processor.helper.yaml.yaml_utils import yaml_from_file

logger = getlogger()

class KubernetesTemplateProcessor(TemplateProcessor):
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
            kube_policy = ["apiVersion","kind","metadata","spec"]
            return True if json_data and any(elem in json_data for elem in kube_policy) else False
        return False

    def process_template(self, paths):
        """
        process the files stored at specified paths and returns the template
        """
        template_json = None
        
        if paths and isinstance(paths, list):
            template_file_path = ""

            for path in paths:
                file_path = '%s/%s' % (self.dir_path, path)
                logger.info("Fetching data : %s ", path)
                if self.is_template_file(file_path):
                    template_file_path = file_path
                else :
                    logger.info("\t\t WARN: %s contains invalid Kubernetes yaml")

            self.template_file = template_file_path
            if template_file_path and exists_file(template_file_path):
                kubernetes_template_parser = KubernetesTemplateParser(template_file_path) 
                template_json = kubernetes_template_parser.parse(template_file_path)
                if template_json:
                    self.contentType = kubernetes_template_parser.contentType
                    if template_json.get("kind"):
                        self.resource_types = [template_json.get("kind").lower()]
                
        return template_json
