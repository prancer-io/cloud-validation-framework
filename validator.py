"""
   Common file for running validator functions.
"""
import argparse
import sys
import atexit
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import init_currentdata,\
    delete_currentdata, put_in_currentdata
from processor.database.database import init_db, TIMEOUT
from processor.connector.snapshot import populate_container_snapshots
from processor.connector.validation import run_container_validation_tests
from processor.notifications.notification import check_send_notification


logger = getlogger()


def main(arg_vals=None):
    """Main driver utility for running validator tests."""
    logger.info("Comand: '%s %s'", sys.executable.rsplit('/', 1)[-1], ' '.join(sys.argv))
    cmd_parser = argparse.ArgumentParser("Validator functional tests.")
    cmd_parser.add_argument('container', action='store', help='Container tests directory.')
    cmd_parser.add_argument('--db', action='store_true', default=False,
                            help='Mongo to be used for input and output data.')

    args = cmd_parser.parse_args(arg_vals)
    # Delete the rundata at the end of the script.
    atexit.register(delete_currentdata)
    logger.info(args)
    init_currentdata()
    _, db_init_res = init_db()
    if db_init_res:
        if args.db:
            logger.info("Running tests from the database.")
        else:
            logger.info("Running tests from file system.")
        put_in_currentdata('jsonsource', args.db)
        status = populate_container_snapshots(args.container, args.db)
        if status:
            run_container_validation_tests(args.container, args.db)
        check_send_notification(args.container, args.db)
    else:
        msg = "Mongo DB connection timed out after %d ms, check the mongo server, exiting!....."
        logger.info(msg, TIMEOUT)



if __name__ == "__main__":
    main()
