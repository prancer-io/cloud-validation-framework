import codecs
import hcl
import hcl2
from lark import tree
from processor.helper.hcl import parser
from processor.logging.log_handler import getlogger

logger = getlogger()

def hcl_to_json(file_path):
    """
    converts the hcl file to json file
    """
    json_data = {}
    try:
        with open(file_path, 'r', encoding="utf-8") as fp:
            json_data = parser.loads(fp)
    except Exception as e:
        try:
            with codecs.open(file_path, "r", encoding="utf-8-sig") as fp:
                json_data = parser.loads(fp)
        except Exception as e:
            error = str(e)
            error = error.split("Expected one of")[0]
            logger.debug("Unspported terraform file, error while parsing file: %s , error: %s", file_path, error)

    return json_data

if __name__ == "__main__":
    json_data = hcl_to_json("/tmp/extrasg.tf")
    import json
    print(json.dumps(json_data, indent=2))

