"""Framework Configuration utilities"""
import configparser
import os
from processor.helper.file.file_utils import exists_file, exists_dir

FRAMEWORKDIR = None
FRAMEWORKCONFIG = None
CURRENTDATA = None
DATABASE = 'MONGODB'
TESTS = 'TESTS'
DBTESTS = 'database'
DBNAME = 'dbname'
DBURL = 'dburl'
CFGFILE = 'config.ini'
NONE = 'NONE'
SNAPSHOT = 'SNAPSHOT'
FULL = 'FULL'
DBVALUES = [NONE, SNAPSHOT, FULL]


def parseint(value, default=0):
    intvalue = default
    try:
        intvalue = int(value)
    except:
        pass
    return intvalue


def parsebool(val, defval=False):
    "Parse boolean from the input value"
    retval = defval
    if val:
        if isinstance(val, str) and val.lower() in ['false', 'true']:
            retval = True if val.lower() == 'true' else False
        else:
            retval = bool(parseint(val))
    return retval


def framework_currentdata():
    """Return the framework current data."""
    global CURRENTDATA
    if CURRENTDATA:
        return CURRENTDATA
    CURRENTDATA = '%s/rundata' % framework_dir()
    return CURRENTDATA


def framework_config():
    """Return the framework config file."""
    global FRAMEWORKCONFIG
    if FRAMEWORKCONFIG:
        return FRAMEWORKCONFIG
    FRAMEWORKCONFIG = '%s/%s' % (framework_dir(), CFGFILE)
    return FRAMEWORKCONFIG


def framework_dir():
    """Return top level framework directory"""
    global FRAMEWORKDIR
    if FRAMEWORKDIR:
        return FRAMEWORKDIR
    fwdir = os.getenv('FRAMEWORKDIR', None)
    if fwdir and exists_dir(fwdir):
        FRAMEWORKDIR = fwdir
    else:
        FRAMEWORKDIR = os.getcwd()
    return FRAMEWORKDIR


def get_config_data(config_file):
    """Return config data from the config file."""
    config_data = None
    if exists_file(config_file):
        config_data = configparser.ConfigParser(allow_no_value=True)
        config_data.read(config_file)
    return config_data


def config_value(section, key, configfile=None, default=None):
    """Get value for the key from the given config section"""
    if not configfile:
        configfile = framework_config()
    config_data = get_config_data(configfile)
    if config_data and section in config_data:
        return config_data.get(section, key, fallback=default)
    return default


def get_test_json_dir():
    """ Path to check and run the tests from the test containers."""
    fw_dir = framework_dir()
    env_test_dir = config_value('TESTS', 'containerFolder')
    test_path = '%s/%s' % (fw_dir, env_test_dir)
    return test_path.replace('//', '/')


def container_exists(container):
    """ Check if the container directory exists"""
    container_dir = '%s/%s' % (get_test_json_dir(), container)
    return True if exists_dir(container_dir) else False
