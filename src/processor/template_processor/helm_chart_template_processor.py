from processor.template_processor.base.base_template_processor import TemplateProcessor
from processor.helper.file.file_utils import exists_file,exists_dir
from processor.helper.yaml.yaml_utils import yaml_from_file,HelmChartConvertionKey
from yaml.loader import FullLoader
from processor.logging.log_handler import getlogger
from processor.templates.helm.helm_parser import HelmTemplateParser

logger = getlogger()

class HelmChartTemplateProcessor(TemplateProcessor):
    """
    For process helm charts
    """
    def __init__(self, node, **kwargs):
        super().__init__(node, tosave=False, **kwargs)
    
    def is_template_file(self, file_path):
        """
        check for valid template file for parse helm template
        """
        file_type = file_path.split(".")[-1]
        file_name = file_path.split("/")[-1].split(".")[0]
        if file_type == "yaml" and file_name == "Chart"  or HelmChartConvertionKey in file_path:
            helm_source = file_path.rpartition("/")[0]
            helm_template = HelmTemplateParser(helm_source)
            if helm_template.validate(helm_source):
                return True
            # file_path.rpartition("/")[0]
            return True
        return False

    def process_template(self, paths):
        """
        process the files stored at specified paths and returns the template
        """
        template_json = None
        
        if paths and isinstance(paths, list):
            template_file_path = ""
            # paths[0] = paths.
            for path in paths:
                file_path = '%s/%s' % (self.dir_path, path)
                logger.info("Fetching data : %s ", path)
                if self.is_template_file(file_path):
                    template_file_path = file_path

            self.template_file = template_file_path
            if template_file_path:
                template_json = yaml_from_file(file_path,loader=FullLoader)
                self.contentType = 'yaml'
        return template_json
        
        
        