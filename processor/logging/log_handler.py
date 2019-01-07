"""Helper functions to setup logging for the framework."""
import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
from processor.helper.config.config_utils import framework_dir,\
    get_config_data, framework_config


FWLOGGER = None
FWLOGFILENAME = None


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
    }
    if fw_cfg and 'LOGGING' in fw_cfg:
        fwconf = fw_cfg['LOGGING']
        log_config['level'] = logging.getLevelName(fwconf['level']) \
            if 'level' in fwconf and fwconf['level'] else logging.INFO
        log_config['size'] = fwconf.getint('size') if 'size' in fwconf else 10
        log_config['backups'] = fwconf.getint('backups') if 'backups' in fwconf else 10
        log_config['propagate'] = fwconf.getboolean('propagate') if 'propagate' in fwconf \
            else True
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
    return logger


def getlogger(fw_cfg=None):
    """Get the logger for the framework."""
    global FWLOGGER
    if FWLOGGER:
        return FWLOGGER
    FWLOGGER = logging_fw(fw_cfg)
    return FWLOGGER
