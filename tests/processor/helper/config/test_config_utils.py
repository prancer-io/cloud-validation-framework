import os
import tempfile
import configparser
from processor.helper.config.config_utils import framework_dir, framework_config
from processor.helper.config.config_utils import get_config_data,\
    config_value, get_test_json_dir, framework_currentdata

TESTSDIR = None

def set_tests_dir():
    global TESTSDIR
    if TESTSDIR:
        return TESTSDIR
    MYDIR = os.path.abspath(os.path.dirname(__file__))
    TESTSDIR = os.getenv('FRAMEWORKDIR', os.path.join(MYDIR, '../../../../'))
    return TESTSDIR

set_tests_dir()


def test_framework_dir():
    os.chdir(TESTSDIR)
    tests_curdir = os.getcwd()
    fw_dir = framework_dir()
    os.chdir(fw_dir)
    prod_curdir = os.getcwd()
    assert tests_curdir == prod_curdir


def test_framework_config():
    configini = '%s/realm/config.ini' % TESTSDIR
    with open(configini) as f:
        tests_configini = f.read()
    configfile = framework_config()
    with open(configfile) as f:
        prod_configini = f.read()
    assert tests_configini == prod_configini


def test_rundata_dir():
    tests_rundata = '%s/rundata' % TESTSDIR
    rundata_exists = os.path.exists(tests_rundata) and os.path.isdir(tests_rundata)
    assert rundata_exists == True


def test_get_solution_dir():
    os.chdir(TESTSDIR)
    tests_curdir = os.getcwd()
    os.chdir(framework_dir())
    prod_curdir = os.getcwd()
    assert tests_curdir == prod_curdir


def test_get_config_data():
    configdata = get_config_data(None)
    assert configdata is None
    configdata = get_config_data('/tmp/asdxz.ini')
    assert configdata is None
    tests_configini = '%s/realm/config.ini' % TESTSDIR
    tests_configdata = get_config_data(tests_configini)
    assert tests_configdata is not None
    prod_configdata = get_config_data(framework_config())
    assert prod_configdata is not None
    assert tests_configdata == prod_configdata


def test_config_value():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'ServerAliveInterval': '45', 'Compression': 'yes', 'CompressionLevel': '9'}
    config['bitbucket.org'] = {}
    config['bitbucket.org']['User'] = 'hg'
    config['topsecret.server.com'] = {}
    topsecret = config['topsecret.server.com']
    topsecret['Port'] = '50022'  # mutates the parser
    topsecret['ForwardX11'] = 'no'  # same here
    config['DEFAULT']['ForwardX11'] = 'yes'
    newpath = tempfile.mkdtemp()
    configini = '%s/example.ini' % newpath
    with open(configini, 'w') as configfile:
        config.write(configfile)
    assert configini is not None
    value = config_value('DEFAULT', 'Expansion', configfile='/tmp/axdfe.ini')
    assert value is None
    value = config_value('DEFAULT1', 'Expansion', configfile=configini)
    assert value is None
    value = config_value('DEFAULT', 'Compression', configfile=configini)
    assert value == 'yes'
    value = config_value('DEFAULT', 'Expansion', configfile=configini)
    assert value is None
    value = config_value('DEFAULT', 'Expansion', configfile=configini, default='no')
    assert  value == 'no'
    value = config_value('DEFAULT', 'Expansion', configfile='/tmp/axdfe.ini', default='no')
    assert value == 'no'
    value = config_value('bitbucket.org', 'User', configfile=configini, default='no')
    test_value = 'hg'
    assert test_value == value


def test_get_test_json_dir():
    test_dir = os.getenv('TESTDIR', '/realm/validation/')
    val_dir = '%s/%s' % (TESTSDIR, test_dir)
    os.chdir(val_dir)
    tests_curdir = os.getcwd()
    os.chdir(get_test_json_dir())
    prod_curdir = os.getcwd()
    assert tests_curdir == prod_curdir
