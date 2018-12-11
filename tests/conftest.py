import os
import pytest
import tempfile

TESTSDIR = os.getenv('SOLUTIONDIR', os.path.join(
    os.path.abspath(os.path.dirname(__file__)), '../'))

@pytest.fixture
def create_temp_dir():

    def create_test_temp_dir():
        newpath = tempfile.mkdtemp()
        return newpath

    return create_test_temp_dir

