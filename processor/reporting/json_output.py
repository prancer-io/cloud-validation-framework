"""
   Reporting related utility functions.
"""

from collections import OrderedDict
from processor.helper.config.config_utils import get_test_json_dir
from processor.helper.json.json_utils import dump_json


def dump_output_results(results, test_file, container):
    test_file_parts = test_file.rsplit('/', 1)
    output_file = '%s/%s/output-%s' % (get_test_json_dir(), container, test_file_parts[-1])
    od = OrderedDict()
    od["$schema"] =  ""
    od["contentVersion"]  = "1.0.0.0"
    od["fileType"] = "output"
    od["timestamp"] = ""
    od["snapshot"] = "snapshot.json"
    od["test"] = test_file_parts[-1]
    od["container"] = container
    od["results"] = results
    dump_json(od, output_file)





