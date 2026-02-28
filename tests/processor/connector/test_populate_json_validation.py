"""
Comprehensive tests for validation functions in processor.connector.populate_json
and processor.helper.utils.cli_populate_json.
"""
import os
import sys
import copy
import time
import hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _silence_logger():
    """Silence the logger across all tests so log calls don't raise."""
    with patch("processor.connector.populate_json.logger"):
        yield


def _base_document_json(**overrides):
    """Return a minimal document_json that satisfies pop() calls."""
    doc = {
        "connector": "some_connector",
        "remoteFile": "path/to/file.json",
    }
    doc.update(overrides)
    return doc


# ===================================================================
# Tests for validate_snapshot_data
# ===================================================================

class TestValidateSnapshotData:

    def _call(self, snapshot_json, document_json, file_location="loc"):
        from processor.connector.populate_json import validate_snapshot_data
        return validate_snapshot_data(snapshot_json, document_json, file_location)

    # --- failure cases ---

    def test_missing_snapshots_key(self):
        result = self._call({}, {}, "f")
        assert result is False

    def test_snapshots_not_a_list_string(self):
        result = self._call({"snapshots": "not_a_list"}, {}, "f")
        assert result is False

    def test_snapshots_not_a_list_dict(self):
        result = self._call({"snapshots": {"a": 1}}, {}, "f")
        assert result is False

    def test_snapshots_not_a_list_int(self):
        result = self._call({"snapshots": 42}, {}, "f")
        assert result is False

    def test_snapshots_not_a_list_none(self):
        result = self._call({"snapshots": None}, {}, "f")
        assert result is False

    # --- success cases ---

    def test_empty_list_succeeds(self):
        doc = {}
        result = self._call({"snapshots": []}, doc, "f")
        assert result is True
        assert doc["snapshots"] == []

    def test_copies_snapshots_into_document(self):
        snaps = [{"id": 1}, {"id": 2}]
        doc = {}
        result = self._call({"snapshots": snaps}, doc, "f")
        assert result is True
        assert doc["snapshots"] is snaps  # same reference

    def test_document_json_existing_keys_preserved(self):
        doc = {"existing": "value"}
        self._call({"snapshots": [{"a": 1}]}, doc, "f")
        assert doc["existing"] == "value"
        assert "snapshots" in doc


# ===================================================================
# Tests for validate_master_snapshot_data
# ===================================================================

class TestValidateMasterSnapshotData:

    def _call(self, master_snapshot_json, document_json, file_location="loc"):
        from processor.connector.populate_json import validate_master_snapshot_data
        return validate_master_snapshot_data(
            master_snapshot_json, document_json, file_location
        )

    # --- early failures ---

    def test_no_connector_users(self):
        doc = _base_document_json()
        result = self._call({}, doc, "f")
        assert result is False

    def test_empty_connector_users(self):
        doc = _base_document_json(connectorUsers=[])
        result = self._call({}, doc, "f")
        assert result is False

    def test_missing_snapshots_key(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        result = self._call({}, doc, "f")
        assert result is False

    def test_snapshots_not_list(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        result = self._call({"snapshots": "bad"}, doc, "f")
        assert result is False

    # --- per-snapshot field validation ---

    def test_snapshot_missing_type(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": [{"connectorUser": "u1", "nodes": []}]}
        result = self._call(master, doc, "f")
        assert result is False

    def test_snapshot_missing_connector_user(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": [{"type": "azure", "nodes": []}]}
        result = self._call(master, doc, "f")
        assert result is False

    def test_connector_user_no_match(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": [{"type": "azure", "connectorUser": "u_unknown", "nodes": []}]}
        result = self._call(master, doc, "f")
        assert result is False

    def test_snapshot_missing_nodes(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": [{"type": "azure", "connectorUser": "u1"}]}
        result = self._call(master, doc, "f")
        assert result is False

    def test_nodes_not_list(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": [{"type": "azure", "connectorUser": "u1", "nodes": "bad"}]}
        result = self._call(master, doc, "f")
        assert result is False

    def test_node_missing_master_snapshot_id(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": [{
            "type": "azure", "connectorUser": "u1",
            "nodes": [{"type": "t", "collection": "c"}]
        }]}
        result = self._call(master, doc, "f")
        assert result is False

    def test_aws_node_missing_arn(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": [{
            "type": "aws", "connectorUser": "u1",
            "nodes": [{"masterSnapshotId": "m1", "collection": "c"}]
        }]}
        result = self._call(master, doc, "f")
        assert result is False

    def test_non_aws_node_missing_type(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": [{
            "type": "azure", "connectorUser": "u1",
            "nodes": [{"masterSnapshotId": "m1", "collection": "c"}]
        }]}
        result = self._call(master, doc, "f")
        assert result is False

    def test_node_missing_collection(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": [{
            "type": "azure", "connectorUser": "u1",
            "nodes": [{"masterSnapshotId": "m1", "type": "t"}]
        }]}
        result = self._call(master, doc, "f")
        assert result is False

    # --- success cases ---

    def test_valid_aws_snapshot(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1", "secretKey": "sk"}])
        master = {"snapshots": [{
            "type": "aws", "connectorUser": "u1",
            "nodes": [{
                "masterSnapshotId": "m1",
                "arn": "arn:aws:...",
                "collection": "ec2"
            }]
        }]}
        result = self._call(master, doc, "f")
        assert result is True
        assert "connector" not in doc
        assert "remoteFile" not in doc
        assert "connectorUsers" not in doc
        assert len(doc["snapshots"]) == 1
        # connector_user fields (minus id) should be merged
        assert doc["snapshots"][0]["secretKey"] == "sk"

    def test_valid_non_aws_snapshot(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1", "tenant": "t1"}])
        master = {"snapshots": [{
            "type": "azure", "connectorUser": "u1",
            "nodes": [{
                "masterSnapshotId": "m1",
                "type": "Microsoft.Compute/virtualMachines",
                "collection": "vms"
            }]
        }]}
        result = self._call(master, doc, "f")
        assert result is True
        assert doc["snapshots"][0]["tenant"] == "t1"

    def test_connector_user_id_not_copied(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1", "extra": "e"}])
        master = {"snapshots": [{
            "type": "azure", "connectorUser": "u1",
            "nodes": [{"masterSnapshotId": "m1", "type": "t", "collection": "c"}]
        }]}
        self._call(master, doc, "f")
        snap = doc["snapshots"][0]
        # "id" from connector_user should NOT be copied
        assert "id" not in snap or snap.get("id") != "u1"

    def test_empty_snapshots_list_succeeds(self):
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": []}
        result = self._call(master, doc, "f")
        assert result is True
        assert doc["snapshots"] == []

    def test_multiple_connector_users_match(self):
        users = [
            {"id": "u1", "key": "k1"},
            {"id": "u2", "key": "k2"},
        ]
        doc = _base_document_json(connectorUsers=users)
        master = {"snapshots": [
            {
                "type": "azure", "connectorUser": "u2",
                "nodes": [{"masterSnapshotId": "m1", "type": "t", "collection": "c"}]
            },
        ]}
        result = self._call(master, doc, "f")
        assert result is True
        assert doc["snapshots"][0]["key"] == "k2"

    def test_document_pops_connector_remote_connectorUsers(self):
        """Verify exactly which keys are popped on success."""
        doc = _base_document_json(connectorUsers=[{"id": "u1"}], extra="keep")
        master = {"snapshots": []}
        self._call(master, doc, "f")
        assert "connector" not in doc
        assert "remoteFile" not in doc
        assert "connectorUsers" not in doc
        assert doc["extra"] == "keep"

    def test_failure_does_not_mutate_document(self):
        """On validation failure, document_json should not be mutated (no pops)."""
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        original_keys = set(doc.keys())
        master = {"snapshots": [{"type": "azure"}]}  # missing connectorUser
        self._call(master, doc, "f")
        assert "connector" in doc
        assert "remoteFile" in doc


# ===================================================================
# Tests for validate_test_data
# ===================================================================

class TestValidateTestData:

    def _call(self, test_json, document_json, file_location="loc"):
        from processor.connector.populate_json import validate_test_data
        return validate_test_data(test_json, document_json, file_location)

    # --- failures ---

    def test_missing_testSet(self):
        assert self._call({}, _base_document_json(), "f") is False

    def test_testSet_not_list(self):
        assert self._call({"testSet": "bad"}, _base_document_json(), "f") is False

    def test_testSet_not_list_int(self):
        assert self._call({"testSet": 99}, _base_document_json(), "f") is False

    def test_missing_testName(self):
        tj = {"testSet": [{"cases": [{"testId": "t1"}]}]}
        assert self._call(tj, _base_document_json(), "f") is False

    def test_missing_cases(self):
        tj = {"testSet": [{"testName": "tn"}]}
        assert self._call(tj, _base_document_json(), "f") is False

    def test_cases_not_list(self):
        tj = {"testSet": [{"testName": "tn", "cases": "bad"}]}
        assert self._call(tj, _base_document_json(), "f") is False

    def test_case_missing_testId(self):
        tj = {"testSet": [{"testName": "tn", "cases": [{"other": "x"}]}]}
        assert self._call(tj, _base_document_json(), "f") is False

    # --- success ---

    def test_valid_single_testset(self):
        doc = _base_document_json()
        tj = {"testSet": [{"testName": "tn", "cases": [{"testId": "t1"}]}]}
        assert self._call(tj, doc, "f") is True
        assert doc["testSet"] == tj["testSet"]
        assert "connector" not in doc
        assert "remoteFile" not in doc

    def test_empty_testSet_succeeds(self):
        doc = _base_document_json()
        assert self._call({"testSet": []}, doc, "f") is True
        assert doc["testSet"] == []

    def test_multiple_testsets(self):
        doc = _base_document_json()
        tj = {"testSet": [
            {"testName": "a", "cases": [{"testId": "1"}]},
            {"testName": "b", "cases": [{"testId": "2"}, {"testId": "3"}]},
        ]}
        assert self._call(tj, doc, "f") is True

    def test_failure_does_not_pop_keys(self):
        doc = _base_document_json()
        self._call({"testSet": "bad"}, doc, "f")
        assert "connector" in doc
        assert "remoteFile" in doc

    def test_second_testset_invalid(self):
        """Validation should fail if the second testset is invalid."""
        doc = _base_document_json()
        tj = {"testSet": [
            {"testName": "ok", "cases": [{"testId": "1"}]},
            {"cases": [{"testId": "2"}]},  # missing testName
        ]}
        assert self._call(tj, doc, "f") is False


# ===================================================================
# Tests for validate_master_test_data
# ===================================================================

class TestValidateMasterTestData:

    def _call(self, master_test_json, document_json, file_location="loc"):
        from processor.connector.populate_json import validate_master_test_data
        return validate_master_test_data(
            master_test_json, document_json, file_location
        )

    # --- failures ---

    def test_missing_testSet(self):
        assert self._call({}, _base_document_json(), "f") is False

    def test_testSet_not_list(self):
        assert self._call({"testSet": {}}, _base_document_json(), "f") is False

    def test_missing_masterTestName(self):
        tj = {"testSet": [{"cases": [{"masterTestId": "m1"}]}]}
        assert self._call(tj, _base_document_json(), "f") is False

    def test_missing_cases(self):
        tj = {"testSet": [{"masterTestName": "mtn"}]}
        assert self._call(tj, _base_document_json(), "f") is False

    def test_cases_not_list(self):
        tj = {"testSet": [{"masterTestName": "mtn", "cases": 123}]}
        assert self._call(tj, _base_document_json(), "f") is False

    def test_case_missing_masterTestId(self):
        tj = {"testSet": [{"masterTestName": "mtn", "cases": [{"x": 1}]}]}
        assert self._call(tj, _base_document_json(), "f") is False

    # --- success ---

    def test_valid_master_test(self):
        doc = _base_document_json()
        tj = {"testSet": [{"masterTestName": "mtn", "cases": [{"masterTestId": "m1"}]}]}
        assert self._call(tj, doc, "f") is True
        assert doc["testSet"] == tj["testSet"]
        assert "connector" not in doc
        assert "remoteFile" not in doc

    def test_empty_testSet_succeeds(self):
        doc = _base_document_json()
        assert self._call({"testSet": []}, doc, "f") is True

    def test_failure_preserves_document(self):
        doc = _base_document_json()
        self._call({}, doc, "f")
        assert "connector" in doc

    def test_second_case_invalid(self):
        doc = _base_document_json()
        tj = {"testSet": [
            {"masterTestName": "a", "cases": [{"masterTestId": "1"}, {"bad": "2"}]},
        ]}
        assert self._call(tj, doc, "f") is False


# ===================================================================
# Tests for validate_json_data (cli_populate_json)
# ===================================================================

class TestValidateJsonData:

    def _call(self, json_data, filetype):
        from processor.helper.utils.cli_populate_json import validate_json_data
        return validate_json_data(json_data, filetype)

    # --- snapshot ---

    def test_snapshot_valid(self):
        data = {"fileType": "snapshot", "snapshots": [{"id": 1}]}
        assert self._call(data, "snapshot") is True

    def test_snapshot_missing_snapshots(self):
        data = {"fileType": "snapshot"}
        assert self._call(data, "snapshot") is False

    def test_snapshot_snapshots_not_list(self):
        data = {"fileType": "snapshot", "snapshots": "bad"}
        assert self._call(data, "snapshot") is False

    def test_snapshot_empty_list(self):
        """Empty list is falsy, so validate_json_data returns a falsy value."""
        data = {"fileType": "snapshot", "snapshots": []}
        assert not self._call(data, "snapshot")

    # --- masterSnapshot ---

    def test_master_snapshot_valid(self):
        data = {"fileType": "masterSnapshot", "snapshots": [{"id": 1}]}
        assert self._call(data, "masterSnapshot") is True

    def test_master_snapshot_missing_snapshots(self):
        data = {"fileType": "masterSnapshot"}
        assert self._call(data, "masterSnapshot") is False

    def test_master_snapshot_snapshots_not_list(self):
        data = {"fileType": "masterSnapshot", "snapshots": 42}
        assert self._call(data, "masterSnapshot") is False

    # --- test ---

    def test_test_valid(self):
        data = {
            "fileType": "test",
            "snapshot": "snap_ref",
            "testSet": [{"testId": "t1"}],
        }
        assert self._call(data, "test") is True

    def test_test_missing_snapshot_field(self):
        data = {"fileType": "test", "testSet": [{"testId": "t1"}]}
        assert self._call(data, "test") is False

    def test_test_missing_testSet(self):
        data = {"fileType": "test", "snapshot": "s"}
        assert self._call(data, "test") is False

    def test_test_testSet_not_list(self):
        data = {"fileType": "test", "snapshot": "s", "testSet": "bad"}
        assert self._call(data, "test") is False

    # --- mastertest ---

    def test_mastertest_valid(self):
        data = {
            "fileType": "mastertest",
            "masterSnapshot": "ms_ref",
            "testSet": [{"masterTestId": "m1"}],
        }
        assert self._call(data, "mastertest") is True

    def test_mastertest_missing_masterSnapshot(self):
        data = {"fileType": "mastertest", "testSet": [{}]}
        assert self._call(data, "mastertest") is False

    def test_mastertest_missing_testSet(self):
        data = {"fileType": "mastertest", "masterSnapshot": "ms"}
        assert self._call(data, "mastertest") is False

    def test_mastertest_testSet_not_list(self):
        data = {"fileType": "mastertest", "masterSnapshot": "ms", "testSet": {}}
        assert not self._call(data, "mastertest")

    # --- structure ---

    def test_structure_valid(self):
        data = {"fileType": "structure", "some": "data"}
        assert self._call(data, "structure") is True

    def test_structure_empty_data_still_truthy_dict(self):
        """A dict with fileType is truthy, so structure should still pass."""
        data = {"fileType": "structure"}
        assert self._call(data, "structure") is True

    def test_structure_exception_still_returns_true(self):
        """For 'structure' type, exceptions should still return True."""
        data = {}  # missing 'fileType' -> KeyError
        assert self._call(data, "structure") is True

    # --- notifications ---

    def test_notifications_valid(self):
        data = {"fileType": "notifications", "rules": []}
        assert self._call(data, "notifications") is True

    # --- fileType mismatch ---

    def test_filetype_mismatch(self):
        """If fileType doesn't match, for structure/notifications it might
        still pass the truthy check, but for others it should eventually
        fail when accessing missing keys."""
        data = {"fileType": "snapshot"}
        # filetype arg says mastertest but data says snapshot
        assert self._call(data, "mastertest") is False

    # --- exception path ---

    def test_exception_returns_false_for_non_structure(self):
        data = {}  # KeyError on 'fileType'
        assert self._call(data, "snapshot") is False

    def test_exception_returns_true_for_structure(self):
        data = {}
        assert self._call(data, "structure") is True


# ===================================================================
# Tests for json_record (cli_populate_json)
# ===================================================================

class TestJsonRecord:

    @patch("processor.helper.utils.cli_populate_json.config_value")
    def _call(self, container, filetype, filename, json_data, mock_config):
        mock_config.return_value = "test_collection"
        from processor.helper.utils.cli_populate_json import json_record
        return json_record(container, filetype, filename, json_data)

    def test_basic_structure(self):
        record = self._call("cont", "snapshot", "/path/to/myfile.json", {"a": 1})
        assert record["container"] == "cont"
        assert record["type"] == "snapshot"
        assert record["name"] == "myfile"
        assert record["json"] == {"a": 1}
        assert "checksum" in record
        assert "timestamp" in record
        assert "collection" in record

    def test_removes_schema(self):
        data = {"$schema": "http://...", "key": "val"}
        record = self._call("c", "test", "/f.json", data)
        assert "$schema" not in record["json"]
        assert record["json"]["key"] == "val"

    def test_no_json_data_defaults_empty_dict(self):
        record = self._call("c", "structure", "/f.json", None)
        assert record["json"] == {}

    def test_name_parsed_from_filename(self):
        record = self._call("c", "test", "/a/b/c/my_test.json", {})
        assert record["name"] == "my_test"

    def test_checksum_is_md5(self):
        record = self._call("c", "test", "/f.json", {})
        expected = hashlib.md5("{}".encode('utf-8')).hexdigest()
        assert record["checksum"] == expected

    def test_timestamp_is_int(self):
        record = self._call("c", "test", "/f.json", {})
        assert isinstance(record["timestamp"], int)


# ===================================================================
# Tests for add_new_container (cli_populate_json)
# ===================================================================

class TestAddNewContainer:

    @patch("processor.helper.utils.cli_populate_json.update_one_document")
    @patch("processor.helper.utils.cli_populate_json.get_documents")
    def test_new_container_fields_contract(self, mock_get_docs, mock_update):
        """Verify the PascalCase field contract: 'Snapshots' and 'Tests'."""
        container_struct = {
            "json": {"containers": []},
            "collection": "structures",
        }
        mock_get_docs.return_value = [container_struct]

        from processor.helper.utils.cli_populate_json import add_new_container
        add_new_container("my_container", "testdb")

        updated = mock_update.call_args[0][0]
        new_cont = updated["json"]["containers"][0]

        assert new_cont["name"] == "my_container"
        assert new_cont["containerId"] == 1
        assert new_cont["status"] == "active"
        # PascalCase contract
        assert "Snapshots" in new_cont
        assert "Tests" in new_cont
        assert "masterSnapshots" in new_cont
        assert "masterTests" in new_cont
        assert "others" in new_cont
        # All are empty lists
        for key in ("Snapshots", "Tests", "masterSnapshots", "masterTests", "others"):
            assert new_cont[key] == []

    @patch("processor.helper.utils.cli_populate_json.update_one_document")
    @patch("processor.helper.utils.cli_populate_json.get_documents")
    def test_container_id_increments(self, mock_get_docs, mock_update):
        existing_container = {
            "containerId": 5,
            "status": "active",
            "name": "existing",
            "masterSnapshots": [],
            "Snapshots": [],
            "masterTests": [],
            "Tests": [],
            "others": [],
        }
        container_struct = {
            "json": {"containers": [existing_container]},
            "collection": "structures",
        }
        mock_get_docs.return_value = [container_struct]

        from processor.helper.utils.cli_populate_json import add_new_container
        add_new_container("new_one", "testdb")

        updated = mock_update.call_args[0][0]
        new_cont = updated["json"]["containers"][-1]
        assert new_cont["containerId"] == 6

    @patch("processor.helper.utils.cli_populate_json.update_one_document")
    @patch("processor.helper.utils.cli_populate_json.get_documents")
    def test_duplicate_container_skipped(self, mock_get_docs, mock_update):
        existing = {
            "containerId": 1, "name": "dup",
            "status": "active", "masterSnapshots": [],
            "Snapshots": [], "masterTests": [], "Tests": [], "others": [],
        }
        container_struct = {
            "json": {"containers": [existing]},
            "collection": "structures",
        }
        mock_get_docs.return_value = [container_struct]

        from processor.helper.utils.cli_populate_json import add_new_container
        add_new_container("dup", "testdb")

        mock_update.assert_not_called()


# ===================================================================
# Edge-case and integration-style tests
# ===================================================================

class TestEdgeCases:

    def test_validate_snapshot_data_with_extra_fields(self):
        """Extra fields in snapshot_json should be ignored."""
        from processor.connector.populate_json import validate_snapshot_data
        doc = {}
        result = validate_snapshot_data(
            {"snapshots": [{"x": 1}], "extra": True}, doc, "f"
        )
        assert result is True
        assert doc["snapshots"] == [{"x": 1}]

    def test_validate_test_data_testId_can_be_int(self):
        """testId can be any type as long as it exists."""
        from processor.connector.populate_json import validate_test_data
        doc = _base_document_json()
        tj = {"testSet": [{"testName": "n", "cases": [{"testId": 123}]}]}
        assert validate_test_data(tj, doc, "f") is True

    def test_validate_master_test_data_masterTestId_can_be_int(self):
        from processor.connector.populate_json import validate_master_test_data
        doc = _base_document_json()
        tj = {"testSet": [{"masterTestName": "n", "cases": [{"masterTestId": 999}]}]}
        assert validate_master_test_data(tj, doc, "f") is True

    def test_master_snapshot_deep_copy_isolation(self):
        """Snapshots stored in document should be deep-copied (independent)."""
        from processor.connector.populate_json import validate_master_snapshot_data
        doc = _base_document_json(connectorUsers=[{"id": "u1", "k": "v"}])
        node = {"masterSnapshotId": "m1", "type": "t", "collection": "c"}
        snapshot = {"type": "azure", "connectorUser": "u1", "nodes": [node]}
        master = {"snapshots": [snapshot]}
        validate_master_snapshot_data(master, doc, "f")
        # Modify the original snapshot; document copy should be unaffected
        snapshot["type"] = "MODIFIED"
        assert doc["snapshots"][0]["type"] == "azure"

    def test_validate_test_data_first_case_ok_second_bad(self):
        """If the second case in a testset lacks testId, validation fails."""
        from processor.connector.populate_json import validate_test_data
        doc = _base_document_json()
        tj = {"testSet": [{
            "testName": "n",
            "cases": [{"testId": "ok"}, {"noId": "bad"}],
        }]}
        assert validate_test_data(tj, doc, "f") is False

    def test_validate_master_snapshot_multiple_nodes(self):
        """Multiple valid nodes should all pass."""
        from processor.connector.populate_json import validate_master_snapshot_data
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": [{
            "type": "aws", "connectorUser": "u1",
            "nodes": [
                {"masterSnapshotId": "m1", "arn": "a1", "collection": "c1"},
                {"masterSnapshotId": "m2", "arn": "a2", "collection": "c2"},
            ]
        }]}
        assert validate_master_snapshot_data(master, doc, "f") is True
        assert len(doc["snapshots"]) == 1
        assert len(doc["snapshots"][0]["nodes"]) == 2

    def test_validate_master_snapshot_second_node_invalid(self):
        """Second node missing collection should fail."""
        from processor.connector.populate_json import validate_master_snapshot_data
        doc = _base_document_json(connectorUsers=[{"id": "u1"}])
        master = {"snapshots": [{
            "type": "aws", "connectorUser": "u1",
            "nodes": [
                {"masterSnapshotId": "m1", "arn": "a1", "collection": "c1"},
                {"masterSnapshotId": "m2", "arn": "a2"},  # missing collection
            ]
        }]}
        assert validate_master_snapshot_data(master, doc, "f") is False

    def test_validate_master_snapshot_multiple_snapshots(self):
        """Multiple snapshots with different connector users."""
        from processor.connector.populate_json import validate_master_snapshot_data
        doc = _base_document_json(connectorUsers=[
            {"id": "u1", "region": "us"},
            {"id": "u2", "region": "eu"},
        ])
        master = {"snapshots": [
            {
                "type": "aws", "connectorUser": "u1",
                "nodes": [{"masterSnapshotId": "m1", "arn": "a", "collection": "c"}]
            },
            {
                "type": "azure", "connectorUser": "u2",
                "nodes": [{"masterSnapshotId": "m2", "type": "t", "collection": "c"}]
            },
        ]}
        assert validate_master_snapshot_data(master, doc, "f") is True
        assert len(doc["snapshots"]) == 2
        assert doc["snapshots"][0]["region"] == "us"
        assert doc["snapshots"][1]["region"] == "eu"
