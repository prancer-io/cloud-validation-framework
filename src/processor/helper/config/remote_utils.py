"""Remote Configuration utilities"""
import configparser
import os
import datetime
import subprocess
from urllib import request
from inspect import currentframe, getframeinfo

from processor.helper.file.file_utils import exists_file, exists_dir, mkdir_path
from processor.helper.config.config_utils import COMPLIANCE, CRAWL, CRAWL_AND_COMPLIANCE, framework_dir, config_value, framework_config, \
    CFGFILE, get_config_data

def console_log(message, cf):
    """Logger like statements only used till logger configuration is read and initialized."""
    filename = getframeinfo(cf).filename
    line = cf.f_lineno
    now = datetime.datetime.now()
    fmtstr = '%s,%s(%s: %3d) %s' % (now.strftime('%Y-%m-%d %H:%M:%S'), str(now.microsecond)[:3],
                                    os.path.basename(filename).replace('.py', ''), line, message)
    print(fmtstr)


def remote_config_ini_setup():
    """Need the config.ini file to read initial configuration data"""
    error = False
    config_ini = None
    fwdir = os.getenv('FRAMEWORKDIR', None)
    if fwdir:
        if exists_dir(fwdir):
            config_ini = '%s/%s' % (fwdir, CFGFILE)
            if exists_file(config_ini):
                config_data = get_config_data(config_ini)
                if config_data:
                    pass
                else:
                    console_log("Configuration(%s) INI file is invalid, correct it and try again!" % config_ini, currentframe())
                    error = True
            else:
                console_log("Configuration(%s) INI file does not exist, creating it!" % config_ini, currentframe())
                create_remote_config(config_ini)
        else:
            console_log("FRAMEWORKDIR: %s, env variable set to non-existent directory, exiting....." % fwdir, currentframe())
            error = True
    else:
        fwdir = os.getcwd()
        config_ini = '%s/%s' % (fwdir, CFGFILE)
        if exists_file(config_ini):
            config_data = get_config_data(config_ini)
            if config_data:
                pass
            else:
                console_log("Configuration(%s) INI file is invalid, correct it and try again!" % config_ini, currentframe())
                error = True
        else:
            console_log("Configuration(%s) INI file does not exist, creating it!" % config_ini, currentframe())
            create_remote_config(config_ini)

    if not error:
        opapresent = check_exe_in_path_and_curdir(config_ini, 'OPA', 'opaexe', 'opa')
        if not opapresent:
            console_log("opa binary required, not present in path or current directory, exiting...", currentframe())
            error = True
        if not error:
            helmpresent = check_exe_in_path_and_curdir(config_ini, 'HELM', 'helmexe', 'helm')
            if not helmpresent:
                console_log("helm binary required, not present in path or current directory, exiting...", currentframe())
                error = True
    if not error:
        get_azure_api_versions_from_github(config_ini, fwdir)
    return error, config_ini

def check_exe_in_path_and_curdir(config_ini, section, field, defaultexe):
    exename = config_value(section, field, configfile=config_ini)
    exepresent = False
    try:
        subprocess.Popen([exename, "version"], stdout=subprocess.DEVNULL)
        exepresent = True
    except FileNotFoundError:
        pass
    if not exepresent:
        curexe=os.getcwd() + os.sep + defaultexe
        try:
            subprocess.Popen([curexe, "version"], stdout=subprocess.DEVNULL)
            exepresent = True
        except FileNotFoundError:
            pass
    return exepresent

def get_azure_api_versions_from_github(config_ini, fwdir):
    apiversion = config_value('AZURE', 'api', configfile=config_ini)
    if apiversion:
        apifile = fwdir + os.sep + apiversion
    else:
        azpath = config_value('AZURE', 'azurestructurefolder', configfile=config_ini)
        apiversion = 'azureApiVersions.json'
        apifile = fwdir + os.sep + azpath + os.sep + apiversion
    apifile = apifile.replace('//', '/')
    if not exists_file(apifile):
        url='https://github.com/prancer-io/cloud-validation-framework/raw/master/realm/azureApiVersions.json'
        urlresp = request.urlopen(url)
        respdata = urlresp.read()
        respdata = respdata.decode()
        with open(apifile, 'w') as apif:
            apif.write(respdata)


def create_remote_config(config_ini):
    cdata = {
        'LOGGING': {
            'level': 'ERROR',
            'propagate': True,
            'logFolder': 'log'
        },
        'REPORTING': {
            'reportOutputFolder':  './validation/'
        },
        'TESTS': {
            'containerFolder':  './validation/',
            'database': 'NONE'
        },
        'GIT': {
            'parameterStructureFolder': './'
        },
        'AZURE': {
            'api': './azureApiVersions.json',
            'azureStructureFolder': '.'
        },
        'OPA': {
            'opa': True,
            'opaexe': 'opa'
        },
        'HELM': {
            'helmexe': 'helm'
        }
    }
    cfgparser = configparser.ConfigParser(allow_no_value=True)
    cfgparser.read_dict(cdata)
    with open(config_ini, 'w') as configfile:
        cfgparser.write(configfile)