import pytest
import os.path
import tempfile
from processor.helper.file.file_utils import check_directory
from processor.helper.file.file_utils import check_filename
from processor.helper.file.file_utils import delete_file


def mock_dirs():
    return ['/tmp', '~/tmp', '~/abc']


def mock_filenames():
    return ['/tmp/a', '~/tmp/a.txt', '~/abc/b.ini']


def mock_exists_file_check(fname):
    fnames = mock_filenames()
    return True if fname in fnames else False


def mock_is_file_check(fname):
    fnames = mock_filenames()
    return True if fname in fnames else False


def mock_exists_dir_check(dirname):
    dirs = mock_dirs()
    return True if dirname in dirs else False


def mock_is_dir_check(dirname):
    dirs = mock_dirs()
    return True if dirname in dirs else False


@pytest.fixture
def create_temp_file():

    def create_test_file(fname):
        newpath = tempfile.mkdtemp()
        os.chdir(newpath)
        with open(fname, 'w') as f:
            f.write('hello')
        return '%s/%s' % (newpath, fname)

    return create_test_file


def test_none_directory():
    assert False == check_directory(None)


def test_dir_exists(monkeypatch):
    monkeypatch.setattr(os.path, 'exists', mock_exists_dir_check)
    monkeypatch.setattr(os.path, 'isdir', mock_is_dir_check)
    assert True == check_directory('/tmp')
    assert False == check_directory('/xyz')


def test_none_file():
    assert False == check_filename(None)


def test_file_exists(monkeypatch):
    monkeypatch.setattr(os.path, 'exists', mock_exists_file_check)
    monkeypatch.setattr(os.path, 'isfile', mock_is_file_check)
    assert True == check_filename('/tmp/a')
    assert False == check_filename('/tmp/b')


def test_delete_file(create_temp_file):
    fname = create_temp_file('a.txt')
    assert True == delete_file(fname)
    assert False == delete_file('/tmp/axzs')
