import hcl
import hcl2
from processor.logging.log_handler import getlogger

logger = getlogger()

def remove_list_from_values(data):
    if isinstance(data, dict):
        new_data = {}
        for key, values in data.items():
            value = {}
            if isinstance(values, list) and values:
                if len(values) == 1:
                    value = values[0]
                else:
                    for val in values:
                        if isinstance(val, dict):
                            for k, v in val.items():
                                value[k] = v
            else:
                value = values
            value = remove_list_from_values(value)
            new_data[key] = value
        data = new_data
    return data

def hcl_to_json(file_path):
    """
    converts the hcl file to json file
    """
    json_data = {}
    try:
        with open(file_path, 'r') as fp:
            json_data = hcl2.load(fp)
            json_data = remove_list_from_values(json_data)
    except Exception:
        try:
            with open(file_path, 'r') as fp:
                json_data = hcl.load(fp)
        except Exception as e:
            logger.error("Failed to convert hcl to json data, file: %s , error: %s", file_path, str(e))

    return json_data