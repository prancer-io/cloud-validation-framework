"""Helper functions to setup logging for the framework."""
import datetime
import logging
from logging.handlers import RotatingFileHandler
import datetime
import time
import os
from pymongo import MongoClient
from processor.helper.config.config_utils import framework_dir,\
    get_config_data, framework_config


FWLOGGER = None
FWLOGFILENAME = None
MONGOLOGGER = None



class MongoDBHandler(logging.Handler):
    """Customized logging handler that puts logs to the database, pymongo required
    """
    def __init__(self, dbname):
        logging.Handler.__init__(self)
        dbconnection = MongoClient(port=27017)
        if dbname:
            db = dbconnection[dbname]
        else:
            db = dbconnection['test']
        collection = 'logs_%s' % datetime.datetime.now().strftime('%Y%M%d%H%M%S')
        if db:
            coll = db[collection]
            self.collection = coll


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
            if self.collection:
                self.collection.insert(db_record, check_keys=False)
        except Exception as e:
            print('CRITICAL Logger DB ERROR: Logging to database not possible!')



def logging_fw(fwconfigfile):
    """Framework file logging"""
    global FWLOGFILENAME
    fwlogfile = '%Y%m%d-%H%M%S'
    if not fwconfigfile:
        fwconfigfile = framework_config()
    fw_cfg = get_config_data(fwconfigfile)
    log_config = {
        "level": logging.INFO,
        "propagate": True,
        "size": 10,
        "backups": 10,
        "db": None
    }
    if fw_cfg and 'LOGGING' in fw_cfg:
        fwconf = fw_cfg['LOGGING']
        log_config['level'] = logging.getLevelName(fwconf['level']) \
            if 'level' in fwconf and fwconf['level'] else logging.INFO
        log_config['size'] = fwconf.getint('size') if 'size' in fwconf else 10
        log_config['backups'] = fwconf.getint('backups') if 'backups' in fwconf else 10
        log_config['propagate'] = fwconf.getboolean('propagate') if 'propagate' in fwconf \
            else True
        log_config['db'] = fwconf['dbname'] if 'dbname' in fwconf else None
    level = os.getenv('LOGLEVEL', None)
    loglevel = level if level and level in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'] \
        else log_config['level']
    logformat = '%(asctime)s(%(module)s:%(lineno)4d) - %(message)s'
    logging.basicConfig(level=loglevel, format=logformat)
    logger = logging.getLogger(__name__)
    logger.propagate = log_config['propagate']
    logpath = '%s/log/' % framework_dir()
    FWLOGFILENAME = '%s%s.log' % (logpath, datetime.datetime.today().strftime(fwlogfile))
    handler = RotatingFileHandler(
        FWLOGFILENAME,
        maxBytes=1024 * 1024 * log_config['size'],
        backupCount=log_config['backups']
    )
    handler.setFormatter(logging.Formatter(logformat))
    handler.setLevel(log_config['level'])
    logger.addHandler(handler)
    unittest = os.getenv('UNITTEST', None)
    if log_config['db'] and not unittest:
        dblogformat = '%(message)s'
        dbhandler = MongoDBHandler(log_config['db'])
        dbhandler.setFormatter(logging.Formatter(dblogformat))
        dbhandler.setLevel(log_config['level'])
        logger.addHandler(dbhandler)
    return logger


def getlogger(fw_cfg=None):
    """Get the logger for the framework."""
    global FWLOGGER
    if FWLOGGER:
        return FWLOGGER
    FWLOGGER = logging_fw(fw_cfg)
    return FWLOGGER
