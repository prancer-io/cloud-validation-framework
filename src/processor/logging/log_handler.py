"""Helper functions to setup logging for the framework."""
import logging
from logging.handlers import RotatingFileHandler
import datetime
import time
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


FWLOGGER = None
FWLOGFILENAME = None
MONGOLOGGER = None
DBLOGGER = None
dbhandler = None
# LOGFORMAT = '%(asctime)s(%(module)s:%(lineno)4d) - %(message)s'
LOGFORMAT = '%(asctime)s - %(message)s'


def get_dblog_name():
    """ Set as per current datetime formay, could be passed thru an environment variable"""
    dblog_name = os.getenv('DBLOG_NAME', None)
    if not dblog_name:
        dblog_name = 'logs_%s' % datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return dblog_name


def get_loglevel(fwconf=None):
    """ Highest priority is at command line, then ini file otherwise default is INFO"""
    loglevels = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
    level = os.getenv('LOGLEVEL', None)
    loglevel = level if level and level in loglevels else None
    cfglevel = fwconf['level'].upper() if fwconf and 'level' in fwconf and fwconf['level'] and fwconf['level'].upper() in \
                                          loglevels else None
    if loglevel:
        return loglevel
    elif cfglevel:
        return cfglevel
    else:
        return logging.INFO


class MongoDBHandler(logging.Handler):
    """Customized logging handler that puts logs to the database, pymongo required
    """
    def __init__(self, dburl, dbname, collection='logs'):
        logging.Handler.__init__(self)
        try:
            dbconnection =  MongoClient(host=dburl, serverSelectionTimeoutMS=3000)
            _ = dbconnection.list_database_names()
            if dbname:
                db = dbconnection[dbname]
            else:
                db = dbconnection['test']
            # Collection where the log statements are being put in.
            self.coll_name = collection
            # Every run of the prancer-basic will have a log name associated with it.
            self.log_name = ''
            if db:
                self.db = db
                self.set_log_collection()
            else:
                self.collection = None
        except ServerSelectionTimeoutError as ex:
            self.collection = None

    def set_log_collection(self):
        global DBLOGGER
        self.collection = self.db[self.coll_name]
        DBLOGGER = get_dblog_name()
        self.dblog_name = DBLOGGER
        self.collection.insert({'name': self.dblog_name, 'logs': []}, check_keys=False)

    def get_log_collection(self):
        return self.dblog_name

    def reset_log_collection(self):
        self.dblog_name = ''

    def emit(self, record):
        """Add record to the database"""
        # format the log message so it can be put to db (escape quotes)
        self.log_msg = self.format(record)
        db_record = {
            "timestamp": int(time.time() * 1000),
            "level": record.levelname,
            "module": record.module,
            "line": record.lineno,
            "asctime": record.asctime,
            "msg": self.log_msg
        }

        try:
            if self.collection and self.dblog_name:
                # self.collection.insert(db_record, check_keys=False)
                self.collection.update({'name': self.dblog_name}, {'$push': {'logs': db_record}})
        except Exception as e:
            print('CRITICAL Logger DB ERROR: Logging to database not possible!')


def get_logdir(fw_cfg, baselogdir):
    """ Given ini logging config and base framework dir, checks if the log folder is writeable."""
    if not fw_cfg:
        return False, None
    log_writeable = True
    if fw_cfg and 'LOGGING' in fw_cfg:
        fwconf = fw_cfg['LOGGING']
        if 'logFolder' in fwconf and fwconf['logFolder'] and os.path.isdir(baselogdir):
            logdir = '%s/%s' % (baselogdir, fwconf['logFolder'])
    try:
        if not os.path.exists(logdir):
            os.makedirs(logdir)
    except:
        log_writeable = False
    try:
        if log_writeable:
            from pathlib import Path
            testfile = '%s/%d' % (logdir, int(time.time()))
            Path(testfile).touch()
            if os.path.exists(testfile):
                os.remove(testfile)
            else:
                log_writeable = False
    except:
        log_writeable = False
    return log_writeable, logdir



def ini_logging_config(fwconfigfile):
    """logging config"""
    from processor.helper.config.config_utils import framework_config, get_config_data, framework_dir, get_base_log_dir
    if not fwconfigfile:
        fwconfigfile = framework_config()
    fw_cfg = get_config_data(fwconfigfile)
    log_config = {
        "level": logging.INFO,
        "propagate": True,
        "size": 10,
        "backups": 10,
        "db": None,
        'logpath': None
    }
    if fw_cfg and 'LOGGING' in fw_cfg:
        base_log_dir = get_base_log_dir()
        if base_log_dir is None:
            base_log_dir = framework_dir()
        logwriteable, logpath = get_logdir(fw_cfg, base_log_dir)
        if logwriteable and logpath:
            log_config['logpath'] = logpath
        fwconf = fw_cfg['LOGGING']
        log_config['level'] = get_loglevel(fwconf)
        log_config['size'] = fwconf.getint('size') if 'size' in fwconf else 10
        log_config['backups'] = fwconf.getint('backups') if 'backups' in fwconf else 10
        log_config['propagate'] = fwconf.getboolean('propagate') if 'propagate' in fwconf else True
        log_config['db'] = fwconf['dbname'] if 'dbname' in fwconf else None
    return log_config


def default_logging(fwconfigfile=None):
    """Framework default logging to console"""
    log_config = None
    if fwconfigfile:
        log_config = ini_logging_config(fwconfigfile)

    logging.basicConfig(format=LOGFORMAT)
    logger = logging.getLogger(__name__)
    logger.propagate = log_config['propagate'] if log_config and 'propagate' in log_config else True
    logger.setLevel(get_loglevel(log_config))
    return logger


def add_file_logging(fwconfigfile):
    """ Add file logging to the basic logging"""
    global FWLOGGER, FWLOGFILENAME
    log_config = ini_logging_config(fwconfigfile)
    if not log_config['logpath']:
        return
    dblogname = os.getenv('DBLOG_NAME', None)
    logname  = dblogname if dblogname else datetime.datetime.today().strftime('%Y%m%d-%H%M%S')
    FWLOGFILENAME = '%s/%s.log' % (log_config['logpath'], logname)
    if not FWLOGGER:
        FWLOGGER = default_logging()
    handler = RotatingFileHandler(
        FWLOGFILENAME,
        maxBytes=1024 * 1024 * log_config['size'],
        backupCount=log_config['backups']
    )
    handler.setFormatter(logging.Formatter(LOGFORMAT))
    handler.setLevel(log_config['level'])
    FWLOGGER.addHandler(handler)


def add_db_logging(fwconfigfile, dburl, dbargs):
    """ Add database logging to the basic logging"""
    global FWLOGGER, dbhandler
    log_config = ini_logging_config(fwconfigfile)
    unittest = os.getenv('UNITTEST', "false")
    if log_config['db'] and unittest != "true" and dbargs and dburl:
        if not FWLOGGER:
            FWLOGGER = default_logging()
        dblogformat = '%(asctime)s-%(message)s'
        dbhandler = MongoDBHandler(dburl, log_config['db'])
        dbhandler.setFormatter(logging.Formatter(dblogformat))
        dbhandler.setLevel(log_config['level'])
        FWLOGGER.addHandler(dbhandler)


def getlogger(fw_cfg=None):
    """Get the logger for the framework."""
    global FWLOGGER
    if FWLOGGER:
        return FWLOGGER
    FWLOGGER = default_logging()
    return FWLOGGER

def logging_fw(fwconfigfile, dbargs, refresh_logger=False):
    """Framework file logging"""
    global FWLOGGER
    if FWLOGGER and (dbhandler and dbargs == 'FULL') and not refresh_logger:
        return FWLOGGER
    FWLOGGER = default_logging(fwconfigfile)
    add_file_logging(fwconfigfile)
    unittest = os.getenv('UNITTEST', "false")
    if unittest != "true":
        from processor.logging.dburl_kv import get_dburl
        dburl = get_dburl()
        add_db_logging(fwconfigfile, dburl, dbargs)
    return FWLOGGER


def init_logger(dbargs, fw_cfg=None, refresh_logger=False):
    """Get the logger for the framework."""
    return logging_fw(fw_cfg, dbargs, refresh_logger)


def init_logger_old(dbargs, fw_cfg=None, refresh_logger=False):
    """Get the logger for the framework."""
    global FWLOGGER
    if FWLOGGER and (dbhandler and dbargs == 'FULL') and not refresh_logger:
        return FWLOGGER
    FWLOGGER = logging_fw(fw_cfg, dbargs)
    return FWLOGGER


def get_dblogger():
    return DBLOGGER


def get_dblog_handler():
    return dbhandler

