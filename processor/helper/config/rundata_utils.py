"""
   Run time data storage and retrieval.
"""
import time
import datetime
import json
import socket
import os.path
from processor.helper.config.config_utils import framework_currentdata
from processor.helper.json.json_utils import json_from_file, save_json_to_file
from processor.logging.log_handler import getlogger, FWLOGFILENAME
from processor.helper.file.file_utils import remove_file, exists_dir, mkdir_path
exclude_list = ['token', 'clientSecret']


logger = getlogger()


def init_currentdata():
    started = int(time.time() * 1000)
    runcfg = framework_currentdata()
    rundir = os.path.dirname(runcfg)
    if not exists_dir(rundir):
        mkdir_path(rundir)
    rundata = {
        'start': started,
        'end': started,
        'errors': [],
        'host': socket.gethostname(),
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_currentdata(rundata)


def put_in_currentdata(key, value):
    if key and value:
        currdata = get_currentdata()
        if key in currdata:
            val = currdata[key]
            if isinstance(val, list):
                val.append(value)
            else:
                currdata[key] = value
        else:
            currdata[key] = value
        save_currentdata(currdata)


def delete_from_currentdata(key):
    if key:
        currdata = get_currentdata()
        if key in currdata:
            del currdata[key]
        save_currentdata(currdata)


def get_from_currentdata(key):
    """ Get the data for this key from the rundata"""
    data = None
    currdata = get_currentdata()
    if key and key in currdata:
        data = currdata[key]
    return data


def get_currentdata():
    """Get the current currentdata, if present"""
    runcfg = framework_currentdata()
    currdata = json_from_file(runcfg)
    if not currdata:
        currdata = {}
    return currdata


def save_currentdata(currdata):
    """Save the key value rundata for further access, if None store it empty."""
    if not currdata:
        currdata = {}
    runcfg = framework_currentdata()
    save_json_to_file(currdata, runcfg)


def delete_currentdata():
    """Delete the rundata config file when exiting of the script."""
    rundata = get_currentdata()
    rundata['end'] = int(time.time() * 1000)
    rundata['log'] = FWLOGFILENAME
    rundata['duration'] = '%d seconds' % int((rundata['end'] - rundata['start'])/1000)
    rundata['start'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rundata['start']/1000))
    rundata['end'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rundata['end']/1000))
    for field in exclude_list:
        if field in rundata:
            del rundata[field]
    logger.info("\033[92m Run Stats: %s\033[00m" % json.dumps(rundata, indent=2))
    runcfg = framework_currentdata()
    remove_file(runcfg)

