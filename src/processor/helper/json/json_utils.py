""" Utility functions for json."""

import re
import json
import time
import glob
from json.decoder import JSONDecodeError
from collections import OrderedDict
from processor.helper.file.file_utils import exists_file, exists_dir, mkdir_path
from processor.helper.config.config_utils import get_test_json_dir
from processor.logging.log_handler import getlogger
from bson import json_util

EXCLUSION = 'Exclusion'
SNAPSHOT = 'snapshot'
MASTERSNAPSHOT = 'masterSnapshot'
JSONTEST = 'test'
MASTERTEST = 'mastertest'
TEST = 'test'
OUTPUT = 'output'
STRUCTURE = 'structure'
NOTIFICATIONS = 'notifications'
EXCLUSIONS = 'exclusions'
collectiontypes = {
    TEST: 'TEST',
    STRUCTURE: 'STRUCTURE',
    SNAPSHOT: 'SNAPSHOT',
    MASTERSNAPSHOT: 'MASTERSNAPSHOT',
    MASTERTEST: 'MASTERTEST',
    OUTPUT: 'OUTPUT',
    NOTIFICATIONS: 'NOTIFICATIONS',
    EXCLUSIONS: 'EXCLUSIONS'
}
logger = getlogger()


def store_snapshot(snapshot_dir, data):
    if exists_dir(snapshot_dir):
        snapshot_file = '%s/%s' % (snapshot_dir, data['snapshotId'])
        save_json_to_file(data, snapshot_file)


def make_snapshots_dir(container):
    snapshot_dir = None
    json_dir = '%s%s' % (get_test_json_dir(), container)
    if exists_dir(json_dir):
        snapshot_dir = '%s/snapshots' % json_dir
        mkdir_path(snapshot_dir)
    return snapshot_dir


def save_json_to_file(indata, outfile):
    """Save json data to the file"""
    if indata is not None:
        try:
            instr = json.dumps(indata, indent=2, default=json_util.default)
            with open(outfile, 'w') as jsonwrite:
                jsonwrite.write(instr)
        except:
            pass


def json_from_string(json_str):
    """Get json from the string."""
    try:
        jsondata = json.loads(json_str)
        return jsondata
    except:
        logger.debug('Failed to load json data: %s', json_str)
    return None

def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        if match.group(2) is not None:
            return ""
        else:
            return match.group(1)
    return regex.sub(_replacer, string)


def json_from_file(jsonfile, escape_chars=None, object_pairs_hook=OrderedDict):
    """ Get json data from the file."""
    jsondata = None
    try:
        if exists_file(jsonfile):
            file_data = None
            try:
                with open(jsonfile) as infile:
                    file_data = infile.read()
            except UnicodeDecodeError:
                with open(jsonfile, 'r', encoding='utf-8') as infile:
                    file_data = infile.read()

            if escape_chars and isinstance(escape_chars, list):
                for escape_char in escape_chars:
                    file_data = file_data.replace(escape_char, '\\\%s' % escape_char)
            
            file_data = remove_comments(file_data)    
            try:
                jsondata = json.loads(file_data, object_pairs_hook=object_pairs_hook)
            except JSONDecodeError:
                with open(jsonfile, 'r', encoding='utf-8-sig') as infile:
                    file_data = infile.read()
                    file_data = remove_comments(file_data)
            
            jsondata = json.loads(file_data, object_pairs_hook=object_pairs_hook)
    except Exception as ex:
        logger.debug('Failed to load json from file: %s, exception: %s', jsonfile, ex)
    return jsondata


def valid_json(json_input):
    """ Checks validity of the json """
    try:
        _ = json.loads(json_input)
        return True
    except:
        logger.debug('Not a valid json: %s', json_input)
    return False


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


def get_field_value_with_default(data, parameter, defval):
    """get json value for a nested attribute, else return default value."""
    retval = get_field_value(data, parameter)
    return retval if retval else defval


def get_field_value(data, parameter):
    """get json value for a nested attribute."""
    retval = None
    parameter = parameter[1:] if parameter and parameter.startswith('.') else parameter
    fields = parameter.split('.') if parameter else None
    if data and fields:
        retval = data
        for field in fields:
            match = re.match(r'(.*)\[(\d+)\]', field, re.I)
            if match:
                field, index = match.groups()
                retval = retval[field] if retval and field in retval and isinstance(retval, dict) else None
                i = int(index)
                retval = retval[i] if retval and isinstance(retval, list) and i < len(retval) else None
            else:
                retval = retval[field] if retval and field in retval and isinstance(retval, dict) else None
    return retval


def put_value(json_data, field, value):
    """Put the value for a multiple depth key."""
    data = json_data
    field = field[1:] if field and field.startswith('.') else field
    fields = field.split('.') if field else []
    for idx, fld in enumerate(fields):
        if idx == len(fields) - 1:
            data[fld] = value
        else:
            if fld not in data or not isinstance(data[fld], dict):
                data[fld] = {}
        data = data[fld]


def parse_boolean(val):
    """String to boolean type."""
    return True if val and val.lower() == 'true' else False


def set_timestamp(json_data, fieldname='timestamp'):
    """Set the current timestamp for the object."""
    if not isinstance(json_data, dict):
        return False
    timestamp = int(time.time() * 1000)
    json_data[fieldname] = timestamp
    return True


def get_container_dir(container, tabs=1):
    """Translate container name to container directory"""
    json_test_dir = get_test_json_dir()
    logger.info('%s LOCATION: %s', '\t' * tabs, json_test_dir)
    container_dir = '%s/%s' % (json_test_dir, container)
    container_dir = container_dir.replace('//', '/')
    logger.info('%s COLLECTION: %s', '\t' * tabs, container_dir)
    return container_dir


def get_container_snapshot_json_files(container, mastersnapshot=False):
    """Return list of snapshot files in the container."""
    container_dir = get_container_dir(container)
    if mastersnapshot:
        snapshot_files = get_json_files(container_dir, MASTERSNAPSHOT)
    else:
        snapshot_files = get_json_files(container_dir, SNAPSHOT)
    if not snapshot_files:
        snapshot_files = []
    return container_dir, snapshot_files


def get_json_files(json_dir, file_type):
    """Return list of json files based on the file type."""
    file_list = []
    # logger.info('JSON dir:%s, filetype: %s', json_dir, file_type)
    if json_dir and file_type:
        for filename in glob.glob('%s/*.json' % json_dir.replace('//', '/')):
            json_data = json_from_file(filename)
            if json_data and 'fileType' in json_data and json_data['fileType'] == file_type:
                file_list.append(filename)
    return file_list


def get_container_exclusion_json(container):
    """Return list of exclusion data from a exclusion file in the container."""
    exclusion_data = {}
    container_dir = get_container_dir(container)
    exclusion_files = get_json_files(container_dir, EXCLUSION)
    if exclusion_files:
        exclusion_data = json_from_file(exclusion_files[0])
    return exclusion_data


if __name__ == "__main__":
    json_data = json_from_file("/home/swan-13/Documents/project/prancer/repo-github/cloud-validation-framework/realm/gitConnector.json")
    print(json.dumps(json_data, indent=2))    