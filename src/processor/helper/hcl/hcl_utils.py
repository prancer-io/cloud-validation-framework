import hcl
from processor.logging.log_handler import getlogger

logger = getlogger()

def hcl_to_json(file_path):
    """
    converts the hcl file to json file
    """
    json_data = {}
    try:
        with open(file_path, 'r') as fp:
            json_data = hcl.load(fp)
    except Exception as e:
        logger.error("Failed to convert hcl to json data, file: %s , error: %s", file_path, str(e))
    return json_data