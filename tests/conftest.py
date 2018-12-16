import os
import json
import pytest
import tempfile

TESTSDIR = os.getenv('SOLUTIONDIR', os.path.join(
    os.path.abspath(os.path.dirname(__file__)), '../'))
data_dict = {'a': 'b', 'c': {'d': 'e'}, 'f': {'g': {'h': 1}}}


@pytest.fixture
def create_temp_dir():

    def create_test_temp_dir():
        newpath = tempfile.mkdtemp()
        return newpath

    return create_test_temp_dir


@pytest.fixture
def create_temp_json():

    def create_test_temp_json(path, data=data_dict):
        fname = 'a1.json'
        fullname = '%s/%s' % (path, fname)
        with open(fullname, 'w') as f:
            f.write(json.dumps(data, indent=2))
        return fname

    return create_test_temp_json

