"""
   Common file for running validator functions.
"""
import argparse
import sys
import atexit
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import init_currentdata, delete_currentdata
from processor.database.database import init_db
from processor.connector.snapshot import populate_container_snapshots
from processor.connector.validation import run_container_validation_tests


logger = getlogger()


def main(arg_vals=None):
    """Main driver utility for running validator tests."""
    logger.info("Comand: '%s %s'", sys.executable.rsplit('/', 1)[-1], ' '.join(sys.argv))
    cmd_parser = argparse.ArgumentParser("Validator functional tests.")
    cmd_parser.add_argument('container', action='store', help='Container tests directory.')
    args = cmd_parser.parse_args(arg_vals)
    # Delete the rundata at the end of the script.
    atexit.register(delete_currentdata)
    logger.info(args)
    init_currentdata()
    init_db()
    status = populate_container_snapshots(args.container)
    if status:
        run_container_validation_tests(args.container)


if __name__ == "__main__":
    main()
