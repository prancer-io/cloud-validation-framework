"""Helper functions to setup logging for framework."""
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
    FWLOGFILE = '%Y%m%d-%H%M%S'
    if not fwconfigfile:
        fwconfigfile = framework_config()
    fw_cfg = get_config_data(fwconfigfile)
    logconfig = {
        "level": logging.INFO,
        "propagate": True,
        "size": 10,
        "backups": 10,
    }
    if fw_cfg and 'LOGGING' in fw_cfg:
        fwconf = fw_cfg['LOGGING']
        logconfig['level'] = logging.getLevelName(fwconf['level']) \
            if 'level' in fwconf and fwconf['level'] else logging.INFO
        logconfig['size'] = fwconf.getint('size') if 'size' in fwconf else 10
        logconfig['backups'] = fwconf.getint('backups') if 'backups' in fwconf else 10
        logconfig['propagate'] = fwconf.getboolean('propagate') if 'propagate' in fwconf \
            else True
    level = os.getenv('LOGLEVEL', None)
    loglevel = level if level and level in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'] \
        else logconfig['level']
    logformat = '%(asctime)s(%(module)s:%(lineno)4d) - %(message)s'
    logging.basicConfig(level=loglevel, format=logformat)
    logger = logging.getLogger(__name__)
    logger.propagate = logconfig['propagate']
    logpath = '%s/log/' % framework_dir()
    FWLOGFILENAME = '%s%s.log' % (logpath, datetime.datetime.today().strftime(FWLOGFILE))
    handler = RotatingFileHandler(
        FWLOGFILENAME,
        maxBytes=1024 * 1024 * logconfig['size'],
        backupCount=logconfig['backups']
    )
    handler.setFormatter(logging.Formatter(logformat))
    handler.setLevel(logconfig['level'])
    logger.addHandler(handler)
    return logger


def getlogger(fw_cfg=None):
    """Get the logger for the framework."""
    global FWLOGGER
    if FWLOGGER:
        return FWLOGGER
    FWLOGGER = logging_fw(fw_cfg)
    return FWLOGGER

