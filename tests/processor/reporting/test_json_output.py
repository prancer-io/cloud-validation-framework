import os
from processor.reporting.json_output import dump_output_results


def test_dump_output_results(create_temp_dir):
    newpath = create_temp_dir()
    fname = '%s/test1.json' % newpath
    new_fname = '%s/output-a1.json' % newpath
    dump_output_results([], fname, 'test1', 'snapshot')
    file_exists = os.path.exists(new_fname)
    assert False == file_exists
