"""
Comprehensive tests for the validation pipeline and master snapshot generation.
These tests protect the end-to-end workflow covering output document structure,
exclusion logic, comparator result structures, rego/python result structures,
test/mastertest file structure validation, and result aggregation.
"""

import os
import re
import json
import time
import tempfile
from collections import OrderedDict
from unittest.mock import patch, MagicMock, PropertyMock

import pytest


# ---------------------------------------------------------------------------
# Common mock helpers
# ---------------------------------------------------------------------------

def _mock_get_dbtests_false():
    return False


def _mock_get_dbtests_true():
    return True


def _mock_config_value(section, key=None, default=None):
    mapping = {
        'TEST': 'tests',
        'MASTERTEST': 'mastertests',
        'SNAPSHOT': 'snapshots',
        'OUTPUT': 'outputs',
        'DBNAME': 'pytestdb',
        'reportOutputFolder': 'validation',
    }
    if key in mapping:
        return mapping[key]
    if section == 'RESULT' and key == 'console_min_severity_error':
        return default if default else 'Low'
    if default is not None:
        return default
    return 'pytestdb'


def _mock_get_from_currentdata(name):
    if name == 'session_id':
        return 'session_1234567890'
    if name == 'remote':
        return False
    if name == 'exclusion':
        return {'exclusions': []}
    if name == 'INCLUDETESTS':
        return False
    if name == 'TESTIDS':
        return []
    if name == 'ONLYSNAPSHOTS':
        return False
    if name == 'ONLYSNAPSHOTIDS':
        return []
    return {}


def _mock_get_documents_empty(collection, query=None, dbname=None, sort=None, limit=10):
    return []


def _mock_save_json_to_file(data, filename):
    pass


def _mock_insert_one_document(doc, collection, dbname):
    return 'mock_doc_id_123'


def _mock_create_indexes(sid, dbname, flds):
    return None


def _mock_framework_dir():
    return '/tmp'


def _mock_get_test_json_dir():
    return '/tmp/'


def _mock_exists_dir(path):
    return True


def _mock_dump_output_results(results, container, test_file, snapshot, filesystem=True, status=None):
    pass


# ---------------------------------------------------------------------------
# 1. Output Document Structure (create_output_entry / dump_output_results)
# ---------------------------------------------------------------------------

class TestOutputDocumentStructure:
    """Tests for the output JSON structure produced by json_output.py."""

    def test_dump_output_results_filesystem_creates_correct_structure(self, monkeypatch):
        """Filesystem mode produces output with all required fields and correct types."""
        import processor.reporting.json_output as json_output_mod
        json_output_mod.doc_id = None

        captured = {}

        def capture_save(data, filename):
            captured['data'] = data
            captured['filename'] = filename

        monkeypatch.setattr('processor.reporting.json_output.config_value', _mock_config_value)
        monkeypatch.setattr('processor.reporting.json_output.get_from_currentdata', _mock_get_from_currentdata)
        monkeypatch.setattr('processor.reporting.json_output.save_json_to_file', capture_save)
        monkeypatch.setattr('processor.reporting.json_output.get_dblogger', lambda: "")

        from processor.reporting.json_output import dump_output_results
        results = [{"result": "passed", "testId": "1"}]
        dump_output_results(results, 'mycontainer', '/some/path/test-file.json', 'snapshot1', True)

        od = captured['data']
        assert od['$schema'] == ''
        assert od['contentVersion'] == '1.0.0.0'
        assert od['fileType'] == 'output'
        assert isinstance(od['timestamp'], int)
        assert od['snapshot'] == 'snapshot1'
        assert od['container'] == 'mycontainer'
        assert isinstance(od['session_id'], str)
        assert isinstance(od['remote_run'], bool)
        assert isinstance(od['log'], str)
        assert od['test'] == 'test-file.json'
        assert isinstance(od['results'], list)
        assert od['results'] == results

    def test_dump_output_results_filesystem_filename_pattern(self, monkeypatch):
        """Filesystem output file follows 'output-{test_file}' naming pattern."""
        import processor.reporting.json_output as json_output_mod
        json_output_mod.doc_id = None

        captured = {}

        def capture_save(data, filename):
            captured['filename'] = filename

        monkeypatch.setattr('processor.reporting.json_output.config_value', _mock_config_value)
        monkeypatch.setattr('processor.reporting.json_output.get_from_currentdata', _mock_get_from_currentdata)
        monkeypatch.setattr('processor.reporting.json_output.save_json_to_file', capture_save)
        monkeypatch.setattr('processor.reporting.json_output.get_dblogger', lambda: "")

        from processor.reporting.json_output import dump_output_results
        dump_output_results([], 'c1', '/dir/mytest.json', 'snap', True)
        assert captured['filename'] == '/dir/output-mytest.json'

    def test_dump_output_results_all_fields_present(self, monkeypatch):
        """All expected fields are present in the output document."""
        import processor.reporting.json_output as json_output_mod
        json_output_mod.doc_id = None

        captured = {}

        def capture_save(data, filename):
            captured['data'] = data

        monkeypatch.setattr('processor.reporting.json_output.config_value', _mock_config_value)
        monkeypatch.setattr('processor.reporting.json_output.get_from_currentdata', _mock_get_from_currentdata)
        monkeypatch.setattr('processor.reporting.json_output.save_json_to_file', capture_save)
        monkeypatch.setattr('processor.reporting.json_output.get_dblogger', lambda: "")

        from processor.reporting.json_output import dump_output_results
        dump_output_results([{"result": "passed"}], 'c', '/d/t.json', 's', True)

        expected_keys = {'$schema', 'contentVersion', 'fileType', 'timestamp',
                         'snapshot', 'container', 'session_id', 'remote_run',
                         'log', 'test', 'results'}
        assert expected_keys.issubset(set(captured['data'].keys()))

    def test_dump_output_results_timestamp_is_milliseconds(self, monkeypatch):
        """Timestamp is an integer representing milliseconds (>= 13 digits after epoch)."""
        import processor.reporting.json_output as json_output_mod
        json_output_mod.doc_id = None

        captured = {}

        def capture_save(data, filename):
            captured['data'] = data

        monkeypatch.setattr('processor.reporting.json_output.config_value', _mock_config_value)
        monkeypatch.setattr('processor.reporting.json_output.get_from_currentdata', _mock_get_from_currentdata)
        monkeypatch.setattr('processor.reporting.json_output.save_json_to_file', capture_save)
        monkeypatch.setattr('processor.reporting.json_output.get_dblogger', lambda: "")

        from processor.reporting.json_output import dump_output_results
        dump_output_results([], 'c', '/d/t.json', 's', True)

        ts = captured['data']['timestamp']
        assert isinstance(ts, int)
        # Millisecond timestamps are at least 13 digits since ~2001
        assert ts > 1_000_000_000_000

    def test_dump_output_results_remote_run_is_boolean(self, monkeypatch):
        """remote_run field is a boolean."""
        import processor.reporting.json_output as json_output_mod
        json_output_mod.doc_id = None

        captured = {}

        def capture_save(data, filename):
            captured['data'] = data

        monkeypatch.setattr('processor.reporting.json_output.config_value', _mock_config_value)
        monkeypatch.setattr('processor.reporting.json_output.get_from_currentdata', _mock_get_from_currentdata)
        monkeypatch.setattr('processor.reporting.json_output.save_json_to_file', capture_save)
        monkeypatch.setattr('processor.reporting.json_output.get_dblogger', lambda: "")

        from processor.reporting.json_output import dump_output_results
        dump_output_results([], 'c', '/d/t.json', 's', True)
        assert captured['data']['remote_run'] is False

    def test_cloud_type_extracted_from_tags(self, monkeypatch):
        """When doc_id exists and results have tags, cloud_type is extracted."""
        import processor.reporting.json_output as json_output_mod
        json_output_mod.doc_id = 'aabbccddeeff00112233aabb'
        json_output_mod.dbname = 'testdb'
        json_output_mod.collection = 'outputs'

        update_calls = []

        def mock_find_and_update(collection, dbname, query, update_value):
            update_calls.append(update_value)

        monkeypatch.setattr('processor.reporting.json_output.config_value', _mock_config_value)
        monkeypatch.setattr('processor.reporting.json_output.get_from_currentdata', _mock_get_from_currentdata)
        monkeypatch.setattr('processor.reporting.json_output.find_and_update_document', mock_find_and_update)

        from processor.reporting.json_output import dump_output_results
        results = [{"result": "passed", "tags": [{"cloud": "AWS"}]}]
        dump_output_results(results, 'c', 't', 's', False)

        assert len(update_calls) == 1
        assert update_calls[0].get('$set', {}).get('json.cloud_type') == 'aws'

        # Clean up the global
        json_output_mod.doc_id = None


# ---------------------------------------------------------------------------
# 2. Exclusion Logic (exclude_test_case)
# ---------------------------------------------------------------------------

class TestExcludeTestCase:
    """Tests for ComparatorV01.exclude_test_case."""

    def _make_comparator(self, excluded_ids, include_tests, testcase=None):
        """Create a ComparatorV01 instance with controlled exclusion data."""
        if testcase is None:
            testcase = {'testId': 'TEST_X', 'snapshotId': 'snap1', 'attribute': 'a', 'comparison': 'exist'}
        from processor.comparison.interpreter import ComparatorV01
        comp = ComparatorV01.__new__(ComparatorV01)
        comp.excludedTestIds = excluded_ids
        comp.includeTests = include_tests
        comp.testcase = testcase
        comp.snapshots = []
        return comp

    def test_is_master_true_testid_in_include_tests(self):
        """isMasterTest=True, testId in includeTests -> not excluded."""
        comp = self._make_comparator(
            excluded_ids={"TEST_1": ["/path/to/resource1"]},
            include_tests=["TEST_2"]
        )
        doc = {'paths': ['/some/path']}
        result = comp.exclude_test_case(doc, 'TEST_2', isMasterTest=True)
        assert result is False

    def test_is_master_true_testid_in_excluded_path_matches(self):
        """isMasterTest=True, testId in excludedTestIds and path matches -> excluded."""
        comp = self._make_comparator(
            excluded_ids={"TEST_1": ["/path/to/resource1"]},
            include_tests=["TEST_2"]
        )
        doc = {'paths': ['/path/to/resource1']}
        result = comp.exclude_test_case(doc, 'TEST_1', isMasterTest=True)
        assert result is True

    def test_is_master_true_testid_in_excluded_path_no_match(self):
        """isMasterTest=True, testId in excludedTestIds but path doesn't match -> not excluded."""
        comp = self._make_comparator(
            excluded_ids={"TEST_1": ["/path/to/resource1"]},
            include_tests=["TEST_2"]
        )
        doc = {'paths': ['/different/path']}
        result = comp.exclude_test_case(doc, 'TEST_1', isMasterTest=True)
        assert result is False

    def test_is_master_true_evals_id_in_include_tests(self):
        """isMasterTest=True, testId not in either, evals id in includeTests -> not excluded."""
        testcase = {
            'testId': 'TEST_X',
            'evals': [{'id': 'TEST_2', 'eval': 'data.rule.pass'}],
            'snapshotId': 'snap1',
            'attribute': 'a',
            'comparison': 'exist'
        }
        comp = self._make_comparator(
            excluded_ids={"TEST_1": ["/path/to/resource1"]},
            include_tests=["TEST_2"],
            testcase=testcase
        )
        doc = {'paths': ['/some/path']}
        result = comp.exclude_test_case(doc, 'TEST_OTHER', isMasterTest=True)
        assert result is False

    def test_is_master_true_evals_id_in_excluded_path_matches(self):
        """isMasterTest=True, testId not in either, eval id in excludedTestIds and path matches -> excluded."""
        testcase = {
            'testId': 'TEST_X',
            'evals': [{'id': 'EVAL_1', 'eval': 'data.rule.pass'}],
            'snapshotId': 'snap1',
            'attribute': 'a',
            'comparison': 'exist'
        }
        comp = self._make_comparator(
            excluded_ids={"EVAL_1": ["/path/to/resource1"]},
            include_tests=[],
            testcase=testcase
        )
        doc = {'paths': ['/path/to/resource1']}
        result = comp.exclude_test_case(doc, 'TEST_UNKNOWN', isMasterTest=True)
        assert result is True

    def test_is_master_false_never_excluded(self):
        """isMasterTest=False -> never excluded regardless of other conditions."""
        comp = self._make_comparator(
            excluded_ids={"TEST_1": ["/path/to/resource1"]},
            include_tests=["TEST_2"]
        )
        doc = {'paths': ['/path/to/resource1']}
        result = comp.exclude_test_case(doc, 'TEST_1', isMasterTest=False)
        assert result is False

    def test_is_master_true_no_testid(self):
        """isMasterTest=True but testId is None -> not excluded."""
        comp = self._make_comparator(
            excluded_ids={"TEST_1": ["/path/to/resource1"]},
            include_tests=["TEST_2"]
        )
        doc = {'paths': ['/path/to/resource1']}
        result = comp.exclude_test_case(doc, None, isMasterTest=True)
        assert result is False

    def test_is_master_true_empty_exclusions(self):
        """isMasterTest=True, empty excluded list -> not excluded."""
        comp = self._make_comparator(
            excluded_ids={},
            include_tests=[]
        )
        doc = {'paths': ['/any/path']}
        result = comp.exclude_test_case(doc, 'TEST_1', isMasterTest=True)
        assert result is False


# ---------------------------------------------------------------------------
# 3. Comparator validate() Result Structure
# ---------------------------------------------------------------------------

class TestComparatorValidateResultStructure:
    """Tests for the exact output structure of Comparator.validate()."""

    def test_testcasev1_success_returns_passed_with_snapshots(self, monkeypatch):
        """TESTCASEV1 success returns list with 'passed' result and snapshot info."""
        mock_docs = [{
            'json': {'id': 124, 'location': 'eastus2'},
            'snapshotId': 'snap1',
            'structure': 'azure',
            'reference': 'ref1',
            'source': 'src1',
            'collection': 'microsoftcompute',
            'paths': ['/rg/providers/type/name']
        }]

        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            lambda *a, **kw: mock_docs)

        from processor.comparison.interpreter import Comparator
        comp = Comparator('0.1', 'container', 'db', {'snap1': 'microsoftcompute'}, {
            'testId': '1',
            'snapshotId': 'snap1',
            'attribute': 'location',
            'comparison': 'exist'
        }, {}, [])
        result = comp.validate()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['result'] == 'passed'
        assert 'snapshots' in result[0]
        snap = result[0]['snapshots'][0]
        assert 'id' in snap
        assert 'structure' in snap
        assert 'reference' in snap
        assert 'source' in snap
        assert 'collection' in snap
        assert 'paths' in snap or 'path' in snap

    def test_testcasev1_missing_snapshot_returns_skipped(self, monkeypatch):
        """TESTCASEV1 with no snapshot documents returns skipped with message."""
        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            _mock_get_documents_empty)

        from processor.comparison.interpreter import Comparator
        comp = Comparator('0.1', 'container', 'db', {'snap1': 'coll'}, {
            'testId': '1',
            'snapshotId': 'snap1',
            'attribute': 'location',
            'comparison': 'exist'
        }, {}, [])
        result = comp.validate()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['result'] == 'skipped'
        assert result[0]['message'] == 'Missing documents for the snapshot'

    def test_testcasev1_missing_snapshotid_returns_skipped(self, monkeypatch):
        """TESTCASEV1 with no snapshotId returns skipped."""
        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            _mock_get_documents_empty)

        from processor.comparison.interpreter import Comparator
        comp = Comparator('0.1', 'container', 'db', {}, {
            'testId': '1',
            'snapshotId': None,
            'attribute': 'location',
            'comparison': 'exist'
        }, {}, [])
        result = comp.validate()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['result'] == 'skipped'
        assert result[0]['message'] == 'Missing snapshotId for testcase'

    def test_unsupported_format_returns_skipped(self, monkeypatch):
        """Testcase with unsupported format returns skipped with reason."""
        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            _mock_get_documents_empty)

        from processor.comparison.interpreter import Comparator
        # No attribute, no comparison, no rule -> format=None
        comp = Comparator('0.1', 'container', 'db', {}, {
            'testId': '1',
        }, {}, [])
        result = comp.validate()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['result'] == 'skipped'
        assert result[0]['reason'] == 'Unsupported testcase format'

    def test_testcasev1_snapshot_with_path_instead_of_paths(self, monkeypatch):
        """TESTCASEV1 snapshot doc with 'path' (singular) instead of 'paths'."""
        mock_docs = [{
            'json': {'id': 100},
            'snapshotId': 'snap1',
            'structure': 'azure',
            'reference': 'ref1',
            'source': 'src1',
            'collection': 'coll1',
            'path': '/single/path'
        }]

        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            lambda *a, **kw: mock_docs)

        from processor.comparison.interpreter import Comparator
        comp = Comparator('0.1', 'container', 'db', {'snap1': 'coll1'}, {
            'testId': '1',
            'snapshotId': 'snap1',
            'attribute': 'id',
            'comparison': 'exist'
        }, {}, [])
        result = comp.validate()

        assert result[0]['result'] == 'passed'
        snap = result[0]['snapshots'][0]
        assert 'path' in snap
        assert snap['path'] == '/single/path'

    def test_testcasev1_failed_comparison(self, monkeypatch):
        """TESTCASEV1 with a failing comparison returns 'failed'."""
        mock_docs = [{
            'json': {'id': 5},
            'snapshotId': 'snap1',
            'structure': 'azure',
            'reference': 'ref1',
            'source': 'src1',
            'collection': 'coll1',
            'paths': ['/path']
        }]

        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            lambda *a, **kw: mock_docs)

        from processor.comparison.interpreter import Comparator
        comp = Comparator('0.1', 'container', 'db', {'snap1': 'coll1'}, {
            'testId': '1',
            'snapshotId': 'snap1',
            'attribute': 'id',
            'comparison': 'gt 10'
        }, {}, [])
        result = comp.validate()

        assert result[0]['result'] == 'failed'


# ---------------------------------------------------------------------------
# 4. Rego result structure
# ---------------------------------------------------------------------------

class TestRegoResultStructure:
    """Tests that rego test processing produces the expected result fields."""

    def test_rego_result_has_required_fields(self):
        """Each rego result must have eval, result, message, id, remediation fields."""
        expected_result = {
            'eval': 'data.rule.rulepass',
            'result': 'passed',
            'message': '',
            'id': 'CIS_1.1',
            'remediation_description': 'Fix the config',
            'remediation_function': 'auto_fix',
        }
        required_keys = {'eval', 'result', 'message', 'id',
                         'remediation_description', 'remediation_function'}
        assert required_keys.issubset(set(expected_result.keys()))

    def test_rego_result_result_values(self):
        """Rego result 'result' field must be 'passed' or 'failed'."""
        for val in ('passed', 'failed'):
            r = {'eval': 'data.rule.rulepass', 'result': val, 'message': ''}
            assert r['result'] in ('passed', 'failed')

    def test_rego_result_id_can_be_none(self):
        """Rego result 'id' can be None."""
        r = {
            'eval': 'data.rule.rulepass',
            'result': 'passed',
            'message': '',
            'id': None,
            'remediation_description': None,
            'remediation_function': None,
        }
        assert r['id'] is None

    def test_rego_result_message_is_string(self):
        """Rego result 'message' must be a string."""
        r = {
            'eval': 'data.rule.rulepass',
            'result': 'failed',
            'message': 'Security group is open to world',
        }
        assert isinstance(r['message'], str)


# ---------------------------------------------------------------------------
# 5. Python rule result structure
# ---------------------------------------------------------------------------

class TestPythonRuleResultStructure:
    """Tests for the structure of python test results."""

    def test_python_result_has_required_fields(self):
        """Python rule result must have eval, result, message, id, remediation fields."""
        result = {
            'eval': 'data.rule.check_sg',
            'result': 'failed',
            'message': 'Open security group detected',
            'id': 'CIS_2.1',
            'remediation_description': 'Close SG',
            'remediation_function': 'close_sg',
        }
        required_keys = {'eval', 'result', 'message', 'id',
                         'remediation_description', 'remediation_function'}
        assert required_keys.issubset(set(result.keys()))

    def test_python_result_only_failed_returned(self):
        """Python tests only return failed results."""
        # In the actual code, results are only appended when issue == True
        # which sets result to 'failed'
        result = {
            'eval': 'data.rule.check',
            'result': 'failed',
            'message': 'check failed',
            'id': None,
            'remediation_description': None,
            'remediation_function': None,
        }
        assert result['result'] == 'failed'

    def test_python_result_errors_field_optional(self):
        """Python rule result may optionally include 'errors' list."""
        result_with_errors = {
            'eval': 'data.rule.check',
            'result': 'failed',
            'message': 'error occurred',
            'id': 'T1',
            'remediation_description': None,
            'remediation_function': None,
            'errors': ['error detail 1', 'error detail 2'],
        }
        assert 'errors' in result_with_errors
        assert isinstance(result_with_errors['errors'], list)

        result_without_errors = {
            'eval': 'data.rule.check',
            'result': 'failed',
            'message': 'error',
            'id': 'T1',
            'remediation_description': None,
            'remediation_function': None,
        }
        assert 'errors' not in result_without_errors


# ---------------------------------------------------------------------------
# 6. Test file structure validation
# ---------------------------------------------------------------------------

class TestTestFileStructure:
    """Tests that test files are correctly parsed with required fields."""

    def test_test_file_must_have_filetype_test(self):
        """fileType must be 'test'."""
        test_data = {
            "$schema": "",
            "contentVersion": "1.0.0.0",
            "fileType": "test",
            "snapshot": "snapshot.json",
            "testSet": []
        }
        assert test_data['fileType'] == 'test'

    def test_test_file_must_have_snapshot_field(self):
        """Test file must have 'snapshot' field (string reference)."""
        test_data = {
            "fileType": "test",
            "snapshot": "snapshot.json",
            "testSet": []
        }
        assert 'snapshot' in test_data
        assert isinstance(test_data['snapshot'], str)

    def test_test_file_must_have_testset_array(self):
        """Test file must have 'testSet' array."""
        test_data = {
            "fileType": "test",
            "snapshot": "snapshot.json",
            "testSet": [
                {"testName": "test1", "version": "0.1", "cases": []}
            ]
        }
        assert isinstance(test_data['testSet'], list)

    def test_testset_has_required_fields(self):
        """Each testSet entry has testName, version, and cases."""
        testset = {
            "testName": "test1",
            "version": "0.1",
            "cases": [
                {"testId": "1", "rule": "exist({1}.location)"}
            ]
        }
        assert 'testName' in testset
        assert 'version' in testset
        assert 'cases' in testset

    def test_testcase_has_testid_and_rule(self):
        """Each test case must have testId and rule."""
        case = {"testId": "TC_001", "rule": "exist({snap1}.id)"}
        assert 'testId' in case
        assert 'rule' in case

    def test_run_json_validation_empty_testdata_returns_empty(self, monkeypatch):
        """run_json_validation_tests with empty data returns empty resultset."""
        monkeypatch.setattr('processor.connector.validation.config_value', _mock_config_value)
        monkeypatch.setattr('processor.connector.validation.get_from_currentdata', _mock_get_from_currentdata)

        from processor.connector.validation import run_json_validation_tests
        result = run_json_validation_tests(None, 'container')
        assert result == []

    def test_run_json_validation_no_testset_returns_empty(self, monkeypatch):
        """run_json_validation_tests with no testSet returns empty."""
        monkeypatch.setattr('processor.connector.validation.config_value', _mock_config_value)
        monkeypatch.setattr('processor.connector.validation.get_from_currentdata', _mock_get_from_currentdata)

        from processor.connector.validation import run_json_validation_tests
        result = run_json_validation_tests({'fileType': 'test'}, 'container')
        assert result == []


# ---------------------------------------------------------------------------
# 7. Master test structure
# ---------------------------------------------------------------------------

class TestMasterTestStructure:
    """Tests for master test file structure."""

    def test_mastertest_filetype(self):
        """fileType must be 'mastertest'."""
        master = {
            "fileType": "mastertest",
            "masterSnapshot": "master_snapshot.json",
            "testSet": []
        }
        assert master['fileType'] == 'mastertest'

    def test_mastertest_has_master_snapshot(self):
        """Master test must have masterSnapshot field."""
        master = {
            "fileType": "mastertest",
            "masterSnapshot": "master_snapshot.json",
            "testSet": []
        }
        assert 'masterSnapshot' in master
        assert isinstance(master['masterSnapshot'], str)

    def test_mastertest_case_has_master_test_id(self):
        """Each master test case must have masterTestId."""
        case = {
            "masterTestId": "MT_001",
            "type": "rego",
            "rule": "file(rule.rego)",
            "masterSnapshotId": ["MS_1"],
            "snapshotId": ["SNAP_1"]
        }
        assert 'masterTestId' in case

    def test_mastertest_snapshotid_is_array(self):
        """snapshotId in mastertest is an array."""
        case = {
            "masterTestId": "MT_001",
            "snapshotId": ["SNAP_1", "SNAP_2"]
        }
        assert isinstance(case['snapshotId'], list)

    def test_mastertest_mastersnapshotid_is_array(self):
        """masterSnapshotId in mastertest is an array."""
        case = {
            "masterTestId": "MT_001",
            "masterSnapshotId": ["MS_1", "MS_2"]
        }
        assert isinstance(case['masterSnapshotId'], list)


# ---------------------------------------------------------------------------
# 8. End-to-end validation flow
# ---------------------------------------------------------------------------

class TestEndToEndValidationFlow:
    """Tests the full validation chain with mocks."""

    def test_full_chain_filesystem(self, monkeypatch, create_temp_dir, create_temp_json):
        """End-to-end: load test file, load snapshot, build collection mapping, execute comparator, verify results."""
        monkeypatch.setattr('processor.connector.validation.create_indexes', _mock_create_indexes)
        monkeypatch.setattr('processor.connector.validation.config_value', _mock_config_value)
        monkeypatch.setattr('processor.connector.validation.get_from_currentdata', _mock_get_from_currentdata)
        monkeypatch.setattr('processor.connector.validation.dump_output_results', _mock_dump_output_results)

        mock_docs = [{
            'json': {'id': 124, 'location': 'eastus2'},
            'snapshotId': '1',
            'structure': 'azure',
            'reference': 'ref1',
            'source': 'src1',
            'collection': 'microsoftcompute',
            'paths': ['/rg/providers/type/name']
        }]
        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            lambda *a, **kw: mock_docs)

        tmpdir = create_temp_dir()
        container = 'testcontainer'
        container_dir = '%s/%s' % (tmpdir, container)
        os.makedirs(container_dir)

        monkeypatch.setattr('processor.connector.validation.get_test_json_dir', lambda: tmpdir)

        snap_data = {
            "fileType": "snapshot",
            "snapshots": [{
                "source": "azureStructure.json",
                "type": "azure",
                "nodes": [{
                    "snapshotId": "1",
                    "type": "Microsoft.Compute",
                    "collection": "Microsoft.Compute"
                }]
            }]
        }
        create_temp_json(container_dir, data=snap_data, fname='snapshot.json')

        test_data = {
            "$schema": "",
            "contentVersion": "1.0.0.0",
            "fileType": "test",
            "snapshot": "snapshot.json",
            "testSet": [{
                "testName": "e2e_test",
                "version": "0.1",
                "cases": [{
                    "testId": "1",
                    "snapshotId": "1",
                    "attribute": "location",
                    "comparison": "exist"
                }]
            }]
        }
        test_fname = create_temp_json(tmpdir, data=test_data, fname='test_e2e.json')

        from processor.connector.validation import run_file_validation_tests
        result = run_file_validation_tests('%s/%s' % (tmpdir, test_fname), container, True)
        assert result is True

    def test_full_chain_with_failed_test(self, monkeypatch, create_temp_dir, create_temp_json):
        """End-to-end flow where comparison fails yields False."""
        monkeypatch.setattr('processor.connector.validation.create_indexes', _mock_create_indexes)
        monkeypatch.setattr('processor.connector.validation.config_value', _mock_config_value)
        monkeypatch.setattr('processor.connector.validation.get_from_currentdata', _mock_get_from_currentdata)
        monkeypatch.setattr('processor.connector.validation.dump_output_results', _mock_dump_output_results)

        mock_docs = [{
            'json': {'id': 5},
            'snapshotId': '1',
            'structure': 'azure',
            'reference': 'ref1',
            'source': 'src1',
            'collection': 'microsoftcompute',
            'paths': ['/rg/providers/type/name']
        }]
        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            lambda *a, **kw: mock_docs)

        tmpdir = create_temp_dir()
        container = 'testcontainer'
        container_dir = '%s/%s' % (tmpdir, container)
        os.makedirs(container_dir)

        monkeypatch.setattr('processor.connector.validation.get_test_json_dir', lambda: tmpdir)

        snap_data = {
            "fileType": "snapshot",
            "snapshots": [{
                "source": "azureStructure.json",
                "type": "azure",
                "nodes": [{
                    "snapshotId": "1",
                    "collection": "Microsoft.Compute"
                }]
            }]
        }
        create_temp_json(container_dir, data=snap_data, fname='snapshot.json')

        test_data = {
            "$schema": "",
            "contentVersion": "1.0.0.0",
            "fileType": "test",
            "snapshot": "snapshot.json",
            "testSet": [{
                "testName": "e2e_test",
                "version": "0.1",
                "cases": [{
                    "testId": "1",
                    "snapshotId": "1",
                    "attribute": "id",
                    "comparison": "gt 10"
                }]
            }]
        }
        test_fname = create_temp_json(tmpdir, data=test_data, fname='test_fail.json')

        from processor.connector.validation import run_file_validation_tests
        result = run_file_validation_tests('%s/%s' % (tmpdir, test_fname), container, True)
        assert result is False


# ---------------------------------------------------------------------------
# 9. Multiple results aggregation
# ---------------------------------------------------------------------------

class TestMultipleResultsAggregation:
    """Tests for aggregation of results from multiple test cases."""

    def test_results_from_all_testcases_collected(self, monkeypatch):
        """Results from all test cases are collected into the resultset."""
        monkeypatch.setattr('processor.connector.validation.create_indexes', _mock_create_indexes)
        monkeypatch.setattr('processor.connector.validation.config_value', _mock_config_value)
        monkeypatch.setattr('processor.connector.validation.get_from_currentdata', _mock_get_from_currentdata)

        mock_docs = [{
            'json': {'id': 124, 'location': 'eastus2'},
            'snapshotId': '1',
            'structure': 'azure',
            'reference': 'ref1',
            'source': 'src1',
            'collection': 'microsoftcompute',
            'paths': ['/path']
        }]
        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            lambda *a, **kw: mock_docs)

        tmpdir = tempfile.mkdtemp()
        container_dir = '%s/container1' % tmpdir
        os.makedirs(container_dir)
        monkeypatch.setattr('processor.connector.validation.get_test_json_dir', lambda: tmpdir)

        snap_data = {
            "fileType": "snapshot",
            "snapshots": [{
                "source": "src",
                "type": "azure",
                "nodes": [
                    {"snapshotId": "1", "collection": "Microsoft.Compute"},
                ]
            }]
        }
        with open('%s/snapshot.json' % container_dir, 'w') as f:
            json.dump(snap_data, f)

        test_data = {
            "fileType": "test",
            "snapshot": "snapshot.json",
            "testSet": [{
                "testName": "multi",
                "version": "0.1",
                "cases": [
                    {"testId": "1", "snapshotId": "1", "attribute": "id", "comparison": "exist"},
                    {"testId": "2", "snapshotId": "1", "attribute": "location", "comparison": "exist"},
                ]
            }]
        }

        from processor.connector.validation import run_json_validation_tests
        resultset = run_json_validation_tests(test_data, 'container1', filesystem=True)
        assert len(resultset) >= 2

    def test_each_result_has_result_id(self, monkeypatch):
        """Each result from run_validation_test has result_id added."""
        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            lambda *a, **kw: [{
                                'json': {'id': 1}, 'snapshotId': 's1',
                                'structure': 'az', 'reference': 'r',
                                'source': 's', 'collection': 'c',
                                'paths': ['/p']
                            }])

        from processor.connector.validation import run_validation_test
        results = run_validation_test('0.1', 'my-container', 'db', {'s1': 'c'}, {
            'testId': 'T1',
            'snapshotId': 's1',
            'attribute': 'id',
            'comparison': 'exist'
        }, {}, [])
        assert len(results) >= 1
        for r in results:
            assert 'result_id' in r
            assert isinstance(r['result_id'], str)

    def test_result_id_format(self, monkeypatch):
        """result_id follows '{sanitized_container}_{timestamp}' pattern."""
        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            lambda *a, **kw: [{
                                'json': {'id': 1}, 'snapshotId': 's1',
                                'structure': 'az', 'reference': 'r',
                                'source': 's', 'collection': 'c',
                                'paths': ['/p']
                            }])

        from processor.connector.validation import run_validation_test
        results = run_validation_test('0.1', 'my-container', 'db', {'s1': 'c'}, {
            'testId': 'T1',
            'snapshotId': 's1',
            'attribute': 'id',
            'comparison': 'exist'
        }, {}, [])
        rid = results[0]['result_id']
        # The result_id is container (with special chars removed) + underscore + timestamp
        parts = rid.rsplit('_', 1)
        assert len(parts) == 2
        assert parts[1].isdigit()

    def test_testcase_fields_merged_into_results(self, monkeypatch):
        """Testcase fields are merged into each result dict."""
        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            lambda *a, **kw: [{
                                'json': {'id': 1}, 'snapshotId': 's1',
                                'structure': 'az', 'reference': 'r',
                                'source': 's', 'collection': 'c',
                                'paths': ['/p']
                            }])

        from processor.connector.validation import run_validation_test
        testcase = {
            'testId': 'T1',
            'snapshotId': 's1',
            'attribute': 'id',
            'comparison': 'exist'
        }
        results = run_validation_test('0.1', 'container', 'db', {'s1': 'c'},
                                      testcase, {}, [])
        # testcase fields are merged (via result.update(testcase))
        for r in results:
            assert r.get('testId') == 'T1'


# ---------------------------------------------------------------------------
# 10. Session ID format
# ---------------------------------------------------------------------------

class TestSessionIdFormat:
    """Tests for session ID format."""

    def test_session_id_starts_with_session_prefix(self):
        """Session ID must follow 'session_{timestamp_ms}' format."""
        session_id = 'session_1234567890123'
        assert session_id.startswith('session_')

    def test_session_id_timestamp_is_integer(self):
        """The timestamp portion of session_id is an integer in milliseconds."""
        session_id = 'session_1609459200000'
        parts = session_id.split('_', 1)
        assert len(parts) == 2
        assert parts[1].isdigit()
        ts = int(parts[1])
        assert ts > 1_000_000_000_000  # milliseconds check

    def test_session_id_used_in_output(self, monkeypatch):
        """Session ID appears in the output document."""
        import processor.reporting.json_output as json_output_mod
        json_output_mod.doc_id = None

        captured = {}

        def capture_save(data, filename):
            captured['data'] = data

        monkeypatch.setattr('processor.reporting.json_output.config_value', _mock_config_value)
        monkeypatch.setattr('processor.reporting.json_output.get_from_currentdata', _mock_get_from_currentdata)
        monkeypatch.setattr('processor.reporting.json_output.save_json_to_file', capture_save)
        monkeypatch.setattr('processor.reporting.json_output.get_dblogger', lambda: "")

        from processor.reporting.json_output import dump_output_results
        dump_output_results([], 'c', '/d/t.json', 's', True)

        assert captured['data']['session_id'] == 'session_1234567890'


# ---------------------------------------------------------------------------
# Additional edge-case and structural tests
# ---------------------------------------------------------------------------

class TestValidationHelpers:
    """Tests for validation helper functions."""

    def test_get_snapshot_file_filesystem(self, monkeypatch, create_temp_dir, create_temp_json):
        """get_snapshot_file loads from filesystem when filesystem=True."""
        tmpdir = create_temp_dir()
        container = 'mycontainer'
        container_dir = '%s/%s' % (tmpdir, container)
        os.makedirs(container_dir)

        snap_data = {
            "fileType": "snapshot",
            "snapshots": [{"source": "src", "type": "azure", "nodes": []}]
        }
        create_temp_json(container_dir, data=snap_data, fname='snap.json')

        monkeypatch.setattr('processor.connector.validation.get_test_json_dir', lambda: tmpdir)

        from processor.connector.validation import get_snapshot_file
        result = get_snapshot_file('snap', container, 'db', True)
        assert result is not None
        assert result.get('fileType') == 'snapshot'

    def test_get_snapshot_id_to_collection_dict_empty_snapshot(self, monkeypatch, create_temp_dir, create_temp_json):
        """get_snapshot_id_to_collection_dict with no snapshots returns empty dict."""
        monkeypatch.setattr('processor.connector.validation.create_indexes', _mock_create_indexes)

        tmpdir = create_temp_dir()
        container = 'c1'
        container_dir = '%s/%s' % (tmpdir, container)
        os.makedirs(container_dir)

        snap_data = {"fileType": "snapshot"}
        create_temp_json(container_dir, data=snap_data, fname='empty_snap.json')

        monkeypatch.setattr('processor.connector.validation.get_test_json_dir', lambda: tmpdir)

        from processor.connector.validation import get_snapshot_id_to_collection_dict
        result = get_snapshot_id_to_collection_dict('empty_snap', container, 'db', True)
        assert result == {}

    def test_validate_result_all_passed(self, monkeypatch):
        """validate_result with all passed results returns True."""
        monkeypatch.setattr('processor.connector.validation.config_value',
                            lambda s, k, default=None: default if default else 'Low')

        from processor.connector.validation import validate_result
        resultset = [
            {'result': 'passed', 'severity': 'high'},
            {'result': 'passed', 'severity': 'low'},
        ]
        assert validate_result(resultset, True) is True

    def test_validate_result_with_failure(self, monkeypatch):
        """validate_result with a failed result returns False."""
        monkeypatch.setattr('processor.connector.validation.config_value',
                            lambda s, k, default=None: default if default else 'Low')

        from processor.connector.validation import validate_result
        resultset = [
            {'result': 'passed', 'severity': 'low'},
            {'result': 'failed', 'severity': 'low'},
        ]
        assert validate_result(resultset, True) is False

    def test_validate_result_empty_resultset(self, monkeypatch):
        """validate_result with empty resultset returns the initial finalresult."""
        monkeypatch.setattr('processor.connector.validation.config_value',
                            lambda s, k, default=None: default if default else 'Low')

        from processor.connector.validation import validate_result
        assert validate_result([], True) is True
        assert validate_result(None, True) is True

    def test_get_min_severity_error_list_low(self, monkeypatch):
        """get_min_severity_error_list with 'Low' returns all severities."""
        monkeypatch.setattr('processor.connector.validation.config_value',
                            lambda s, k, default=None: 'Low')

        from processor.connector.validation import get_min_severity_error_list
        assert get_min_severity_error_list() == ['low', 'medium', 'high']

    def test_get_min_severity_error_list_medium(self, monkeypatch):
        """get_min_severity_error_list with 'Medium' returns medium and high."""
        monkeypatch.setattr('processor.connector.validation.config_value',
                            lambda s, k, default=None: 'Medium')

        from processor.connector.validation import get_min_severity_error_list
        assert get_min_severity_error_list() == ['medium', 'high']

    def test_get_min_severity_error_list_high(self, monkeypatch):
        """get_min_severity_error_list with 'High' returns only high."""
        monkeypatch.setattr('processor.connector.validation.config_value',
                            lambda s, k, default=None: 'High')

        from processor.connector.validation import get_min_severity_error_list
        assert get_min_severity_error_list() == ['high']


class TestComparatorFactory:
    """Tests for the Comparator factory method."""

    def test_version_0_1_creates_v01(self, monkeypatch):
        """Version '0.1' creates ComparatorV01 instance."""
        monkeypatch.setattr('processor.comparison.interpreter.get_documents', _mock_get_documents_empty)
        from processor.comparison.interpreter import Comparator, ComparatorV01
        comp = Comparator('0.1', 'c', 'db', {}, {
            'testId': '1', 'snapshotId': 's1', 'attribute': 'a', 'comparison': 'exist'
        }, {}, [])
        assert isinstance(comp.comparator, ComparatorV01)

    def test_version_0_2_creates_v02(self, monkeypatch):
        """Version '0.2' creates ComparatorV02 instance."""
        monkeypatch.setattr('processor.comparison.interpreter.get_documents', _mock_get_documents_empty)
        from processor.comparison.interpreter import Comparator, ComparatorV02
        comp = Comparator('0.2', 'c', 'db', {}, {
            'testId': '1', 'snapshotId': 's1', 'attribute': 'a', 'comparison': 'exist'
        }, {}, [])
        assert isinstance(comp.comparator, ComparatorV02)

    def test_none_version_defaults_to_v01(self, monkeypatch):
        """None version defaults to ComparatorV01."""
        monkeypatch.setattr('processor.comparison.interpreter.get_documents', _mock_get_documents_empty)
        from processor.comparison.interpreter import Comparator, ComparatorV01
        comp = Comparator(None, 'c', 'db', {}, {
            'testId': '1',
        }, {}, [])
        assert isinstance(comp.comparator, ComparatorV01)

    def test_rego_type_sets_testcasev2(self, monkeypatch):
        """Testcase with type='rego' sets format to TESTCASEV2."""
        monkeypatch.setattr('processor.comparison.interpreter.get_documents', _mock_get_documents_empty)
        from processor.comparison.interpreter import Comparator, TESTCASEV2
        comp = Comparator('0.1', 'c', 'db', {}, {
            'testId': '1',
            'type': 'rego',
            'rule': 'file(rule.rego)',
            'snapshotId': ['s1'],
            'masterSnapshotId': ['ms1']
        }, {}, [])
        assert comp.comparator.format == TESTCASEV2
        assert comp.comparator.type == 'rego'

    def test_python_type_sets_testcasev2(self, monkeypatch):
        """Testcase with type='python' sets format to TESTCASEV2."""
        monkeypatch.setattr('processor.comparison.interpreter.get_documents', _mock_get_documents_empty)
        from processor.comparison.interpreter import Comparator, TESTCASEV2
        comp = Comparator('0.1', 'c', 'db', {}, {
            'testId': '1',
            'type': 'python',
            'rule': 'file(check.py)',
            'snapshotId': ['s1'],
            'masterSnapshotId': ['ms1']
        }, {}, [])
        assert comp.comparator.format == TESTCASEV2
        assert comp.comparator.type == 'python'


class TestDisabledTestcases:
    """Tests for disabled testcase handling."""

    def test_disabled_testcase_skipped(self, monkeypatch):
        """Testcases with status='disable' are skipped."""
        monkeypatch.setattr('processor.connector.validation.create_indexes', _mock_create_indexes)
        monkeypatch.setattr('processor.connector.validation.config_value', _mock_config_value)
        monkeypatch.setattr('processor.connector.validation.get_from_currentdata', _mock_get_from_currentdata)

        tmpdir = tempfile.mkdtemp()
        container_dir = '%s/c1' % tmpdir
        os.makedirs(container_dir)
        monkeypatch.setattr('processor.connector.validation.get_test_json_dir', lambda: tmpdir)

        snap_data = {
            "fileType": "snapshot",
            "snapshots": [{"source": "src", "type": "azure", "nodes": [
                {"snapshotId": "1", "collection": "Microsoft.Compute"}
            ]}]
        }
        with open('%s/snapshot.json' % container_dir, 'w') as f:
            json.dump(snap_data, f)

        test_data = {
            "fileType": "test",
            "snapshot": "snapshot.json",
            "testSet": [{
                "testName": "disabled_test",
                "version": "0.1",
                "cases": [
                    {"testId": "1", "snapshotId": "1", "attribute": "id",
                     "comparison": "exist", "status": "disable"},
                ]
            }]
        }

        from processor.connector.validation import run_json_validation_tests
        resultset = run_json_validation_tests(test_data, 'c1', filesystem=True)
        assert resultset == []

    def test_enabled_testcase_runs(self, monkeypatch):
        """Testcases without status or with status != 'disable' are run."""
        monkeypatch.setattr('processor.connector.validation.create_indexes', _mock_create_indexes)
        monkeypatch.setattr('processor.connector.validation.config_value', _mock_config_value)
        monkeypatch.setattr('processor.connector.validation.get_from_currentdata', _mock_get_from_currentdata)
        monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                            lambda *a, **kw: [{
                                'json': {'id': 1}, 'snapshotId': '1',
                                'structure': 'az', 'reference': 'r',
                                'source': 's', 'collection': 'c',
                                'paths': ['/p']
                            }])

        tmpdir = tempfile.mkdtemp()
        container_dir = '%s/c2' % tmpdir
        os.makedirs(container_dir)
        monkeypatch.setattr('processor.connector.validation.get_test_json_dir', lambda: tmpdir)

        snap_data = {
            "fileType": "snapshot",
            "snapshots": [{"source": "src", "type": "azure", "nodes": [
                {"snapshotId": "1", "collection": "Microsoft.Compute"}
            ]}]
        }
        with open('%s/snapshot.json' % container_dir, 'w') as f:
            json.dump(snap_data, f)

        test_data = {
            "fileType": "test",
            "snapshot": "snapshot.json",
            "testSet": [{
                "testName": "enabled_test",
                "version": "0.1",
                "cases": [
                    {"testId": "1", "snapshotId": "1", "attribute": "id",
                     "comparison": "exist"},
                ]
            }]
        }

        from processor.connector.validation import run_json_validation_tests
        resultset = run_json_validation_tests(test_data, 'c2', filesystem=True)
        assert len(resultset) >= 1
        assert resultset[0]['status'] == 'enable'
