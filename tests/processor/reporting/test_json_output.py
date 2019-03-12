import os
from processor.reporting.json_output import dump_output_results, json_record

def mock_config_value(key, default=None):
    return 'pytestdb'

def mock_insert_one_document(doc, collection, dbname):
    pass

def test_dump_output_results(monkeypatch, create_temp_dir):
    monkeypatch.setattr('processor.reporting.json_output.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.reporting.json_output.config_value', mock_config_value)
    newpath = create_temp_dir()
    fname = '%s/test1.json' % newpath
    new_fname = '%s/output-a1.json' % newpath
    dump_output_results([], fname, 'test1', 'snapshot')
    file_exists = os.path.exists(new_fname)
    assert False == file_exists
    val = dump_output_results([], fname, 'test1', 'snapshot', False)
    assert val is None


def test_json_record(monkeypatch):
    monkeypatch.setattr('processor.reporting.json_output.config_value', mock_config_value)
    val = json_record('abcd', 'test', 'a.json', json_data=None)
    assert val is not None
    val = json_record('abcd', 'test', 'a.json', json_data={'$schema': '1.9.0'})
    assert val is not None
    exists = '$schema' not in val['json']
    assert exists == True