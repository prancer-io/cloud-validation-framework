import os
import shutil
from processor.helper.config.rundata_utils import init_config,\
    add_to_run_config, delete_from_run_config, delete_run_config
from processor.helper.config.config_utils import RUNCONFIG


TESTSDIR = os.getenv('SOLUTIONDIR', os.path.join(
    os.path.abspath(os.path.dirname(__file__)), '../../../../'))



def test_init_config():
    rundir = os.path.dirname(RUNCONFIG)
    if os.path.exists(rundir):
        shutil.rmtree(rundir)
    assert False == os.path.exists(rundir)
    assert False == os.path.exists(RUNCONFIG)
    init_config()
    assert True == os.path.exists(rundir)
    assert True == os.path.exists(RUNCONFIG)
    os.remove(RUNCONFIG)
    assert True == os.path.exists(rundir)
    assert False == os.path.exists(RUNCONFIG)
    init_config()
    assert True == os.path.exists(rundir)
    assert True == os.path.exists(RUNCONFIG)


def test_add_to_run_config(load_json_file):
    init_config()
    assert True == os.path.exists(RUNCONFIG)
    add_to_run_config('a', 'val1')
    runconfig = load_json_file(RUNCONFIG)
    result = True if runconfig and 'a' in runconfig and runconfig['a'] == 'val1' else False
    assert result == True
    add_to_run_config('b', ['val1'])
    runconfig = load_json_file(RUNCONFIG)
    result = True if runconfig and 'b' in runconfig and runconfig['b'] == ['val1'] else False
    assert result == True
    add_to_run_config('b', 'val2')
    runconfig = load_json_file(RUNCONFIG)
    result = True if runconfig and 'b' in runconfig and runconfig['b'] == ['val1', 'val2'] else False
    assert result == True


def test_delete_from_run_config(load_json_file):
    init_config()
    assert True == os.path.exists(RUNCONFIG)
    add_to_run_config('a', 'val1')
    runconfig = load_json_file(RUNCONFIG)
    result = True if runconfig and 'a' in runconfig and runconfig['a'] == 'val1' else False
    assert result == True
    delete_from_run_config('a')
    runconfig = load_json_file(RUNCONFIG)
    result = False if runconfig and 'a' in runconfig else True
    assert result == True


def test_delete_run_config():
    init_config()
    assert True == os.path.exists(RUNCONFIG)
    add_to_run_config('token', 'abcd')
    delete_run_config()
    assert False == os.path.exists(RUNCONFIG)
