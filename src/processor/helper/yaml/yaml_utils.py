""" Utility functions for yaml."""

import yaml
from collections import OrderedDict
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger

logger = getlogger()


def save_yaml_to_file(indata, outfile, indent=None):
    """Save dict data to the file in yaml format"""
    if indata is not None:
        try:
            with open(outfile, 'w') as yamlfile:
                yaml.dump(indata, yamlfile, indent=indent)
        except:
            pass


def yaml_from_string(yaml_str):
    """Get dict from the string in yaml format."""
    try:
        yamldata = yaml.load(yaml_str)
        return yamldata
    except:
        print('Failed to load yaml data: %s', yaml_str)
    return None


def yaml_from_file(yamlfile, loader=None):
    """ Get yaml data from the file in a dict."""
    yamldata = None
    try:
        if exists_file(yamlfile):
            with open(yamlfile) as infile:
                if loader:
                    yamldata = yaml.load(infile, Loader=loader)
                else:
                    yamldata = yaml.load(infile)
    except Exception as ex:
        print('Failed to load yaml from file: %s, exception: %s', yamlfile, ex)
    return yamldata


def valid_yaml(yaml_input):
    """ Checks validity of the yaml """
    try:
        data = yaml.load(yaml_input)
        return isinstance(data, dict)
    except:
        print('Not a valid yaml: %s', yaml_input)
    return False

