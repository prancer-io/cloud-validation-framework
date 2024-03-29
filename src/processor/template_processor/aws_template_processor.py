import json
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import json_from_file
from processor.template_processor.base.base_template_processor import TemplateProcessor
from processor.templates.aws.aws_parser import AWSTemplateParser, allowed_extensions
from processor.helper.file.file_utils import exists_file
from cfn_flip import to_json

logger = getlogger()

class AWSTemplateProcessor(TemplateProcessor):
    """
    Base Template Processor for process template 
    """
    def __init__(self, node, **kwargs):
        super().__init__(node, tosave=False, **kwargs)

    def is_parameter_file(self, file_path):
        """
        check for valid parameter file for parse cloudformation template
        """
        file_parts = file_path.split(".")
        if len(file_parts) > 0 and file_parts[-1] in allowed_extensions:
            json_data = json_from_file(file_path)
            if json_data and isinstance(json_data, list):
                parameter = json_data[0]
                if isinstance(parameter, dict) and "ParameterKey" in parameter and "ParameterValue" in parameter:
                    return True
        return False

    def is_template_file(self, file_path):
        """
        check for valid template file for parse cloudformation template
        """
        file_parts = file_path.split(".")
        if len(file_parts) > 0 and file_parts[-1] in allowed_extensions:
            template_json = None
            if file_path.endswith(".yaml") and exists_file(file_path):
                with open(file_path, encoding="utf-8") as yml_file:
                    try:
                        template_json = json.loads(to_json(yml_file.read()))
                        self.contentType = 'yaml'
                    except:
                        pass
            elif file_path.endswith(".json"):
                template_json = json_from_file(file_path)
                self.contentType = 'json'
            
            elif file_path.endswith(".template") or file_path.endswith(".txt"):
                template_json = json_from_file(file_path)
                if template_json:
                    self.contentType = 'json'
                else:
                    with open(file_path, encoding="utf-8") as yml_file:
                        try:
                            template_json = json.loads(to_json(yml_file.read()))
                            self.contentType = 'yaml'
                        except:
                            pass

            if template_json and "AWSTemplateFormatVersion" in template_json:
                return True
        return False

    def is_valid_file_extension(self, file_path):
        for extn in allowed_extensions:
            if file_path.endswith(extn):
                return True
        return False

    def process_template(self, paths):
        """
        process the files stored at specified paths and returns the template
        """
        template_json = None
        if paths and isinstance(paths, list):
            parameter_file = None
            template_file = None
            for path in paths:
                file_path = ('%s/%s' % (self.dir_path, path)).replace("//", "/")
                if self.is_valid_file_extension(file_path) and self.is_parameter_file(file_path):
                    parameter_file = file_path
                else:
                    template_file = file_path

            if template_file:
                self.template_files = [template_file]
                if parameter_file:
                    self.parameter_files = [parameter_file]
                    aws_template_parser = AWSTemplateParser(template_file, parameter_file=parameter_file)
                else:
                    aws_template_parser = AWSTemplateParser(template_file)
                template_json = aws_template_parser.parse()
                self.contentType = aws_template_parser.contentType
                self.resource_types = aws_template_parser.resource_types

        return template_json
