"""
   Common file for running validator functions.
"""
import argparse
import sys
import atexit
import platform
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import init_currentdata,\
    delete_currentdata, put_in_currentdata
from processor.database.database import init_db
from processor.helper.config.config_utils import config_value
from processor.api.utils import parsebool

from processor.notifications.notification import send_notification
from processor.connector.snapshot import populate_container_snapshots
from processor.connector.validation import run_container_validation_tests


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
    init_db()
    if args.db:
        logger.info("Running tests from the database.")
    else:
        logger.info("Running tests from file system.")
    put_in_currentdata('jsonsource', args.db)
    # val = get_vault_data()
    # logger.info('Secret Value: %s', val)
    status = populate_container_snapshots(args.container, args.db)
    if status:
        run_container_validation_tests(args.container, args.db)
    notification_enabled = parsebool(config_value('NOTIFICATION', 'enabled'))
    logger.info('Notification: %s, %s', notification_enabled, type(notification_enabled))
    if notification_enabled:
        msg = 'Completed tests for container: %s using %s.' % \
              (args.container, 'database' if args.db else 'filesystem')
        uname = platform.node()
        system = platform.system()
        msg = '%s on %s/%s' % ( msg[:-1], uname, system)
        send_notification(msg)


if __name__ == "__main__":
    main()
