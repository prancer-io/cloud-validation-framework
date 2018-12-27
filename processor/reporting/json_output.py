"""Reporting related utility functions."""
from collections import OrderedDict
from processor.helper.json.json_utils import save_json_to_file


def dump_output_results(results, test_file, container):
    """ Dump the report in the json format for test execution results."""
    test_file_parts = test_file.rsplit('/', 1)
    output_file = '%s/output-%s' % (test_file_parts[0], test_file_parts[-1])
    od = OrderedDict()
    od["$schema"] = ""
    od["contentVersion"] = "1.0.0.0"
    od["fileType"] = "output"
    od["timestamp"] = ""
    od["snapshot"] = "snapshot.json"
    od["test"] = test_file_parts[-1]
    od["container"] = container
    od["results"] = results
    save_json_to_file(od, output_file)
