import pytest
import os.path
import tempfile
from processor.helper.file.file_utils import exists_dir
from processor.helper.file.file_utils import exists_file
from processor.helper.file.file_utils import remove_file
from processor.helper.file.file_utils import mkdir_path


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


def test_none_directory():
    assert False == exists_dir(None)


def test_exists_dir(monkeypatch):
    monkeypatch.setattr(os.path, 'exists', mock_exists_dir_check)
    monkeypatch.setattr(os.path, 'isdir', mock_is_dir_check)
    assert True == exists_dir('~/tmp')
    assert True == exists_dir('~/abc')
    assert False == exists_dir('/xyz')


def test_none_file():
    assert False == exists_file(None)


def test_exists_file(monkeypatch):
    monkeypatch.setattr(os.path, 'exists', mock_exists_file_check)
    monkeypatch.setattr(os.path, 'isfile', mock_is_file_check)
    assert True == exists_file('/tmp/a')
    assert False == exists_file('/tmp/b')


def test_remove_file(create_temp_file):
    fname = create_temp_file('a.txt')
    assert True == remove_file(fname)
    assert False == remove_file('/tmp/axzs')


def ignoretest_mkdir_path(create_temp_dir):
    newpath = create_temp_dir()
    assert True == mkdir_path('%s/a/b/c' % newpath)
    assert False == mkdir_path('/a/b/c')