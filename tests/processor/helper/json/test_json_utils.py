import copy
import os.path
import collections
from tests.conftest import TESTSDIR, data_dict
from processor.helper.json.json_utils import save_json_to_file, json_from_file,\
    json_from_string, valid_json, check_field_exists, get_field_value, put_value,\
    parse_boolean, set_timestamp, get_container_dir, get_container_snapshot_json_files,\
    get_json_files
from processor.reporting.json_output import dump_output_results


def test_save_json_to_file(create_temp_dir):
    newpath = create_temp_dir()
    fname = '%s/a1.json' % newpath
    file_exists = os.path.exists(fname)
    assert False == file_exists
    save_json_to_file({}, fname)
    file_exists = os.path.exists(fname)
    assert True == file_exists
    os.remove(fname)
    save_json_to_file(None, fname)
    file_exists = os.path.exists(fname)
    assert False == file_exists
    save_json_to_file({'a': 'b'}, fname)
    file_exists = os.path.exists(fname)
    assert True == file_exists
    os.remove(fname)
    fname = '%s/a/a1.json' % newpath
    file_exists = os.path.exists(fname)
    assert False == file_exists
    save_json_to_file({'a':'b'}, fname)
    file_exists = os.path.exists(fname)
    assert False == file_exists


def test_json_from_file(create_temp_dir, create_temp_json, create_temp_text):
    newpath = create_temp_dir()
    fname = create_temp_text(newpath)
    fullpath = '%s/%s' % (newpath, fname)
    file_exists = os.path.exists(fullpath)
    assert True == file_exists
    json_data = json_from_file(fullpath)
    assert json_data is None
    fname = create_temp_json(newpath)
    fullpath = '%s/%s' % (newpath, fname)
    file_exists = os.path.exists(fullpath)
    assert True == file_exists
    json_data = json_from_file(fullpath)
    assert json_data is not None
    assert isinstance(json_data, collections.OrderedDict)
    json_data = json_from_file(None)
    assert json_data is None
    json_data = json_from_file('/tmp/xyza.json')
    assert json_data is None


def test_json_from_string(create_temp_dir, create_temp_json):
    newpath = create_temp_dir()
    fname = create_temp_json(newpath)
    fullpath = '%s/%s' % (newpath, fname)
    file_exists = os.path.exists(fullpath)
    assert  True == file_exists
    with open(fullpath) as f:
        data_str = f.read()
    assert data_str is not None
    data = json_from_string(data_str)
    assert data is not None
    data_str = 'abcd'
    data = json_from_string(data_str)
    assert data is None
    data = json_from_string(None)
    assert data is None


def test_valid_json(create_temp_dir, create_temp_json):
    newpath = create_temp_dir()
    fname = create_temp_json(newpath)
    fullpath = '%s/%s' % (newpath, fname)
    file_exists = os.path.exists(fullpath)
    assert True == file_exists
    with open(fullpath) as f:
        data_str = f.read()
    assert data_str is not None
    isjson = valid_json(data_str)
    assert True == isjson
    data_str = 'abcd'
    isjson = valid_json(data_str)
    assert False == isjson
    isjson = valid_json(None)
    assert False == isjson


def test_check_field_exists():
    assert False == check_field_exists(data_dict, None)
    assert False == check_field_exists(None, 'c.d')
    assert False == check_field_exists(data_dict, 'c.d.e')
    assert True == check_field_exists(data_dict, 'a')
    assert True == check_field_exists(data_dict, 'c.d')
    assert True == check_field_exists(data_dict, 'f.g.h')


def test_get_field_value():
    assert None == get_field_value(data_dict, None)
    assert None == get_field_value(None, 'c.d')
    assert None == get_field_value(data_dict, 'c.d.e')
    assert 'b' == get_field_value(data_dict, 'a')
    assert 'e' == get_field_value(data_dict, 'c.d')
    assert 1 == get_field_value(data_dict, 'f.g.h')
    assert {'h': 1} == get_field_value(data_dict, 'f.g')


def test_put_value():
    data_new = copy.deepcopy(data_dict)
    put_value(data_new, 'a.b', 1)
    assert 1 == get_field_value(data_new, 'a.b')
    put_value(data_new, '.a.b', 2)
    assert 2 == get_field_value(data_new, 'a.b')
    put_value(data_new, 'm.n.o', {'a': {'b': 'c'}})
    assert {'a': {'b': 'c'}} == get_field_value(data_new, 'm.n.o')


def test_get_boolean():
    assert False == parse_boolean(None)
    assert False == parse_boolean('False')
    assert True == parse_boolean('true')
    assert True == parse_boolean('TrUE')


def test_set_timestamp():
    assert False == set_timestamp(None)
    assert False == set_timestamp([1,2,3])
    assert True == set_timestamp({})
    time_data = {'a': 1}
    assert True == set_timestamp(time_data)
    ts_exists = True if 'timestamp' in time_data and \
                        time_data['timestamp'] and \
                        isinstance(time_data['timestamp'], int) else False
    assert True == ts_exists
    time_data = {'a': 1}
    assert True == set_timestamp(time_data, 'ts')
    ts_exists = True if 'ts' in time_data and \
                        time_data['ts'] and \
                        isinstance(time_data['ts'], int) else False
    assert True == ts_exists


def skiptest_get_container_dir():
    container = 'container1'
    mytest_dir = '%s/realm/validation/%s' % (TESTSDIR, container)
    os.chdir(mytest_dir)
    mytest_curdir = os.getcwd()
    test_dir = get_container_dir(container)
    os.chdir(test_dir)
    test_curdir = os.getcwd()
    assert mytest_curdir == test_curdir


def test_get_container_snapshot_json_files():
    container = 'container1'
    files = get_container_snapshot_json_files(container)
    assert files is not None


def skiptest_get_json_files():
    container = 'container1'
    mytest_dir = '%s/realm/validation/%s' % (TESTSDIR, container)
    files = get_json_files(mytest_dir, 'snapshot')
    assert True == isinstance(files, list)
    files = get_json_files(mytest_dir, 'test')
    assert True == isinstance(files, list) and len(files) > 0
    files = get_json_files('/a/b/c', 'txt')
    assert True == isinstance(files, list)


def skiptest_dump_output_results():
    container = 'container1'
    test_file = '%s/realm/validation/%s/test1.json' % (TESTSDIR, container)
    outputtest_file = '%s/realm/validation/%s/output-test1.json' % (TESTSDIR, container)
    file_exists = os.path.exists(outputtest_file)
    if file_exists:
        os.remove(outputtest_file)
    dump_output_results([], container, test_file, 'snapshot')
    file_exists = os.path.exists(outputtest_file)
    assert True == file_exists
    os.remove(outputtest_file)
