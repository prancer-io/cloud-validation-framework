import copy
import os.path
import collections
from tests.conftest import TESTSDIR, data_dict
from processor.helper.yaml.yaml_utils import save_yaml_to_file, yaml_from_string,\
    yaml_from_file, valid_yaml


def test_save_yaml_to_file(create_temp_dir):
    newpath = create_temp_dir()
    fname = '%s/a1.yaml' % newpath
    file_exists = os.path.exists(fname)
    assert False == file_exists
    save_yaml_to_file({}, fname)
    file_exists = os.path.exists(fname)
    assert True == file_exists
    os.remove(fname)
    save_yaml_to_file(None, fname)
    file_exists = os.path.exists(fname)
    assert False == file_exists
    save_yaml_to_file({'a': 'b'}, fname)
    file_exists = os.path.exists(fname)
    assert True == file_exists
    os.remove(fname)
    fname = '%s/a/a1.yaml' % newpath
    file_exists = os.path.exists(fname)
    assert False == file_exists
    save_yaml_to_file({'a':'b'}, fname)
    file_exists = os.path.exists(fname)
    assert False == file_exists


def test_yaml_from_file(create_temp_dir, create_yaml, create_temp_text):
    newpath = create_temp_dir()
    fname = create_temp_text(newpath)
    fullpath = '%s/%s' % (newpath, fname)
    file_exists = os.path.exists(fullpath)
    assert True == file_exists
    yaml_data = yaml_from_file(fullpath)
    assert not isinstance(yaml_data, dict)
    yaml_data = [
        "runtime: python27",
        "api_version: 1",
        "threadsafe: true",
    ]
    fname = create_yaml(newpath, '\n'.join(yaml_data))
    fullpath = '%s/%s' % (newpath, fname)
    file_exists = os.path.exists(fullpath)
    assert True == file_exists
    yaml_data = yaml_from_file(fullpath)
    assert yaml_data is not None
    assert isinstance(yaml_data, dict)
    yaml_data = yaml_from_file(None)
    assert yaml_data is None
    yaml_data = yaml_from_file('/tmp/xyza.yaml')
    assert yaml_data is None
    yaml_data = [
        "hello: ][",
    ]
    fname = create_yaml(newpath, '\n'.join(yaml_data))
    fullpath = '%s/%s' % (newpath, fname)
    yaml_data = yaml_from_file(fullpath)
    assert yaml_data is None

def test_yaml_from_string(create_temp_dir, create_yaml):
    newpath = create_temp_dir()
    yaml_data = [
        "runtime: python27",
        "api_version: 1",
        "threadsafe: true",
    ]
    fname = create_yaml(newpath, '\n'.join(yaml_data))
    fullpath = '%s/%s' % (newpath, fname)
    file_exists = os.path.exists(fullpath)
    assert  True == file_exists
    with open(fullpath) as f:
        data_str = f.read()
    assert data_str is not None
    data = yaml_from_string(data_str)
    assert data is not None
    data_str = 'abcd'
    data = yaml_from_string(data_str)
    assert not isinstance(data, dict)
    data = yaml_from_string(None)
    assert data is None


def test_valid_yaml(create_temp_dir, create_yaml):
    newpath = create_temp_dir()
    yaml_data = [
        "runtime: python27",
        "api_version: 1",
        "threadsafe: true",
    ]
    fname = create_yaml(newpath, '\n'.join(yaml_data))
    fullpath = '%s/%s' % (newpath, fname)
    file_exists = os.path.exists(fullpath)
    assert True == file_exists
    with open(fullpath) as f:
        data_str = f.read()
    assert data_str is not None
    isyaml = valid_yaml(data_str)
    assert True == isyaml
    data_str = 'abcd]['
    isyaml = valid_yaml(data_str)
    assert False == isyaml
    isyaml = valid_yaml(None)
    assert False == isyaml

