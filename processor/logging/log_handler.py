"""
   Logging related functionality in this module.
"""

import logging
import datetime
import os
from processor.helper.config.config_utils import (get_solution_dir,
                                                  load_config,
                                                  get_config_ini)

LOGGER = None
LOGFILE = '%Y%m%d-%H%M%S'
LOGFILENAME = None


def get_logger_config(config):
    """Return the logging config"""
    logconfig = {
        "level": logging.INFO,
        "maxbytes": 10,
        "backupcount": 10,
        "propagate": True
    }
    if config and 'LOGGING' in config:
        conf = config['LOGGING']
        logconfig['level'] = logging.getLevelName(conf['level']) \
            if 'level' in conf and conf['level'] else logging.INFO
        logconfig['maxbytes'] = conf.getint('maxbytes') if 'maxbytes' in conf else 10
        logconfig['backupcount'] = conf.getint('backupcount') if 'backupcount' in conf else 10
        logconfig['propagate'] = conf.getboolean('propagate') if 'propagate' in conf else True
    return logconfig


def setup_logging(configfile, ):
    """Setup the logging for the utility"""
    global LOGFILENAME
    config = load_config(configfile)
    logconfig = get_logger_config(config)
    level = os.getenv('LOGLEVEL', None)
    loglevel = level if level and level in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'] \
        else logconfig['level']
    logformat = '%(asctime)s(%(module)s:%(lineno)4d) - %(message)s'
    logging.basicConfig(level=loglevel, format=logformat)
    logger = logging.getLogger(__name__)
    logger.propagate = logconfig['propagate']
    if True:
        from logging.handlers import RotatingFileHandler
        logpath = '%slog/' % get_solution_dir()
        # if not os.path.exists(logpath):
        #     os.mkdir(logpath)
        LOGFILENAME = '%s%s.log' % (logpath, datetime.datetime.today().strftime(LOGFILE))
        handler = RotatingFileHandler(
            LOGFILENAME,
            maxBytes=1024 * 1024 * logconfig['maxbytes'],
            backupCount=logconfig['backupcount']
        )
        handler.setFormatter(logging.Formatter(logformat))
        handler.setLevel(logconfig['level'])
        logger.addHandler(handler)
    return logger


def getlogger(configfile=None):
    """Get the common logger for the application."""
    global LOGGER
    if LOGGER:
        return LOGGER
    if not configfile:
        configfile = get_config_ini()
    LOGGER = setup_logging(configfile)
    return LOGGER

