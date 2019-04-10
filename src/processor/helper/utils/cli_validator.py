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
        LOGLEVEL=INFO python utilities/validator.py   -- Set to ERROR for this run.

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

   FRAMEWORKDIR is required to know config.ini locatin, if not set will consider the current directory
   as the FRAMEWORKDIR and $FRAMEWORKDIR/realm/config.ini

"""
import argparse
import sys
import atexit
import json
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import init_currentdata,\
    delete_currentdata, put_in_currentdata
from processor.helper.config.config_utils import framework_dir
from processor.database.database import init_db, TIMEOUT
from processor.connector.snapshot import populate_container_snapshots
from processor.connector.validation import run_container_validation_tests
try:
    from processor_enterprise.notifications.notification import check_send_notification
except:
    check_send_notification = lambda container, db: None


def validator_main(arg_vals=None):
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
       2 - Exception, Mongo connection failure or http connection exception, the tests execution
            could not
    """
    logger = getlogger()
    logger.critical("START: Argument parsing and Run Initialization.")
    logger.info("Comand: '%s %s'", sys.executable.rsplit('/', 1)[-1], ' '.join(sys.argv))
    cmd_parser = argparse.ArgumentParser("Validator functional tests")
    cmd_parser.add_argument('container', action='store', help='Container tests directory.')
    cmd_parser.add_argument('--db', action='store_true', default=False,
                            help='Mongo to be used for input and output data.')
    args = cmd_parser.parse_args(arg_vals)
    logger.debug("Args: %s", args)
    # Delete the rundata at the end of the script.
    # TODO This can be conditional, only if required by the caller.
    atexit.register(delete_currentdata)
    init_currentdata()
    retval = 0
    # returns the db connection handle and status, handle is ignored.
    _, db_init_res = init_db()
    if db_init_res:
        try:
            logger.debug("Running tests from %s", "the database." if args.db  else "file system.")
            put_in_currentdata('jsonsource', args.db)
            logger.info("Framework dir: %s", framework_dir())
            snapshot_status = populate_container_snapshots(args.container, args.db)
            print(json.dumps(snapshot_status, indent=2))
            if snapshot_status:
                status = run_container_validation_tests(args.container, args.db)
            retval = 0 if snapshot_status else 1
            # check_send_notification(args.container, args.db)
        except (Exception, KeyboardInterrupt) as ex:
            logger.error("Execution exception: %s", ex)
            retval = 2
    else:
        msg = "Mongo DB connection timed out after %d ms, check the mongo server, exiting!....."
        logger.error(msg, TIMEOUT)
        retval = 2
    return retval

