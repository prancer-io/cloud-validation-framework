"""
   Common file for running validator functions.
"""
import argparse
import sys
import atexit
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
    """Main driver utility for running validator tests."""
    logger = getlogger()
    logger.info("Comand: '%s %s'", sys.executable.rsplit('/', 1)[-1], ' '.join(sys.argv))
    cmd_parser = argparse.ArgumentParser("Validator functional tests.")
    cmd_parser.add_argument('container', action='store', help='Container tests directory.')
    cmd_parser.add_argument('--db', action='store_true', default=False,
                            help='Mongo to be used for input and output data.')

    args = cmd_parser.parse_args(arg_vals)
    retval = 0
    # Delete the rundata at the end of the script.
    atexit.register(delete_currentdata)
    logger.info(args)
    init_currentdata()
    _, db_init_res = init_db()
    if db_init_res:
        try:
            if args.db:
                logger.info("Running tests from the database.")
            else:
                logger.info("Running tests from file system.")
            put_in_currentdata('jsonsource', args.db)
            logger.info("Framework dir: %s", framework_dir())
            status = populate_container_snapshots(args.container, args.db)
            if status:
                status = run_container_validation_tests(args.container, args.db)
            retval = 0 if status else 1
            check_send_notification(args.container, args.db)
        except (Exception, KeyboardInterrupt) as ex:
            logger.info("Execution exception: %s", ex)
            retval = 2
    else:
        msg = "Mongo DB connection timed out after %d ms, check the mongo server, exiting!....."
        logger.info(msg, TIMEOUT)
    return retval

