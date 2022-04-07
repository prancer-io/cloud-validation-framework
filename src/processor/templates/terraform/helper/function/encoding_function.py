"""
Performs all in built encoding functions which are supported by terraform processor
"""
import json
from processor.helper.json.json_utils import json_from_string
from processor.logging.log_handler import getlogger

logger = getlogger()

def jsonencode(json_str):
    """ convert string json representation to json format """
    if isinstance(json_str, dict):
        # NOTE: convertion from string to json is already done in processor
        return json_str
    return json.loads(json_str)

def jsondecode(json_str):
    """ convert string json representation to json format """    
    if isinstance(json_str, dict):
        # NOTE: convertion from string to json is already done in processor
        return json_str
    return json.loads(json_str)