"""
   Configuration related utilities
"""
import configparser
import os
from processor.helper.file.file_utils import check_filename

SOLUTIONDIR = os.getenv('SOLUTIONDIR', os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                    '../../../'))
CONFIGINI = '%s/configdata/config.ini' % SOLUTIONDIR
RUNCONFIG = '%s/rundata/rundata' % SOLUTIONDIR


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


def get_subscription_file(parentdir=False):
    env_parameter_file = os.getenv('SUBSCRIPTION', None)
    if env_parameter_file:
        file_path = '%s/%s' % (SOLUTIONDIR, env_parameter_file)
        parameter_file = file_path if parentdir else env_parameter_file
    else:
        parameter_file = get_config('DEFAULT', 'subscription', parentdir=parentdir)
    return parameter_file.replace('//', '/')


def get_config(section, key, configfile=CONFIGINI, default=None, parentdir=False):
    """Get config key from the given section"""
    config = load_config(configfile)
    retval = default
    if config and section in config:
        retval = config.get(section, key)
    if retval and parentdir:
        return '%s/%s' % (SOLUTIONDIR, retval)
    return retval


def get_parameter_file(businessunit, envtype, azureregion, env, filename):
    """ Create the absolute path for the filename based on the input parameters."""
    soln_dir = get_solution_dir()
    parameterfile = '%s/realm/azure/%s/%s/%s/%s/%s' % (soln_dir, businessunit, envtype,
                                                      azureregion, env, filename)
    return parameterfile.replace('//', '/')


def main():
    print(get_config_ini())
    sol_dir = get_solution_dir()
    print(sol_dir)
    cfg_file = '%s/configdata/config.ini' % sol_dir
    print(cfg_file)
    sub_file = get_subscription_file()
    print(sub_file)
    filename = '%s/%s' % (sol_dir, sub_file)
    print(filename)
    print(get_parameter_file('abc', 'nonprod', 'eastus2', 'shared', 'test1.json'))
    print(get_config('DEFAULT', 'subscription'))


if __name__ == "__main__":
    main()

