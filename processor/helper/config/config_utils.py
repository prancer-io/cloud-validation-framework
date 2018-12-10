"""
   Configuration related utilities
"""
import configparser
import os
from processor.helper.file.file_utils import check_filename

SOLUTIONDIR = os.getenv('SOLUTIONDIR',
                        os.path.join(
                            os.path.abspath(os.path.dirname(__file__)),
                            '../../../'))
CONFIGINI = '%srealm/config.ini' % SOLUTIONDIR
RUNCONFIG = '%srundata/rundata' % SOLUTIONDIR
DATABASE = 'MONGODB'
DBNAME = 'dbname'


def get_config_ini():
    """utility method to return the config ini file."""
    return CONFIGINI


def get_solution_dir():
    """Return top level config directory"""
    return SOLUTIONDIR


def load_config(config_file):
    """Load config file in ini format"""
    config = None
    if check_filename(config_file):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(config_file)
    return config


def get_config(section, key, configfile=CONFIGINI, default=None, parentdir=False):
    """Get config key from the given section"""
    config = load_config(configfile)
    retval = default
    if config and section in config:
        retval = config.get(section, key, fallback=default)
    if retval and parentdir:
        return '%s/%s' % (SOLUTIONDIR, retval)
    return retval


def get_test_json_dir():
    """ Path to check and run the tests from the test containers."""
    soln_dir = get_solution_dir()
    env_test_dir = os.getenv('TESTDIR', None)
    if not env_test_dir:
        env_test_dir = "/realm/azure/validation/"
    test_path = '%s/%s' % (soln_dir, env_test_dir)
    return test_path.replace('//', '/')


# def main():
#     print(get_config_ini())
#     sol_dir = get_solution_dir()
#     print(sol_dir)
#     cfg_file = '%srealm/config.ini' % sol_dir
#     print(cfg_file)
#     cfg_data = load_config(cfg_file)
#     print(cfg_data)
#     print(get_config('DEFAULT', 'subscription'))
#
#
# if __name__ == "__main__":
#     main()

