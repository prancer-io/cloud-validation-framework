"""
   Json related utility files.
"""

import json
from collections import OrderedDict
from processor.helper.file.file_utils import check_filename
from processor.helper.config.config_utils import get_parameter_file
from processor.helper.loglib.log_handler import getlogger


logger = getlogger()


def dump_json(json_data, filename):
    """Dump json data in the filename"""
    if json_data:
        with open(filename, 'w') as jsonwrite:
            jsonwrite.write(json.dumps(json_data, indent=2))


def load_json(filename):
    """Load json data from the file."""
    jsondata = None
    try:
        if check_filename(filename):
            with open(filename) as jsonfile:
                jsondata = json.loads(jsonfile.read(), object_pairs_hook=OrderedDict)
    except:
        logger.debug('Failed to load json from file: %s', filename)

    return jsondata


def load_json_input(result):
    """Load json data from the passed str."""
    jsondata = None
    try:
        jsondata = json.loads(result)
    except:
        logger.debug('Failed to load json data: %s', result)
    return jsondata


def is_json(json_input):
    """ Checks the input is json """
    status = True
    try:
        _ = json.loads(json_input)
    except:
        status = False
        logger.debug('Not a valid json: %s', json_input)

    return status


def get_field_value(data, parameter):
    """Utility to get json value from a nested structure."""
    retval = None
    if data and parameter:
        fields = parameter.split('.')
        retval = data
        for field in fields:
            if retval:
                if field in retval:
                    retval = retval[field]
                else:
                    retval = None
    return retval


def set_field_value(json_data, field, value):
    """Set the value for a multiple depth dictionary."""
    data = json_data
    field = field[1:] if field.startswith('.') else field
    flds = field.split('.')
    for idx, fld in enumerate(flds):
        if idx == len(flds) - 1:
            data[fld] = value
        else:
            if fld not in data or not isinstance(data[fld], dict):
                data[fld] = {}
        data = data[fld]


def get_boolean(val):
    """String to boolean type."""
    retval = False
    if val:
        if val.lower() == 'true':
            retval = True
    return retval


def get_vars_json(businessunit, envtype, azureregion, env, filename):
    varsfile = get_parameter_file(businessunit, envtype, azureregion, env, filename)
    logger.debug('Original file: %s', varsfile)
    json_data = load_json(varsfile)
    return varsfile, json_data

