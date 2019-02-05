"""Utility functions for file and  directory"""

import os


def exists_dir(dirname):
    """Check if this path exists and is a directory"""
    if dirname and os.path.exists(dirname) and os.path.isdir(dirname):
        return True
    return False


def exists_file(fname):
    """Check if path exists and is a file"""
    if fname and os.path.exists(fname) and os.path.isfile(fname):
        return True
    return False


def remove_file(fname):
    """Remove the file."""
    try:
        os.remove(fname)
        return True
    except:
        return False


def mkdir_path(dirpath):
    """Make directories recursively."""
    try:
        os.makedirs(dirpath)
        return exists_dir(dirpath)
    except:
        return False
