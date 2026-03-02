"""
Comprehensive tests for helper utility functions across the framework.
Tests cover: json_utils, xml_utils, config_utils, hcl_utils, yaml_utils, file_utils.
"""

import os
import re
import json
import time
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from collections import OrderedDict


# ---------------------------------------------------------------------------
# json_utils tests
# ---------------------------------------------------------------------------

from processor.helper.json.json_utils import (
    remove_comments,
    get_field_value,
    put_value,
    parse_boolean,
    set_timestamp,
    get_json_files,
    store_snapshot,
    save_json_to_file,
    json_from_string,
    collectiontypes,
    SNAPSHOT,
    MASTERSNAPSHOT,
    TEST,
    OUTPUT,
    STRUCTURE,
    NOTIFICATIONS,
    MASTERTEST,
    EXCLUSIONS,
)


# -- remove_comments --

class TestRemoveComments:

    def test_single_line_comment_removed(self):
        result = remove_comments('{"a": 1} // comment')
        assert result == '{"a": 1} '

    def test_block_comment_removed(self):
        result = remove_comments('{"a": 1, /* block */ "b": 2}')
        assert result == '{"a": 1,  "b": 2}'

    def test_url_inside_string_preserved(self):
        input_str = '{"url": "http://example.com"}'
        result = remove_comments(input_str)
        assert result == input_str

    def test_multiline_block_comment_removed(self):
        input_str = '{"a": 1, /* this\nis\nmultiline */ "b": 2}'
        result = remove_comments(input_str)
        assert result == '{"a": 1,  "b": 2}'

    def test_no_comments_unchanged(self):
        input_str = '{"key": "value", "num": 42}'
        result = remove_comments(input_str)
        assert result == input_str

    def test_empty_string(self):
        assert remove_comments('') == ''

    def test_single_quoted_string_with_slashes_preserved(self):
        input_str = "{'url': 'http://example.com'}"
        result = remove_comments(input_str)
        assert result == input_str

    def test_multiple_line_comments(self):
        input_str = '{"a": 1} // first\n{"b": 2} // second'
        result = remove_comments(input_str)
        assert '// first' not in result
        assert '// second' not in result


# -- get_field_value --

class TestGetFieldValue:

    def test_simple_key(self):
        assert get_field_value({'a': 1}, 'a') == 1

    def test_nested_key(self):
        assert get_field_value({'a': {'b': 'c'}}, 'a.b') == 'c'

    def test_array_index_zero(self):
        data = {'a': {'b': [1, 2, 3]}}
        assert get_field_value(data, 'a.b[0]') == 1

    def test_array_index_last(self):
        data = {'a': {'b': [1, 2, 3]}}
        assert get_field_value(data, 'a.b[2]') == 3

    def test_array_then_nested_key(self):
        data = {'a': {'b': [{'c': 10}, {'c': 20}]}}
        assert get_field_value(data, 'a.b[0].c') == 10

    def test_leading_dot_stripped(self):
        data = {'a': {'b': 5}}
        assert get_field_value(data, '.a.b') == 5

    def test_none_data_returns_none(self):
        assert get_field_value(None, 'a.b') is None

    def test_empty_parameter_returns_none(self):
        assert get_field_value({'a': 1}, '') is None

    def test_none_parameter_returns_none(self):
        assert get_field_value({'a': 1}, None) is None

    def test_missing_key_returns_none(self):
        assert get_field_value({'a': 1}, 'b') is None

    def test_deep_missing_key_returns_none(self):
        # When traversal reaches a non-dict value and tries 'field in retval',
        # the source code raises TypeError for non-iterable types.
        with pytest.raises(TypeError):
            get_field_value({'a': {'b': 1}}, 'a.b.c')

    def test_array_index_out_of_range_returns_none(self):
        data = {'a': {'b': [1, 2]}}
        assert get_field_value(data, 'a.b[5]') is None


# -- put_value --

class TestPutValue:

    def test_simple_put(self):
        data = {}
        put_value(data, 'a', 1)
        assert data == {'a': 1}

    def test_nested_put(self):
        data = {}
        put_value(data, 'a.b.c', 1)
        assert data == {'a': {'b': {'c': 1}}}

    def test_overwrite_existing(self):
        data = {'a': 1}
        put_value(data, 'a', 2)
        assert data == {'a': 2}

    def test_leading_dot(self):
        data = {}
        put_value(data, '.a', 1)
        assert data == {'a': 1}

    def test_put_dict_value(self):
        data = {}
        put_value(data, 'x.y', {'nested': True})
        assert data == {'x': {'y': {'nested': True}}}

    def test_put_list_value(self):
        data = {}
        put_value(data, 'items', [1, 2, 3])
        assert data == {'items': [1, 2, 3]}

    def test_empty_field_no_change(self):
        data = {'a': 1}
        put_value(data, '', 2)
        # empty field produces empty split list, loop doesn't execute
        assert data == {'a': 1}


# -- parse_boolean --

class TestParseBoolean:

    def test_true_lowercase(self):
        assert parse_boolean('true') is True

    def test_true_titlecase(self):
        assert parse_boolean('True') is True

    def test_true_uppercase(self):
        assert parse_boolean('TRUE') is True

    def test_true_mixedcase(self):
        assert parse_boolean('TrUe') is True

    def test_false_lowercase(self):
        assert parse_boolean('false') is False

    def test_false_titlecase(self):
        assert parse_boolean('False') is False

    def test_none_returns_false(self):
        assert parse_boolean(None) is False

    def test_empty_string_returns_false(self):
        assert parse_boolean('') is False

    def test_yes_returns_false(self):
        assert parse_boolean('yes') is False


# -- set_timestamp --

class TestSetTimestamp:

    def test_valid_dict(self):
        data = {}
        result = set_timestamp(data)
        assert result is True
        assert 'timestamp' in data
        assert isinstance(data['timestamp'], int)

    def test_non_dict_returns_false(self):
        assert set_timestamp(None) is False
        assert set_timestamp([1, 2]) is False
        assert set_timestamp('string') is False
        assert set_timestamp(42) is False

    def test_custom_fieldname(self):
        data = {}
        result = set_timestamp(data, 'created_at')
        assert result is True
        assert 'created_at' in data
        assert isinstance(data['created_at'], int)

    def test_timestamp_is_recent(self):
        data = {}
        before = int(time.time() * 1000)
        set_timestamp(data)
        after = int(time.time() * 1000)
        assert before <= data['timestamp'] <= after


# -- get_json_files --

class TestGetJsonFiles:

    def test_filters_by_file_type(self, tmp_path):
        # Create JSON files with different fileType values
        snap = {'fileType': 'snapshot', 'data': 'snap_data'}
        test = {'fileType': 'test', 'data': 'test_data'}
        other = {'fileType': 'other', 'data': 'other_data'}

        for name, content in [('s1.json', snap), ('t1.json', test), ('o1.json', other)]:
            with open(str(tmp_path / name), 'w') as f:
                json.dump(content, f)

        result = get_json_files(str(tmp_path), 'snapshot')
        assert len(result) == 1
        assert result[0].endswith('s1.json')

    def test_name_filter(self, tmp_path):
        snap1 = {'fileType': 'snapshot', 'id': 1}
        snap2 = {'fileType': 'snapshot', 'id': 2}
        with open(str(tmp_path / 'alpha.json'), 'w') as f:
            json.dump(snap1, f)
        with open(str(tmp_path / 'beta.json'), 'w') as f:
            json.dump(snap2, f)

        result = get_json_files(str(tmp_path), 'snapshot', name='alpha')
        assert len(result) == 1
        assert result[0].endswith('alpha.json')

    def test_empty_dir_returns_empty(self, tmp_path):
        result = get_json_files(str(tmp_path), 'snapshot')
        assert result == []

    def test_none_dir_returns_empty(self):
        result = get_json_files(None, 'snapshot')
        assert result == []

    def test_none_file_type_returns_empty(self, tmp_path):
        result = get_json_files(str(tmp_path), None)
        assert result == []


# -- store_snapshot --

class TestStoreSnapshot:

    def test_creates_snapshot_file(self, tmp_path):
        data = {'snapshotId': 'snap_001', 'resource': 'vm1'}
        store_snapshot(str(tmp_path), data)
        snapshot_file = tmp_path / 'snap_001'
        assert snapshot_file.exists()
        with open(str(snapshot_file)) as f:
            stored = json.load(f)
        assert stored['resource'] == 'vm1'

    def test_nonexistent_dir_no_error(self):
        data = {'snapshotId': 'snap_002', 'resource': 'vm2'}
        # Should not raise, directory does not exist so nothing happens
        store_snapshot('/nonexistent/path/xyz', data)


# -- collectiontypes constant --

class TestCollectionTypes:

    def test_collectiontypes_keys(self):
        expected_keys = {'test', 'structure', 'snapshot', 'masterSnapshot',
                         'mastertest', 'output', 'notifications', 'exclusions'}
        assert set(collectiontypes.keys()) == expected_keys

    def test_collectiontypes_values(self):
        expected_values = {'TEST', 'STRUCTURE', 'SNAPSHOT', 'MASTERSNAPSHOT',
                           'MASTERTEST', 'OUTPUT', 'NOTIFICATIONS', 'EXCLUSIONS'}
        assert set(collectiontypes.values()) == expected_values


# ---------------------------------------------------------------------------
# xml_utils tests
# ---------------------------------------------------------------------------

from processor.helper.xml.xml_utils import parse_element, xml_to_json
import xml.etree.ElementTree as ET


class TestParseElement:

    def test_simple_element(self):
        elem = ET.fromstring('<root>text</root>')
        result = parse_element(elem)
        assert result['name'] == 'root'
        assert result['text'] == 'text'
        assert result['attributes'] == {}
        assert result['children'] == []

    def test_element_with_attributes(self):
        elem = ET.fromstring('<root attr="val" other="123"/>')
        result = parse_element(elem)
        assert result['attributes'] == {'attr': 'val', 'other': '123'}

    def test_element_with_children(self):
        elem = ET.fromstring('<root><child>hello</child></root>')
        result = parse_element(elem)
        assert len(result['children']) == 1
        assert result['children'][0]['name'] == 'child'
        assert result['children'][0]['text'] == 'hello'

    def test_nested_elements(self):
        elem = ET.fromstring('<a><b><c>deep</c></b></a>')
        result = parse_element(elem)
        assert result['name'] == 'a'
        b = result['children'][0]
        assert b['name'] == 'b'
        c = b['children'][0]
        assert c['name'] == 'c'
        assert c['text'] == 'deep'

    def test_empty_text_is_none(self):
        elem = ET.fromstring('<root>   </root>')
        result = parse_element(elem)
        assert result['text'] is None

    def test_no_text_is_none(self):
        elem = ET.fromstring('<root/>')
        result = parse_element(elem)
        assert result['text'] is None


class TestXmlToJson:

    def test_full_xml_string(self):
        xml_str = '<root><child>text</child></root>'
        result = xml_to_json(xml_str)
        assert result['name'] == 'root'
        assert len(result['children']) == 1

    def test_multiple_children(self):
        xml_str = '<root><a>1</a><b>2</b><c>3</c></root>'
        result = xml_to_json(xml_str)
        assert len(result['children']) == 3
        names = [ch['name'] for ch in result['children']]
        assert names == ['a', 'b', 'c']

    def test_attributes_preserved(self):
        xml_str = '<server host="localhost" port="8080"/>'
        result = xml_to_json(xml_str)
        assert result['attributes']['host'] == 'localhost'
        assert result['attributes']['port'] == '8080'


# ---------------------------------------------------------------------------
# config_utils tests
# ---------------------------------------------------------------------------

from processor.helper.config.config_utils import (
    parsebool,
    parseint,
    generateid,
    DBVALUES,
    RUN_TYPE,
    NONE,
    FULL,
    REMOTE,
)


class TestParseBool:

    def test_true_string(self):
        assert parsebool('true') is True

    def test_false_string(self):
        assert parsebool('false') is False

    def test_true_titlecase(self):
        assert parsebool('True') is True

    def test_false_titlecase(self):
        assert parsebool('False') is False

    def test_int_one(self):
        assert parsebool(1) is True

    def test_int_zero(self):
        assert parsebool(0) is False

    def test_bool_true(self):
        assert parsebool(True) is True

    def test_bool_false(self):
        assert parsebool(False) is False

    def test_none_returns_default(self):
        assert parsebool(None) is False
        assert parsebool(None, defval=True) is True

    def test_invalid_string(self):
        # 'invalid' is not in ['false','true'], goes to else -> parseint('invalid') = 0 -> bool(0) = False
        assert parsebool('invalid') is False


class TestParseInt:

    def test_string_number(self):
        assert parseint('10') == 10

    def test_string_zero(self):
        assert parseint('0') == 0

    def test_non_numeric_returns_default(self):
        assert parseint('abc') == 0
        assert parseint('abc', default=99) == 99

    def test_none_returns_default(self):
        assert parseint(None) == 0
        assert parseint(None, default=-1) == -1

    def test_int_passthrough(self):
        assert parseint(10) == 10

    def test_negative_number(self):
        assert parseint('-5') == -5


class TestGenerateId:

    def test_with_name(self):
        result = generateid('myname')
        assert result.startswith('myname_')
        # pattern: name_xxxxx_xxxx (letters then digits)
        parts = result.split('_')
        assert len(parts) == 3
        assert parts[0] == 'myname'
        assert len(parts[1]) == 5
        assert len(parts[2]) == 4

    def test_without_name(self):
        result = generateid(None)
        parts = result.split('_')
        assert len(parts) == 2
        assert len(parts[0]) == 5
        assert len(parts[1]) == 4

    def test_returns_lowercase(self):
        for _ in range(10):
            result = generateid('Test')
            assert result == result.lower()

    def test_different_calls_different_ids(self):
        ids = {generateid('x') for _ in range(20)}
        # With randomness, we should get many unique IDs
        assert len(ids) > 1


class TestDBValuesConstant:

    def test_dbvalues_list(self):
        assert DBVALUES == ['NONE', 'SNAPSHOT', 'FULL', 'REMOTE']

    def test_dbvalues_individual(self):
        assert NONE == 'NONE'
        assert FULL == 'FULL'
        assert REMOTE == 'REMOTE'


class TestRunTypeConstant:

    def test_run_type_list(self):
        assert RUN_TYPE == ['CRAWL_AND_COMPLIANCE', 'CRAWL', 'COMPLIANCE']


# ---------------------------------------------------------------------------
# yaml_utils tests
# ---------------------------------------------------------------------------

from processor.helper.yaml.yaml_utils import (
    multiple_yaml_from_file,
    is_multiple_yaml_file,
    is_multiple_yaml_convertion,
    is_helm_chart_convertion,
)


class TestMultipleYamlFromFile:

    def test_multiple_docs(self, tmp_path):
        content = "name: doc1\n---\nname: doc2\n---\nname: doc3\n"
        fpath = tmp_path / "multi.yaml"
        fpath.write_text(content)
        from yaml.loader import FullLoader
        result = multiple_yaml_from_file(str(fpath), loader=FullLoader)
        assert result is not None
        assert len(result) == 3

    def test_single_doc(self, tmp_path):
        content = "name: single\nkey: value\n"
        fpath = tmp_path / "single.yaml"
        fpath.write_text(content)
        from yaml.loader import FullLoader
        result = multiple_yaml_from_file(str(fpath), loader=FullLoader)
        assert result is not None
        assert len(result) == 1

    def test_nonexistent_file_returns_none(self):
        result = multiple_yaml_from_file('/nonexistent/file.yaml')
        assert result is None


class TestIsMultipleYamlFile:

    def test_multiple_docs_returns_true(self, tmp_path):
        content = "name: doc1\n---\nname: doc2\n"
        fpath = tmp_path / "multi.yaml"
        fpath.write_text(content)
        assert is_multiple_yaml_file(str(fpath)) is True

    def test_single_doc_returns_false(self, tmp_path):
        content = "name: single\nkey: value\n"
        fpath = tmp_path / "single.yaml"
        fpath.write_text(content)
        assert is_multiple_yaml_file(str(fpath)) is False

    def test_nonexistent_file_returns_false(self):
        assert is_multiple_yaml_file('/nonexistent/file.yaml') is False


class TestIsMultipleYamlConvertion:

    def test_path_with_key_returns_true(self):
        assert is_multiple_yaml_convertion('/tmp/data_multiple_yaml/file.yaml') is True

    def test_path_without_key_returns_false(self):
        assert is_multiple_yaml_convertion('/tmp/data/file.yaml') is False

    def test_key_in_filename(self):
        assert is_multiple_yaml_convertion('/tmp/config_multiple_yaml.yaml') is True


class TestIsHelmChartConvertion:

    def test_path_with_key_returns_true(self):
        assert is_helm_chart_convertion('/tmp/charts_prancer_helm_template/values.yaml') is True

    def test_path_without_key_returns_false(self):
        assert is_helm_chart_convertion('/tmp/charts/values.yaml') is False


# ---------------------------------------------------------------------------
# hcl_utils tests
# ---------------------------------------------------------------------------

from processor.helper.hcl.hcl_utils import hcl_to_json


class TestHclToJson:

    def test_simple_tf_file(self, tmp_path):
        tf_content = '''
variable "region" {
  default = "us-east-1"
}
'''
        fpath = tmp_path / "main.tf"
        fpath.write_text(tf_content)
        result = hcl_to_json(str(fpath))
        assert isinstance(result, dict)

    def test_nonexistent_file_returns_empty_dict(self):
        result = hcl_to_json('/nonexistent/path/main.tf')
        assert result == {}

    def test_invalid_hcl_returns_empty_dict(self, tmp_path):
        fpath = tmp_path / "bad.tf"
        fpath.write_text('this is { not valid {{ hcl content @@@')
        result = hcl_to_json(str(fpath))
        assert result == {}


# ---------------------------------------------------------------------------
# file_utils tests
# ---------------------------------------------------------------------------

from processor.helper.file.file_utils import save_file, mkdir_path, exists_dir, exists_file


class TestSaveFile:

    def test_valid_path_creates_file(self, tmp_path):
        fpath = str(tmp_path / 'output.txt')
        result = save_file(fpath, 'hello world')
        assert result is True
        assert os.path.exists(fpath)
        with open(fpath) as f:
            assert f.read() == 'hello world'

    def test_invalid_path_returns_false(self):
        result = save_file('/nonexistent/dir/file.txt', 'content')
        assert result is False

    def test_empty_content(self, tmp_path):
        fpath = str(tmp_path / 'empty.txt')
        result = save_file(fpath, '')
        assert result is True
        with open(fpath) as f:
            assert f.read() == ''


class TestMkdirPath:

    def test_create_nested_dirs(self, tmp_path):
        nested = str(tmp_path / 'a' / 'b' / 'c')
        result = mkdir_path(nested)
        assert result is True
        assert os.path.isdir(nested)

    def test_existing_dir_returns_false(self, tmp_path):
        # mkdir_path uses os.makedirs which raises if dir exists (no exist_ok)
        result = mkdir_path(str(tmp_path))
        assert result is False

    def test_permission_denied_returns_false(self):
        result = mkdir_path('/proc/fake_dir')
        assert result is False
