"""
   This is driver function to initiate the cloud validation framework for command line.
   The following are the steps to invoke the validator_main() function:
   1) Clone the repository
        git clone https://github.com/prancer-io/cloud-validation-framework.git <cloned-directory>
        cd <cloned-directory>
        export BASEDIR=`pwd`
   2) Install virtualenv(if not present) and create a virtualenv
        virtualenv --python=python3 cloudenv
        source cloudenv/bin/activate
   3) Install mongo server and start the mongo database services. All the data fetched from the
      different clouds is stored in different/same collections as configured in config.ini
   4) Set environment variables
        export PYTHONPATH=$BASEDIR/src
        export FRAMEWORKDIR=$BASEDIR
   5) Edit $BASEDIR/realm/config.ini for detailed logging to be info
        level = INFO
   6) Run the cloud validation tests for different containers (default LOGLEVEL=ERROR)
        python utilities/validator.py container1
        LOGLEVEL=DEBUG python utilities/validator.py   -- Set LOGLEVEL for this run
        LOGLEVEL=INFO python utilities/validator.py   -- Set to INFO for this run.

   The following steps when the prancer-basic is installed, instead of cloning the repository.
   1) Install virtualenv(if not present) and create a virtualenv
        export BASEDIR=`pwd`
        virtualenv --python=python3 cloudenv
        source cloudenv/bin/activate
   2) Install mongo server and start the mongo database services. All the data fetched from the
      different clouds is stored in different/same collections as configured in config.ini
   3) Install prancer-basic using pip
         pip install prancer-basic
   4) Download the realm folder from the https://github.com/prancer-io/cloud-validation-framework/tree/master/realm
      and edit the files to populate the tests and structure files.
   5) Set environment variables
        export PYTHONPATH=$BASEDIR/src
        export FRAMEWORKDIR=$BASEDIR
   6) Edit $BASEDIR/realm/config.ini for detailed logging to be info
        level = INFO
   7) Run the cloud validation tests for different containers(default LOGLEVEL=ERROR)
        LOGLEVEL=DEBUG validator container1
        LOGLEVEL=INFO validator container1

   The command line logs in the file under $FRAMEWORKDIR/log/<logfile>.log, only the steps which are
   marked critical are logged. All error conditions are also logged. Some of the error conditions logged:
      1) Unable to initiate mongo connection, log error and exit
      2) Unable to find tests, snapshots or structure data in database or in filesystem  and continue
      3) Unable to connect using connector for the snapshot and continue.
   For more logging level=INFO or level=DEBUG in the config.ini gives broader logging details of the process.

   FRAMEWORKDIR is required to know config.ini location, if not set will consider the current directory
   as the FRAMEWORKDIR and $FRAMEWORKDIR/realm/config.ini

"""

import argparse
import threading
import sys
import datetime
import atexit
import json
import os
from inspect import currentframe, getframeinfo
from processor.helper.config.config_utils import framework_dir, config_value, framework_config, \
    CFGFILE, get_config_data, FULL, SNAPSHOT, DBVALUES, TESTS, DBTESTS, NONE, CUSTOMER, SINGLETEST, container_exists
from processor.helper.file.file_utils import exists_file, exists_dir
from processor import __version__



def set_customer(cust=None):
    wkEnv = os.getenv('PRANCER_WK_ENV', None)
    customer = cust if cust else os.getenv('CUSTOMER', None)
    if wkEnv and wkEnv.upper() in ['STAGING', 'PRODUCTION']:
        config_path = 'prod' if wkEnv.upper() == 'PRODUCTION' else 'staging'
        if customer:
            os.environ[str(threading.currentThread().ident) + "_SPACE_ID"] = config_path + "/" + customer
        else:
            os.environ[str(threading.currentThread().ident) + "_SPACE_ID"] = "staging/default"
        return True
    elif customer:
        os.environ[str(threading.currentThread().ident) + "_SPACE_ID"] = "staging/" + customer
        return True
    return  False



def console_log(message, cf):
    """Logger like statements only used till logger configuration is read and initialized."""
    filename = getframeinfo(cf).filename
    line = cf.f_lineno
    now = datetime.datetime.now()
    fmtstr = '%s,%s(%s: %3d) %s' % (now.strftime('%Y-%m-%d %H:%M:%S'), str(now.microsecond)[:3],
                                    os.path.basename(filename).replace('.py', ''), line, message)
    print(fmtstr)


def valid_config_ini(config_ini):
    """ Valid config ini path and load the file and check """
    error = None
    if exists_file(config_ini):
        config_data = get_config_data(config_ini)
        if config_data:
            # TODO: can also check for necessary sections and fields.
            pass
        else:
            error = "Configuration(%s) INI file is invalid, correct it and try again!" % config_ini
    else:
        error = "Configuration(%s) INI file does not exist!" % config_ini
    return error


def search_config_ini():
    """Need the config.ini file to read initial configuration data"""
    error = False
    config_ini = None
    fwdir = os.getenv('FRAMEWORKDIR', None)
    if fwdir:
        if exists_dir(fwdir):
            config_ini = '%s/%s' % (fwdir, CFGFILE)
            error_msg = valid_config_ini(config_ini)
            if error_msg:
                console_log("FRAMEWORKDIR: %s, env variable directory exists, checking...." % fwdir, currentframe())
                console_log(error_msg, currentframe())
                error = True
        else:
            console_log("FRAMEWORKDIR: %s, env variable set to non-existent directory, exiting....." % fwdir, currentframe())
            error = True
    else:
        config_ini = '%s/%s' % (os.getcwd(), CFGFILE)
        error_msg = valid_config_ini(config_ini)
        if error_msg:
            console_log("FRAMEWORDIR environment variable NOT SET, searching in current directory.", currentframe())
            console_log(error_msg, currentframe())
            error = True
    return error, config_ini


def validator_main(arg_vals=None, delete_rundata=True):
    """
    Main driver utility for running validator tests
    The arg_vals, if passed should be array of string. A set of examples are:
      1) arg_vals = ['container1'] - Use container1 to process test files from filesystem
      2) args_vals = ['container1', '--db'] - Use container1 to process test documents from database.
    When arg_vals is None, the argparse library parses from sys.argv array list.
    The successful argument parsing initializes the system for the run.
    On exit will run cleanup. The return values of this main entry function are as:
       0 - Success, tests executed.
       1 - Failure, Tests execution error.
       2 - Exception, missing config.ini, Mongo connection failure or http connection exception,
           the tests execution could not be started or completed.
    """
    cmd_parser = argparse.ArgumentParser("Prancer Basic Functionality")
    cmd_parser.add_argument('-v','--version', action='version', version=("Prancer %s" % __version__) , help='Show prancer version')
    cmd_parser.add_argument('container', action='store', help='Container tests directory.')
    cmd_parser.add_argument('--db', action='store', default=None, choices=['NONE', 'SNAPSHOT', 'FULL'],
                            help='NONE - Mongo database not used, SNAPSHOT - for storing snapshots, FULL - Tests, configurations, outputs and snapshots in database')
    cmd_parser.add_argument('--crawler', action='store_true', default=False,
                            help='Crawl and generate snapshot files only')
    cmd_parser.add_argument('--test', action='store', default=None, help='Run a single test in NODB mode')
    cmd_parser.add_argument('--customer', action='store', default=None, help='customer name for config')
    args = cmd_parser.parse_args(arg_vals)

    retval = 2
    set_customer()
    cfg_error, config_ini = search_config_ini()
    if cfg_error:
        return retval

    if args.customer:
        set_customer(args.customer)
    if args.db:
        if args.db.upper() in DBVALUES:
            args.db = DBVALUES.index(args.db.upper())
        else:
            args.db = DBVALUES.index(SNAPSHOT)
    else:
        nodb = config_value(TESTS, DBTESTS)
        if nodb and nodb.upper() in DBVALUES:
            args.db = DBVALUES.index(nodb.upper())
        else:
            args.db = DBVALUES.index(SNAPSHOT)

    if args.test:
        args.db = DBVALUES.index(NONE)

    # Check if we want to run in NO DATABASE MODE
    if args.db:
        # returns the db connection handle and status, handle is ignored.
        from processor.database.database import init_db, TIMEOUT
        _, db_init_res = init_db()
        if not db_init_res:
            msg = "Mongo DB connection timed out after %d ms, check the mongo server, exiting!....." % TIMEOUT
            console_log(msg, currentframe())
            return retval

    # Check the log directory and also check if it is writeable.
    from processor.logging.log_handler import init_logger, get_logdir, default_logging, add_file_logging
    fw_cfg = get_config_data(framework_config())
    log_writeable, logdir = get_logdir(fw_cfg, framework_dir())
    if not log_writeable:
        console_log('Logging directory(%s) is not writeable, exiting....' % logdir)
        return retval

    # Alls well from this point, check container exists in the directory configured
    retval = 0
    logger = init_logger(args.db, framework_config())
    # logger = add_file_logging(config_ini)
    logger.critical("START: Argument parsing and Run Initialization. Version %s", __version__)


    from processor.connector.snapshot import populate_container_snapshots
    from processor.connector.validation import run_container_validation_tests
    try:
        from processor_enterprise.notifications.notification import check_send_notification
    except:
        check_send_notification = lambda container, db: None

    try:
        from processor_enterprise.crawler.master_snapshot import generate_container_mastersnapshots
    except:
        generate_container_snapshots = lambda container, db: None

    logger.info("Command: '%s %s'", sys.executable.rsplit('/', 1)[-1], ' '.join(sys.argv))
    try:
        from processor.helper.config.rundata_utils import init_currentdata, \
            delete_currentdata, put_in_currentdata
        # Delete the rundata at the end of the script as per caller, default is True.
        if delete_rundata:
            atexit.register(delete_currentdata)
        init_currentdata()

        logger.critical("Using Framework dir: %s", framework_dir())
        logger.info("Args: %s", args)
        logger.debug("Running tests from %s.", DBVALUES[args.db])
        fs = True if args.db > DBVALUES.index(SNAPSHOT) else False
        put_in_currentdata('jsonsource', fs)
        put_in_currentdata(DBTESTS, args.db)
        # if args.db == DBVALUES.index(FULL):
        #     from processor.logging.log_handler import get_dblogger
        #     log_name = get_dblogger()
        #     if log_name:
        #         pid = open('/tmp/pid_%s' % os.getpid(), 'w')
        #         pid.write(log_name)
        #         pid.close()
        if args.customer:
            put_in_currentdata(CUSTOMER, args.customer)
        if args.test:
            put_in_currentdata(SINGLETEST, args.test)
            put_in_currentdata('container', args.container)
        else:
            put_in_currentdata(SINGLETEST, False)
        if not args.db:
            retval = 0 if container_exists(args.container) else 2
            if retval:
                logger.critical("Container(%s) is not present in Framework dir: %s",
                                args.container, framework_dir())
                # TODO: Log the path the framework looked for.
                return retval
        if args.crawler:
            # Generate snapshot files from here.
            generate_container_mastersnapshots(args.container, fs)
        else:
            # Normal flow
            snapshot_status = populate_container_snapshots(args.container, fs)
            logger.debug(json.dumps(snapshot_status, indent=2))
            if snapshot_status:
                status = run_container_validation_tests(args.container, fs, snapshot_status)
                retval = 0 if status else 1
            else:
                retval = 1
            check_send_notification(args.container, args.db)
    except (Exception, KeyboardInterrupt) as ex:
        logger.error("Execution exception: %s", ex)
        retval = 2
    return retval

