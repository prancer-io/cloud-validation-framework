""" Utility functions for yaml."""

import yaml
from yaml.loader import SafeLoader
from collections import OrderedDict
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger

logger = getlogger()
MultipleConvertionKey = "_multiple_yaml"
HelmChartConvertionKey = "_prancer_helm_template"

def save_yaml_to_file(indata, outfile, indent=None):
    """Save dict data to the file in yaml format"""
    if indata is not None:
        try:
            with open(outfile, 'w') as yamlfile:
                yaml.dump(indata, yamlfile, indent=indent)
        except Exception as e:
            logger.error("Error saving yaml to file %s: %s", outfile, str(e))


def yaml_from_string(yaml_str):
    """Get dict from the string in yaml format."""
    try:
        yamldata = yaml.safe_load(yaml_str)
        return yamldata
    except Exception as e:
        logger.error('Failed to load yaml data: %s, error: %s', yaml_str, str(e))
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
                    yamldata = yaml.safe_load(infile)
    except Exception as ex:
        print('Failed to load yaml from file: %s, exception: %s' % (yamlfile, ex))
    return yamldata


def valid_yaml(yaml_input):
    """ Checks validity of the yaml """
    try:
        data = yaml.safe_load(yaml_input)
        return isinstance(data, dict)
    except Exception as e:
        logger.warning('Not a valid yaml: %s, error: %s', yaml_input, str(e))
    return False

def multiple_yaml_from_file(yamlfile, loader=None):
    """ Get multiple yaml data from the file in a dict."""
    yamldata = None
    try:
        if exists_file(yamlfile):
            with open(yamlfile) as infile:
                if loader:
                    yamldata = list(yaml.load_all(infile, Loader=loader))
                else:
                    yamldata = list(yaml.safe_load_all(infile))
    except Exception as ex:
        return None
    return yamldata

def is_multiple_yaml_file(file_path):
    try:
      if len (multiple_yaml_from_file(file_path,loader=SafeLoader)) > 1:
          return True
      else: 
          return False
    except Exception as ex:
        return False

def is_multiple_yaml_convertion(file_path):
    return MultipleConvertionKey in file_path

def is_helm_chart_convertion(file_path):
    return HelmChartConvertionKey in file_path
    