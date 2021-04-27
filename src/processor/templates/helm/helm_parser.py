from processor.logging.log_handler import getlogger
from processor.templates.base.template_parser import TemplateParser
from processor.helper.file.file_utils import exists_file,exists_dir


logger = getlogger()


class HelmTemplateParser(TemplateParser):
    def __init__(self, template_file, tosave=False, **kwargs):
        """
        Base Parser class for parse helm
        """
        super().__init__(template_file, tosave=False, **kwargs)
        self.type = {}

    def parse(self,file_path):
        return ""
    
    def validate(self,file_path):
        helm_source = file_path.rpartition("/")[0]
        check_file_path = "%s/Chart.yaml" % helm_source
        valeus_file_path = "%s/values.yaml" % helm_source
        template_dir_path = "%s/templates" % helm_source

        if  all([exists_file(check_file_path),exists_file(valeus_file_path),exists_dir(template_dir_path)]):
            return True
        return False