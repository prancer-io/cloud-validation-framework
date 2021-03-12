"""
Run time data storage and retrieval.
"""
import time
import datetime
import json
import socket
import os.path
import shutil
from processor.helper.config.config_utils import config_value, framework_currentdata, get_cache_data, set_cache_data, TESTS, DBTESTS, DBVALUES, SNAPSHOT, SINGLETEST
from processor.helper.json.json_utils import json_from_file, save_json_to_file,get_container_dir
from processor.logging.log_handler import getlogger, FWLOGFILENAME
from processor.helper.file.file_utils import remove_file, exists_dir, mkdir_path

exclude_list = ['token', 'clientSecret', 'vaulttoken','container']

def get_dbtests():
    currdata = get_currentdata()
    if DBTESTS in currdata:
        dbtests = currdata[DBTESTS]
    else:
        nodb = config_value(TESTS, DBTESTS)
        if nodb and nodb.upper() in DBVALUES:
            dbtests = DBVALUES.index(nodb.upper())
        else:
            dbtests = DBVALUES.index(SNAPSHOT)
        put_in_currentdata(DBTESTS, dbtests)
    return dbtests



def add_to_exclude_list(key):
    if key not in exclude_list:
        exclude_list.append(key)


def init_currentdata():
    """ Initialises data structure to store runtime data. """
    started = int(time.time() * 1000)
    runctx = framework_currentdata()
    run_dir = os.path.dirname(runctx)
    if not exists_dir(run_dir):
        mkdir_path(run_dir)
    run_data = {
        'start': started,
        'end': started,
        'errors': [],
        'host': socket.gethostname(),
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_currentdata(run_data)


def put_in_currentdata(key, value):
    """Adds a value in the current run data"""
    if key:
        curr_data = get_currentdata()
        if key in curr_data:
            val = curr_data[key]
            if isinstance(val, list):
                val.append(value)
            else:
                curr_data[key] = value
        else:
            curr_data[key] = value
        save_currentdata(curr_data)

def delete_from_currentdata(key):
    """Remove a key from the current run data"""
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
    """Get the current run data, if present else empty json object"""
    runctx = framework_currentdata()
    curr_data = json_from_file(runctx)
    if not curr_data:
        curr_data = {}
    return curr_data

def put_in_cachedata(key, value):
    """Adds a value in the cache data"""
    if key:
        curr_data = get_cache_data()
        if key in curr_data:
            val = curr_data[key]
            if isinstance(val, list):
                val.append(value)
            else:
                curr_data[key] = value
        else:
            curr_data[key] = value
        set_cache_data(curr_data)

def get_from_cachedata(key):
    """ Get the data for this key from the cachedata"""
    data = None
    currdata = get_cache_data()
    if key and key in currdata:
        data = currdata[key]
    return data


def save_currentdata(curr_data):
    """Save the key value rundata for further access, if None store it empty."""
    if not curr_data:
        curr_data = {}
    runctx = framework_currentdata()
    save_json_to_file(curr_data, runctx)


def delete_currentdata():
    """Delete the rundata file when exiting of the script."""
    logger = getlogger()
    singletest = get_from_currentdata(SINGLETEST)
    if singletest:
        container = get_from_currentdata('container')
        cdir = get_container_dir(container)
        shutil.rmtree('%s/snapshots' % cdir)

    logger.info("END: Completed the run and cleaning up.")
    runctx = get_currentdata()
    runctx['end'] = int(time.time() * 1000)
    runctx['log'] = FWLOGFILENAME
    if 'start' in runctx:
        runctx['duration'] = '%d seconds' % int((runctx['end'] - runctx['start'])/1000)
        runctx['start'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(runctx['start']/1000))
    runctx['end'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(runctx['end']/1000))
    for field in exclude_list:
        if field in runctx:
            del runctx[field]
    logger.critical("\033[92m Run Stats: %s\033[00m" % json.dumps(runctx, indent=2))
    run_file = framework_currentdata()
    remove_file(run_file)


