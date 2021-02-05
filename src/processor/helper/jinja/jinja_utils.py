import traceback
from ruamel.yaml import YAML
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
import re

logger = getlogger()

yaml = YAML()

class JinjaConverter:
    """ analyse, change and revert YAML/jinja2 mixture to/from valid YAML"""
    def __init__(self):
        self.property_start = '""#<<<'
        self.property_end = '>>>#'
        self.comment_start = "#>"
        self.comment_end = "<#"
        self.block_comment_start = "#{#"
        self.quote = "<quotes>"
        self.double_quote = "<dquotes>"

    def replace_newline_character(self, replace_string, revert=False):
        if revert:
            return replace_string.replace("\n#", "\n")
        else:
            return "\n#".join(replace_string.splitlines())

    def comment_jinja_syntax(self, s):
        """ comment the jinja syntax and return the string with replaced values """

        s = re.sub("({#[\S\s]*?#})", lambda m: self.replace_newline_character(m.group(0)), s, flags=re.DOTALL)
        updated_string = s.replace('{{ ', self.property_start) \
            .replace(' }}', self.property_end) \
            .replace('{%', self.comment_start) \
            .replace('%}', self.comment_end) \
            .replace('"', self.double_quote) \
            .replace("'", self.quote) \
            .replace("{#", self.block_comment_start)
        return updated_string

    def revert(self, s):
        """ reverts the string to it's original states and retuns the updated string """
        if s and isinstance(s, str):
            new_string = s.replace(self.double_quote, '"') \
                .replace(self.quote, "'") \
                .replace(self.property_start, '{{ ') \
                .replace(self.property_end, ' }}') \
                .replace(self.comment_start, '{%') \
                .replace(self.comment_end, '%}') \
                .replace(self.block_comment_start, "{#")
            
            new_string = re.sub("({#[\S\s]*?#})", lambda m: self.replace_newline_character(m.group(0), revert=True), new_string, flags=re.DOTALL)    
            return new_string
        return s
        
    def jinja_to_json(self, file_name, transform=False):
        """ convert jinja file to json object without processing variables """
        json_data = None
        try:
            with open(file_name) as fp:
                if transform:
                    json_data = yaml.load(self.comment_jinja_syntax(fp.read()))
                else:
                    json_data = yaml.load(fp.read())
        except Exception as e:
            logger.info("Failed to convert jinja template into json object %s ", str(e))
        return json_data

    def save_json_to_jinja_file(self, json_data, output_file, transform=False):
        """ convert Jinja file to json object """
        try:
            if exists_file(output_file):
                with open(output_file, 'w') as fp:
                    if transform:
                        yaml.dump(json_data, fp, transform=self.revert)
                    else:
                        yaml.dump(json_data, fp)
                    return True
            logger.info("File doesnot exist at given path : %s", output_file)
        except:
            logger.info("Failed to save json data into jinja file")
            logger.error(traceback.format_exc())
        return False