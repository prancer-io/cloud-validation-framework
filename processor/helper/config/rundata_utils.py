"""
   Run time data storage and retrieval.
"""
import time
import datetime
import json
import socket
import os.path
from processor.helper.config.config_utils import RUNCONFIG
from processor.helper.json.json_utils import load_json, dump_json
from processor.logging.log_handler import getlogger, LOGFILENAME
from processor.helper.file.file_utils import delete_file, check_directory, mkdir_parents
exclude_list = ['token', 'clientSecret']


logger = getlogger()


def init_config():
    started = int(time.time() * 1000)
    rundir = os.path.dirname(RUNCONFIG)
    if not check_directory(rundir):
        mkdir_parents(rundir)
    rundata = {
        'start': started,
        'end': started,
        'errors': [],
        'host': socket.gethostname(),
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_run_config(rundata)


def add_to_run_config(key, value):
    if key and value:
        runconfig = get_run_config()
        if key in runconfig:
            val = runconfig[key]
            if isinstance(val, list):
                val.append(value)
            else:
                runconfig[key] = value
        else:
            runconfig[key] = value
        save_run_config(runconfig)


def delete_from_run_config(key):
    if key:
        runconfig = get_run_config()
        if key in runconfig:
            del runconfig[key]
        save_run_config(runconfig)


def get_from_run_config(key):
    """ Get the data for this key from the rundata"""
    data = None
    runconfig = get_run_config()
    if key and key in runconfig:
        data = runconfig[key]
    return data


def get_run_config():
    """Get the current running config, if not present"""
    runconfig = load_json(RUNCONFIG)
    if not runconfig:
        runconfig = {}
    return runconfig


def save_run_config(rundata):
    """Save the key value rundata for further access, if None store it empty."""
    if not rundata:
        rundata = {}
    dump_json(rundata, RUNCONFIG)


def delete_run_config(silent=False):
    """Delete the rundata config file when exiting of the script."""
    if not silent:
        rundata = get_run_config()
        rundata['end'] = int(time.time() * 1000)
        rundata['log'] = LOGFILENAME
        rundata['duration'] = '%d seconds' % int((rundata['end'] - rundata['start'])/1000)
        rundata['start'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rundata['start']/1000))
        rundata['end'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rundata['end']/1000))
        for field in exclude_list:
            if field in rundata:
                del rundata[field]
        logger.info("\033[92m Run Stats: %s\033[00m" % json.dumps(rundata, indent=2))
    delete_file(RUNCONFIG)

