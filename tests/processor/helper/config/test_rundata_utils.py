import os
import shutil
from processor.helper.config.rundata_utils import init_currentdata,\
    put_in_currentdata, delete_from_currentdata, delete_currentdata
from processor.helper.config.config_utils import framework_currentdata


TESTSDIR = None


def set_tests_dir():
    global TESTSDIR
    if TESTSDIR:
        return TESTSDIR
    MYDIR = os.path.abspath(os.path.dirname(__file__))
    TESTSDIR = os.getenv('FRAMEWORKDIR', os.path.join(MYDIR, '../../../../'))
    return TESTSDIR

set_tests_dir()


def test_init_config():
    runcfg = framework_currentdata()
    rundir = os.path.dirname(runcfg)
    if os.path.exists(rundir):
        shutil.rmtree(rundir)
    assert False == os.path.exists(rundir)
    assert False == os.path.exists(runcfg)
    init_currentdata()
    assert True == os.path.exists(rundir)
    assert True == os.path.exists(runcfg)
    os.remove(runcfg)
    assert True == os.path.exists(rundir)
    assert False == os.path.exists(runcfg)
    init_currentdata()
    assert True == os.path.exists(rundir)
    assert True == os.path.exists(runcfg)


def test_add_to_run_config(load_json_file):
    runcfg = framework_currentdata()
    init_currentdata()
    assert True == os.path.exists(runcfg)
    put_in_currentdata('a', 'val1')
    runconfig = load_json_file(runcfg)
    result = True if runconfig and 'a' in runconfig and runconfig['a'] == 'val1' else False
    assert result == True
    put_in_currentdata('b', ['val1'])
    runconfig = load_json_file(runcfg)
    result = True if runconfig and 'b' in runconfig and runconfig['b'] == ['val1'] else False
    assert result == True
    put_in_currentdata('b', 'val2')
    runconfig = load_json_file(runcfg)
    result = True if runconfig and 'b' in runconfig and runconfig['b'] == ['val1', 'val2'] else False
    assert result == True


def test_delete_from_run_config(load_json_file):
    runcfg = framework_currentdata()
    init_currentdata()
    assert True == os.path.exists(runcfg)
    put_in_currentdata('a', 'val1')
    runconfig = load_json_file(runcfg)
    result = True if runconfig and 'a' in runconfig and runconfig['a'] == 'val1' else False
    assert result == True
    delete_from_currentdata('a')
    runconfig = load_json_file(runcfg)
    result = False if runconfig and 'a' in runconfig else True
    assert result == True


def test_delete_run_config():
    runcfg = framework_currentdata()
    init_currentdata()
    assert True == os.path.exists(runcfg)
    put_in_currentdata('token', 'abcd')
    delete_currentdata()
    assert False == os.path.exists(runcfg)
