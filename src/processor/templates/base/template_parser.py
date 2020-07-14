from processor.logging.log_handler import getlogger

logger = getlogger()

class TemplateParser:
    """
    Base Parser class for parse cloud templates
    """

    def __init__(self, template_file, tosave=False, **kwargs):
        """
        """
        self.template_file = template_file
        self.tosave = tosave
        self.parameter_file = kwargs.get("parameter_file", None)
        self.gparams = {}

    def get_template(self):
        """
        return the template file path
        """
        return self.template_file

    def get_parameter(self):
        """
        return the template file path
        """
        return self.parameter_file

    def parse(self):
        """
        parse the template and return the generated template JSON.
        """
        return {}

    def yaml_to_json(self, yaml_file):
        """
        takes the yaml file path and converts the returns the converted JSON object
        """
        return {}
    
    def process_resource(self, resource):
        """
        process the resource json and return the resource with updated values
        """
        return resource