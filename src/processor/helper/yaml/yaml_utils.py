""" Utility functions for yaml."""

import yaml
from yaml.loader import FullLoader
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
        except:
            pass


def yaml_from_string(yaml_str):
    """Get dict from the string in yaml format."""
    try:
        yamldata = yaml.load(yaml_str, Loader=FullLoader)
        return yamldata
    except:
        print('Failed to load yaml data: %s' % yaml_str)
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
                    yamldata = yaml.load(infile, Loader=FullLoader)
    except Exception as ex:
        print('Failed to load yaml from file: %s, exception: %s' % (yamlfile, ex))
    return yamldata


def valid_yaml(yaml_input):
    """ Checks validity of the yaml """
    try:
        data = yaml.load(yaml_input)
        return isinstance(data, dict)
    except:
        print('Not a valid yaml: %s' % yaml_input)
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
                    yamldata = list(yaml.load_all(infile))
    except Exception as ex:
        return None
    return yamldata

def is_multiple_yaml_file(file_path):
    try:
      if len (multiple_yaml_from_file(file_path,loader=FullLoader)) > 1:
          return True
      else: 
          return False
    except Exception as ex:
        return False

def is_multiple_yaml_convertion(file_path):
    return MultipleConvertionKey in file_path

def is_helm_chart_convertion(file_path):
    return HelmChartConvertionKey in file_path
    