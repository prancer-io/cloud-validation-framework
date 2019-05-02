import os
import json
import pytest
import tempfile

TESTSDIR = os.getenv('SOLUTIONDIR', os.path.join(
    os.path.abspath(os.path.dirname(__file__)), '../'))
data_dict = {'a': 'b', 'c': {'d': 'e'}, 'f': {'g': {'h': 1}}}
os.environ['UNITTEST'] = "true"


@pytest.fixture
def create_temp_dir():

    def create_test_temp_dir():
        newpath = tempfile.mkdtemp()
        return newpath

    return create_test_temp_dir


@pytest.fixture
def create_temp_json():

    def create_test_temp_json(path, data=data_dict, fname = 'a1.json'):
        # fname = 'a1.json'
        fullname = '%s/%s' % (path, fname)
        with open(fullname, 'w') as f:
            f.write(json.dumps(data, indent=2))
        return fname

    return create_test_temp_json


@pytest.fixture
def create_terraform():

    def create_test_terraform(path, data, fname = 'a1.tfvars'):
        # fname = 'a1.tfvars'
        fullname = '%s/%s' % (path, fname)
        with open(fullname, 'w') as f:
            f.write(data)
        return fname

    return create_test_terraform


@pytest.fixture
def load_json_file():

    def get_json_data(filepath):
        json_data = {}
        if filepath and os.path.exists(filepath):
            with open(filepath) as f:
                try:
                    json_data = json.loads(f.read())
                except:
                    json_data = {}
        return json_data

    return get_json_data


@pytest.fixture
def create_temp_text():

    def create_test_temp_text(path):
        fname = 'a1.txt'
        fullname = '%s/%s' % (path, fname)
        with open(fullname, 'w') as f:
            f.write('abcd')
        return fname

    return create_test_temp_text

