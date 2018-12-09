"""
   File and directory utils.
"""

import os


def check_directory(dirname):
    """Check if it is a directory, then further actions on the directory"""
    if not dirname or not os.path.exists(dirname) or not os.path.isdir(dirname):
        return False
    return True


def check_filename(filename):
    """Check the file if exists before any further operations on it"""
    if not filename or not os.path.exists(filename) or not os.path.isfile(filename):
        return False
    return True


def delete_file(filename):
    """Delete filename, not checking the existence of the file."""
    try:
        os.remove(filename)
        return True
    except:
        return False
