"""
   Common utility file to convert terraform to json files.
"""
import argparse
import sys
import atexit
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import init_currentdata, delete_currentdata
from processor.helper.file.file_utils import exists_file
from processor.helper.json.json_utils import save_json_to_file
from processor.connector.snapshot_custom import convert_to_json




def convert_terraform_to_json(terraform, output=None):
    if exists_file(terraform):
        if not output:
            parts = terraform.rsplit('.', -1)
            output = '%s.json' % parts[0]
        json_data = convert_to_json(terraform, 'terraform')
        if json_data:
            save_json_to_file(json_data, output)


def terraform_to_json_main(arg_vals=None):
    """Main driver utility for converting terraform to json files."""
    logger = getlogger()
    logger.info("Comand: '%s %s'", sys.executable.rsplit('/', 1)[-1], ' '.join(sys.argv))
    cmd_parser = argparse.ArgumentParser("Convert terraform to json files")
    cmd_parser.add_argument('terraform', action='store',
                            help='Full path of the terraform file.')
    cmd_parser.add_argument('--output', action='store', default=None,
                            help='Path to store the file.')
    args = cmd_parser.parse_args(arg_vals)
    # Delete the rundata at the end of the script.
    atexit.register(delete_currentdata)
    logger.info(args)
    init_currentdata()
    convert_terraform_to_json(args.terraform, args.output)
    return 0
