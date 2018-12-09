import pytest
import os
import tempfile
import configparser
from processor.helper.config.config_utils import SOLUTIONDIR, CONFIGINI
from processor.helper.config.config_utils import get_solution_dir, load_config,\
    get_config, get_test_json_dir


TESTSDIR = os.getenv('SOLUTIONDIR',os.path.join(
    os.path.abspath(os.path.dirname(__file__)), '../../../../'))


def test_solution_dir():
    os.chdir(TESTSDIR)
    tests_curdir = os.getcwd()
    os.chdir(SOLUTIONDIR)
    prod_curdir = os.getcwd()
    assert tests_curdir == prod_curdir


def test_config_ini():
    configini = '%s/realm/config.ini' % TESTSDIR
    with open(configini) as f:
        tests_configini = f.read()
    with open(CONFIGINI) as f:
        prod_configini = f.read()
    assert  tests_configini == prod_configini


def test_rundata_dir():
    tests_rundata = '%s/rundata' % TESTSDIR
    rundata_exists = os.path.exists(tests_rundata) and os.path.isdir(tests_rundata)
    assert rundata_exists == True


def test_get_solution_dir():
    os.chdir(TESTSDIR)
    tests_curdir = os.getcwd()
    os.chdir(get_solution_dir())
    prod_curdir = os.getcwd()
    assert tests_curdir == prod_curdir


def test_load_config():
    configdata = load_config(None)
    assert  configdata is None
    configdata = load_config('/tmp/asdxz.ini')
    assert configdata is None
    tests_configini = '%s/realm/config.ini' % TESTSDIR
    tests_configdata = load_config(tests_configini)
    assert tests_configdata is not None
    prod_configdata = load_config(CONFIGINI)
    assert  prod_configdata is not None
    assert tests_configdata == prod_configdata


def test_get_config():
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
    value = get_config('DEFAULT', 'Expansion', configfile='/tmp/axdfe.ini')
    assert value is None
    value = get_config('DEFAULT1', 'Expansion', configfile=configini)
    assert value is None
    value = get_config('DEFAULT', 'Compression', configfile=configini)
    assert value == 'yes'
    value = get_config('DEFAULT', 'Expansion', configfile=configini)
    assert value is None
    value = get_config('DEFAULT', 'Expansion', configfile=configini, default='no')
    assert  value == 'no'
    value = get_config('DEFAULT', 'Expansion', configfile='/tmp/axdfe.ini', default='no')
    assert value == 'no'
    value = get_config('bitbucket.org', 'User', configfile=configini, default='no', parentdir=True)
    test_value = '%s/hg' % SOLUTIONDIR
    assert test_value == value


def test_get_test_json_dir():
    test_dir = os.getenv('TESTDIR', '/realm/azure/validation/')
    val_dir = '%s/%s' % (TESTSDIR, test_dir)
    os.chdir(val_dir)
    tests_curdir = os.getcwd()
    os.chdir(get_test_json_dir())
    prod_curdir = os.getcwd()
    assert tests_curdir == prod_curdir
