"""
   Json related utility files.
"""

import json
import time
import glob
from collections import OrderedDict
from processor.helper.file.file_utils import check_filename
from processor.helper.config.config_utils import get_test_json_dir
from processor.logging.log_handler import getlogger

SNAPSHOT = 'snapshot'
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


def check_field_exists(data, parameter):
    """Utility to check json field is present."""
    present = False
    if data and parameter:
        fields = parameter.split('.')
        curdata = data
        if fields:
            allfields = True
            for field in fields:
                if curdata:
                    if field in curdata and isinstance(curdata, dict):
                        curdata = curdata[field]
                    else:
                        allfields = False
            if allfields:
                present = True
    return present


def get_field_value(data, parameter):
    """Utility to get json value from a nested structure."""
    retval = None
    if data and parameter:
        fields = parameter.split('.')
        retval = data
        for field in fields:
            if retval:
                if field in retval and isinstance(retval, dict):
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


def set_timestamp(json_data, fieldname='timestamp'):
    """Set the current timestamp for the object."""
    if not isinstance(json_data, dict):
        return False
    timestamp = int(time.time() * 1000)
    json_data[fieldname] = timestamp
    return True


def get_container_dir(container):
    json_test_dir = get_test_json_dir()
    container_dir = '%s/%s' % (json_test_dir, container)
    container_dir = container_dir.replace('//', '/')
    logger.info(container_dir)
    return container_dir


def get_container_snapshot_json_files(container):
    container_dir = get_container_dir(container)
    snapshot_files = get_json_files(container_dir, SNAPSHOT)
    return container_dir, snapshot_files


def get_json_files(json_dir, filetype):
    file_list = []
    if json_dir and filetype:
        for filename in glob.glob('%s/*.json' % json_dir.replace('//', '/')):
            json_data = load_json(filename)
            if json_data and 'fileType' in json_data and json_data['fileType'] == filetype:
                file_list.append(filename)
    return file_list


def dump_output_results1(results, test_file, container):
    test_file_parts = test_file.rsplit('/', 1)
    output_file = '%s/%s/output-%s' % (get_test_json_dir(), container, test_file_parts[-1])
    od = OrderedDict()
    od["$schema"] =  ""
    od["contentVersion"]  = "1.0.0.0"
    od["fileType"] = "output"
    od["timestamp"] = ""
    od["snapshot"] = "snapshot.json"
    od["test"] = test_file_parts[-1]
    od["container"] = container
    od["results"] = results
    dump_json(od, output_file)





