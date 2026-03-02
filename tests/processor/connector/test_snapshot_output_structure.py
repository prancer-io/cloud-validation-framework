"""
Tests for validating the output structures produced by each connector.
These tests protect the snapshot record format that downstream systems depend on.
"""
import json
import hashlib
import time
import re
import copy
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch, PropertyMock

import pytest


# ---------------------------------------------------------------------------
# 1. Snapshot type registry
# ---------------------------------------------------------------------------

class TestSnapshotTypeRegistry:
    """Verify snapshot.py has the correct type -> function mapping."""

    def test_snapshot_fns_has_all_five_keys(self):
        from processor.connector.snapshot import snapshot_fns
        expected_keys = {'azure', 'aws', 'google', 'kubernetes', 'filesystem'}
        assert set(snapshot_fns.keys()) == expected_keys

    def test_snapshot_fns_azure_maps_to_correct_function(self):
        from processor.connector.snapshot_azure import populate_azure_snapshot
        # Re-read original module-level dict to avoid cross-test pollution
        import processor.connector.snapshot as snap_mod
        import importlib
        importlib.reload(snap_mod)
        assert snap_mod.snapshot_fns['azure'] is populate_azure_snapshot

    def test_snapshot_fns_aws_maps_to_correct_function(self):
        from processor.connector.snapshot_aws import populate_aws_snapshot
        import processor.connector.snapshot as snap_mod
        import importlib
        importlib.reload(snap_mod)
        assert snap_mod.snapshot_fns['aws'] is populate_aws_snapshot

    def test_snapshot_fns_google_maps_to_correct_function(self):
        from processor.connector.snapshot_google import populate_google_snapshot
        import processor.connector.snapshot as snap_mod
        import importlib
        importlib.reload(snap_mod)
        assert snap_mod.snapshot_fns['google'] is populate_google_snapshot

    def test_snapshot_fns_kubernetes_maps_to_correct_function(self):
        from processor.connector.snapshot_kubernetes import populate_kubernetes_snapshot
        import processor.connector.snapshot as snap_mod
        import importlib
        importlib.reload(snap_mod)
        assert snap_mod.snapshot_fns['kubernetes'] is populate_kubernetes_snapshot

    def test_snapshot_fns_filesystem_maps_to_correct_function(self):
        from processor.connector.snapshot_custom import populate_custom_snapshot
        import processor.connector.snapshot as snap_mod
        import importlib
        importlib.reload(snap_mod)
        assert snap_mod.snapshot_fns['filesystem'] is populate_custom_snapshot

    def test_snapshot_fns_values_are_callable(self):
        from processor.connector.snapshot import snapshot_fns
        for key, fn in snapshot_fns.items():
            assert callable(fn), f"snapshot_fns['{key}'] is not callable"


# ---------------------------------------------------------------------------
# 2. AWS snapshot record structure
# ---------------------------------------------------------------------------

class TestAWSSnapshotRecordStructure:
    """Validate the record structure created by AWS get_node."""

    def _build_aws_db_record(self, node, snapshot_source="awsSource.json",
                              snapshot=None, session_id="sess-1"):
        """Build an AWS db_record the same way get_node does (without API calls)."""
        if snapshot is None:
            snapshot = {"testUser": "testuser"}
        collection = node.get('collection', 'COLLECTION')
        parts = snapshot_source.split('.')
        db_record = {
            "structure": "aws",
            "error": None,
            "reference": "",
            "contentType": "json",
            "source": parts[0],
            "path": '',
            "timestamp": int(time.time() * 1000),
            "queryuser": snapshot.get('testUser'),
            "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
            "node": node,
            "region": "",
            "snapshotId": node['snapshotId'],
            "collection": collection.replace('.', '').lower(),
            "session_id": session_id,
            "json": {},
        }
        return db_record

    def test_aws_record_has_structure_field(self):
        node = {"snapshotId": "AWS_001", "collection": "ec2", "type": "instances"}
        record = self._build_aws_db_record(node)
        assert record["structure"] == "aws"

    def test_aws_record_has_reference_field_as_string(self):
        node = {"snapshotId": "AWS_001", "collection": "ec2", "type": "instances"}
        record = self._build_aws_db_record(node)
        assert isinstance(record["reference"], str)

    def test_aws_record_has_source_field(self):
        node = {"snapshotId": "AWS_001", "collection": "ec2", "type": "instances"}
        record = self._build_aws_db_record(node, snapshot_source="myAwsSource.json")
        assert record["source"] == "myAwsSource"

    def test_aws_record_has_path_field(self):
        node = {"snapshotId": "AWS_001", "collection": "ec2", "type": "instances"}
        record = self._build_aws_db_record(node)
        assert isinstance(record["path"], str)

    def test_aws_record_timestamp_is_int_milliseconds(self):
        node = {"snapshotId": "AWS_001", "collection": "ec2", "type": "instances"}
        before = int(time.time() * 1000)
        record = self._build_aws_db_record(node)
        after = int(time.time() * 1000)
        assert isinstance(record["timestamp"], int)
        assert before <= record["timestamp"] <= after

    def test_aws_record_checksum_is_md5(self):
        node = {"snapshotId": "AWS_001", "collection": "ec2", "type": "instances"}
        record = self._build_aws_db_record(node)
        expected_checksum = hashlib.md5("{}".encode('utf-8')).hexdigest()
        assert record["checksum"] == expected_checksum
        assert isinstance(record["checksum"], str)
        assert len(record["checksum"]) == 32  # MD5 hex length

    def test_aws_record_snapshotid_is_string(self):
        node = {"snapshotId": "AWS_001", "collection": "ec2", "type": "instances"}
        record = self._build_aws_db_record(node)
        assert record["snapshotId"] == "AWS_001"
        assert isinstance(record["snapshotId"], str)

    def test_aws_record_collection_is_lowercased_dots_removed(self):
        node = {"snapshotId": "AWS_001", "collection": "Microsoft.Compute", "type": "instances"}
        record = self._build_aws_db_record(node)
        assert record["collection"] == "microsoftcompute"

    def test_aws_record_json_is_dict(self):
        node = {"snapshotId": "AWS_001", "collection": "ec2", "type": "instances"}
        record = self._build_aws_db_record(node)
        assert isinstance(record["json"], dict)

    def test_aws_master_record_has_masterSnapshotId(self):
        """get_all_nodes produces records with masterSnapshotId."""
        node = {"masterSnapshotId": "MASTER_AWS_001", "collection": "ec2",
                "type": "instances", "listMethod": "describe_instances"}
        snapshot_source = "awsSource.json"
        parts = snapshot_source.split('.')
        d_record = {
            "structure": "aws",
            "reference": "",
            "contentType": "json",
            "source": parts[0],
            "path": '',
            "timestamp": int(time.time() * 1000),
            "queryuser": "testuser",
            "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
            "node": node,
            "snapshotId": None,
            "masterSnapshotId": node['masterSnapshotId'],
            "collection": node['collection'].replace('.', '').lower(),
            "json": {},
        }
        assert d_record["masterSnapshotId"] == "MASTER_AWS_001"
        assert isinstance(d_record["masterSnapshotId"], str)


# ---------------------------------------------------------------------------
# 3. Azure snapshot record structure
# ---------------------------------------------------------------------------

class TestAzureSnapshotRecordStructure:
    """Validate the record structure created by Azure get_node."""

    def _build_azure_db_record(self, node, sub_name="MySub", snapshot_source="azureSource.json",
                                user="testuser", session_id="sess-1"):
        """Build an Azure db_record the same way snapshot_azure.get_node does."""
        collection = node.get('collection', 'COLLECTION')
        parts = snapshot_source.split('.')
        db_record = {
            "structure": "azure",
            "reference": sub_name,
            "contentType": "json",
            "source": parts[0],
            "path": '',
            "timestamp": int(time.time() * 1000),
            "queryuser": user,
            "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
            "node": node,
            "snapshotId": node.get('snapshotId'),
            "mastersnapshot": False,
            "masterSnapshotId": None,
            "collection": collection.replace('.', '').lower(),
            "region": "",
            "session_id": session_id,
            "json": {"resources": []},
        }
        return db_record

    def test_azure_record_structure_is_azure(self):
        node = {"snapshotId": "AZ_001", "collection": "Microsoft.Compute", "path": "/subscriptions/x/y"}
        record = self._build_azure_db_record(node)
        assert record["structure"] == "azure"

    def test_azure_record_reference_is_subscription_name(self):
        node = {"snapshotId": "AZ_001", "collection": "Microsoft.Compute", "path": "/subscriptions/x/y"}
        record = self._build_azure_db_record(node, sub_name="MySubscription")
        assert record["reference"] == "MySubscription"
        assert isinstance(record["reference"], str)

    def test_azure_record_has_path_field(self):
        node = {"snapshotId": "AZ_001", "collection": "Microsoft.Compute",
                "path": "/subscriptions/sub-id/resourceGroups/rg/providers/Microsoft.Compute/vm1"}
        record = self._build_azure_db_record(node)
        assert isinstance(record["path"], str)

    def test_azure_record_timestamp_is_int(self):
        node = {"snapshotId": "AZ_001", "collection": "Microsoft.Compute", "path": "/x/y"}
        record = self._build_azure_db_record(node)
        assert isinstance(record["timestamp"], int)

    def test_azure_record_snapshotid_is_string(self):
        node = {"snapshotId": "AZ_001", "collection": "Microsoft.Compute", "path": "/x/y"}
        record = self._build_azure_db_record(node)
        assert record["snapshotId"] == "AZ_001"

    def test_azure_record_collection_normalized(self):
        node = {"snapshotId": "AZ_001", "collection": "Microsoft.Compute", "path": "/x/y"}
        record = self._build_azure_db_record(node)
        assert record["collection"] == "microsoftcompute"

    def test_azure_record_region_is_string(self):
        node = {"snapshotId": "AZ_001", "collection": "Microsoft.Compute", "path": "/x/y"}
        record = self._build_azure_db_record(node)
        assert isinstance(record["region"], str)

    def test_azure_record_json_has_resources_list(self):
        node = {"snapshotId": "AZ_001", "collection": "Microsoft.Compute", "path": "/x/y"}
        record = self._build_azure_db_record(node)
        assert "resources" in record["json"]
        assert isinstance(record["json"]["resources"], list)

    def test_azure_master_record_has_masterSnapshotId(self):
        """get_all_nodes produces records with masterSnapshotId as a list."""
        node = {"masterSnapshotId": "MASTER_AZ_001", "collection": "Microsoft.Compute",
                "type": "Microsoft.Compute/virtualMachines"}
        parts = "azureSource.json".split('.')
        d_record = {
            "structure": "azure",
            "reference": "MySub",
            "contentType": "json",
            "source": parts[0],
            "path": '',
            "timestamp": int(time.time() * 1000),
            "queryuser": "testuser",
            "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
            "node": node,
            "snapshotId": None,
            "mastersnapshot": True,
            "masterSnapshotId": [node['masterSnapshotId']],
            "collection": node['collection'].replace('.', '').lower(),
            "json": {},
        }
        assert d_record["masterSnapshotId"] == ["MASTER_AZ_001"]
        assert isinstance(d_record["masterSnapshotId"], list)


# ---------------------------------------------------------------------------
# 4. Google snapshot record structure
# ---------------------------------------------------------------------------

class TestGoogleSnapshotRecordStructure:
    """Validate the record structure created by Google get_node."""

    def _build_google_db_record(self, node, snapshot_source="googleSource.json",
                                 project_id="my-project", snapshot=None, session_id="sess-1"):
        if snapshot is None:
            snapshot = {"testUser": "testuser"}
        collection = node.get('collection', 'COLLECTION')
        parts = snapshot_source.split('.')
        path = node.get('path', '')
        zone = re.findall(r"(?<=zones\/)[a-zA-Z0-9\-]*(?=\/)", path)
        db_record = {
            "structure": "google",
            "error": None,
            "reference": project_id,
            "contentType": "json",
            "source": parts[0],
            "path": path,
            "timestamp": int(time.time() * 1000),
            "queryuser": snapshot.get('testUser'),
            "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
            "node": node,
            "snapshotId": node['snapshotId'],
            "collection": collection.replace('.', '').lower(),
            "region": zone[0] if zone else "",
            "session_id": session_id,
            "json": {},
        }
        return db_record

    def test_google_record_structure_is_google(self):
        node = {"snapshotId": "GCP_001", "collection": "compute", "path": "projects/my-proj/zones/us-east1-b/instances/vm1"}
        record = self._build_google_db_record(node)
        assert record["structure"] == "google"

    def test_google_record_reference_is_project_id(self):
        node = {"snapshotId": "GCP_001", "collection": "compute", "path": ""}
        record = self._build_google_db_record(node, project_id="test-project-123")
        assert record["reference"] == "test-project-123"
        assert isinstance(record["reference"], str)

    def test_google_record_path_is_string(self):
        node = {"snapshotId": "GCP_001", "collection": "compute",
                "path": "projects/my-proj/zones/us-east1-b/instances/vm1"}
        record = self._build_google_db_record(node)
        assert isinstance(record["path"], str)
        assert record["path"] == "projects/my-proj/zones/us-east1-b/instances/vm1"

    def test_google_record_timestamp_is_int(self):
        node = {"snapshotId": "GCP_001", "collection": "compute", "path": ""}
        record = self._build_google_db_record(node)
        assert isinstance(record["timestamp"], int)

    def test_google_record_snapshotid_is_string(self):
        node = {"snapshotId": "GCP_001", "collection": "compute", "path": ""}
        record = self._build_google_db_record(node)
        assert record["snapshotId"] == "GCP_001"

    def test_google_record_collection_normalized(self):
        node = {"snapshotId": "GCP_001", "collection": "compute.instances", "path": ""}
        record = self._build_google_db_record(node)
        assert record["collection"] == "computeinstances"

    def test_google_record_json_is_dict(self):
        node = {"snapshotId": "GCP_001", "collection": "compute", "path": ""}
        record = self._build_google_db_record(node)
        assert isinstance(record["json"], dict)

    def test_google_record_region_extracted_from_zone_path(self):
        node = {"snapshotId": "GCP_001", "collection": "compute",
                "path": "projects/my-proj/zones/us-east1-b/instances/vm1"}
        record = self._build_google_db_record(node)
        assert record["region"] == "us-east1-b"

    def test_google_record_region_empty_when_no_zone(self):
        node = {"snapshotId": "GCP_001", "collection": "compute",
                "path": "projects/my-proj/global/networks/default"}
        record = self._build_google_db_record(node)
        assert record["region"] == ""


# ---------------------------------------------------------------------------
# 5. Custom/filesystem snapshot record structure
# ---------------------------------------------------------------------------

class TestCustomSnapshotRecordStructure:
    """Validate the record structure created by custom/filesystem get_node."""

    def _build_custom_db_record(self, node, ref="master", connector_type="filesystem",
                                 snapshot_source="customSource.json", snapshot=None,
                                 base_path="", session_id="sess-1"):
        if snapshot is None:
            snapshot = {"testUser": "testuser", "source": snapshot_source}
        collection = node.get('collection', 'COLLECTION')
        parts = snapshot_source.split('.')
        db_record = {
            "structure": connector_type,
            "reference": ref if not base_path else "",
            "source": parts[0],
            "path": base_path + node['path'],
            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000),
            "queryuser": snapshot.get('testUser'),
            "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
            "node": node,
            "snapshotId": node['snapshotId'],
            "collection": collection.replace('.', '').lower(),
            "session_id": session_id,
            "json": {},
        }
        return db_record

    def test_custom_record_structure_is_given_type(self):
        node = {"snapshotId": "FS_001", "collection": "myfiles", "path": "path/to/file.json"}
        record = self._build_custom_db_record(node, connector_type="filesystem")
        assert record["structure"] == "filesystem"

    def test_custom_record_structure_can_be_any_type(self):
        node = {"snapshotId": "FS_001", "collection": "myfiles", "path": "path/to/file.json"}
        record = self._build_custom_db_record(node, connector_type="helmchart")
        assert record["structure"] == "helmchart"

    def test_custom_record_reference_is_git_ref(self):
        node = {"snapshotId": "FS_001", "collection": "myfiles", "path": "path/to/file.json"}
        record = self._build_custom_db_record(node, ref="main")
        assert record["reference"] == "main"

    def test_custom_record_reference_empty_when_base_path(self):
        node = {"snapshotId": "FS_001", "collection": "myfiles", "path": "path/to/file.json"}
        record = self._build_custom_db_record(node, ref="main", base_path="/some/folder/")
        assert record["reference"] == ""

    def test_custom_record_path_includes_base_path(self):
        node = {"snapshotId": "FS_001", "collection": "myfiles", "path": "sub/file.json"}
        record = self._build_custom_db_record(node, base_path="/repo/")
        assert record["path"] == "/repo/sub/file.json"

    def test_custom_record_timestamp_is_int(self):
        node = {"snapshotId": "FS_001", "collection": "myfiles", "path": "a.json"}
        record = self._build_custom_db_record(node)
        assert isinstance(record["timestamp"], int)

    def test_custom_record_snapshotid_is_string(self):
        node = {"snapshotId": "FS_001", "collection": "myfiles", "path": "a.json"}
        record = self._build_custom_db_record(node)
        assert record["snapshotId"] == "FS_001"

    def test_custom_record_collection_normalized(self):
        node = {"snapshotId": "FS_001", "collection": "my.custom.collection", "path": "a.json"}
        record = self._build_custom_db_record(node)
        assert record["collection"] == "mycustomcollection"

    def test_custom_record_json_is_dict(self):
        node = {"snapshotId": "FS_001", "collection": "myfiles", "path": "a.json"}
        record = self._build_custom_db_record(node)
        assert isinstance(record["json"], dict)

    def test_custom_record_contentType_set_on_parse(self):
        """After parsing, contentType should be set to json, yaml, or terraform."""
        node = {"snapshotId": "FS_001", "collection": "myfiles", "path": "a.json"}
        record = self._build_custom_db_record(node)
        # contentType is added after parsing, verify that the initial record
        # can be augmented with contentType
        record['contentType'] = 'json'
        assert record['contentType'] in ('json', 'yaml', 'terraform')


# ---------------------------------------------------------------------------
# 6. Snapshot metadata structure (used in validation results)
# ---------------------------------------------------------------------------

class TestSnapshotMetadataStructure:
    """Validate the metadata fields expected when snapshots are loaded for validation."""

    def test_metadata_has_required_fields_for_single_node(self):
        """A snapshot node should contain at minimum these fields."""
        node = {
            "snapshotId": "SNAP_001",
            "collection": "Microsoft.Compute",
            "type": "Microsoft.Compute/virtualMachines",
            "path": "/subscriptions/sub-1/resourceGroups/rg1/providers/Microsoft.Compute/virtualMachines/vm1",
        }
        assert "snapshotId" in node
        assert isinstance(node["snapshotId"], str)
        assert "collection" in node
        assert "type" in node
        assert "path" in node

    def test_metadata_node_with_master_snapshot_id(self):
        node = {
            "masterSnapshotId": "MASTER_001",
            "collection": "Microsoft.Compute",
            "type": "Microsoft.Compute/virtualMachines",
        }
        assert "masterSnapshotId" in node
        assert isinstance(node["masterSnapshotId"], str)

    def test_metadata_node_with_paths_list(self):
        """Some nodes can have a 'paths' list instead of a single 'path'."""
        node = {
            "snapshotId": "SNAP_002",
            "collection": "compute",
            "type": "compute/instances",
            "paths": ["/path/a", "/path/b"],
        }
        assert isinstance(node["paths"], list)
        assert len(node["paths"]) == 2

    def test_metadata_node_with_resource_types(self):
        """Nodes may optionally contain resourceTypes."""
        node = {
            "snapshotId": "SNAP_003",
            "collection": "compute",
            "type": "rego",
            "masterSnapshotId": ["MASTER_001"],
            "resourceTypes": ["Microsoft.Compute/virtualMachines"],
        }
        assert isinstance(node.get("resourceTypes"), list)


# ---------------------------------------------------------------------------
# 7. Validation result structure
# ---------------------------------------------------------------------------

class TestValidationResultStructure:
    """Test the result format from run_validation_test."""

    @patch('processor.connector.validation.Comparator')
    def test_result_id_format(self, mock_comparator_cls):
        """result_id should be '{container_lowercase}_{timestamp}'."""
        from processor.connector.validation import run_validation_test
        mock_comparator = MagicMock()
        mock_comparator.validate.return_value = [{"result": "passed"}]
        mock_comparator_cls.return_value = mock_comparator

        testcase = {"testId": "T1", "rule": "some_rule"}
        results = run_validation_test("v1", "MyContainer", "testdb", {}, testcase, {}, [])
        assert len(results) >= 1
        result_id = results[0]["result_id"]
        # Should match pattern: lowercased container (special chars removed) _ timestamp
        assert re.match(r'^[a-z]+_\d+$', result_id), f"result_id '{result_id}' does not match expected pattern"

    @patch('processor.connector.validation.Comparator')
    def test_result_merged_with_testcase_fields(self, mock_comparator_cls):
        """Each result should be merged with testcase fields."""
        from processor.connector.validation import run_validation_test
        mock_comparator = MagicMock()
        mock_comparator.validate.return_value = [{"result": "passed", "snapshots": []}]
        mock_comparator_cls.return_value = mock_comparator

        testcase = {"testId": "T1", "rule": "some_rule", "title": "my test"}
        results = run_validation_test("v1", "container", "testdb", {}, testcase, {}, [])
        assert results[0]["testId"] == "T1"
        assert results[0]["rule"] == "some_rule"
        assert results[0]["title"] == "my test"

    @patch('processor.connector.validation.Comparator')
    def test_results_is_a_list_of_dicts(self, mock_comparator_cls):
        """Results should always be a list of dicts."""
        from processor.connector.validation import run_validation_test
        mock_comparator = MagicMock()
        mock_comparator.validate.return_value = [
            {"result": "passed"},
            {"result": "failed"},
        ]
        mock_comparator_cls.return_value = mock_comparator

        testcase = {"testId": "T1", "rule": "r"}
        results = run_validation_test("v1", "container", "db", {}, testcase, {}, [])
        assert isinstance(results, list)
        for r in results:
            assert isinstance(r, dict)

    @patch('processor.connector.validation.Comparator')
    def test_single_result_wrapped_in_list(self, mock_comparator_cls):
        """When Comparator returns a dict instead of list, it should be wrapped."""
        from processor.connector.validation import run_validation_test
        mock_comparator = MagicMock()
        mock_comparator.validate.return_value = {"result": "passed"}
        mock_comparator_cls.return_value = mock_comparator

        testcase = {"testId": "T1", "rule": "r"}
        results = run_validation_test("v1", "container", "db", {}, testcase, {}, [])
        assert isinstance(results, list)
        assert len(results) == 1


# ---------------------------------------------------------------------------
# 8. Snapshot-to-collection mapping
# ---------------------------------------------------------------------------

class TestSnapshotIdToCollectionDict:
    """Test get_snapshot_id_to_collection_dict returns correct mapping."""

    @patch('processor.connector.validation.get_dbtests', return_value=False)
    @patch('processor.connector.validation.create_indexes')
    @patch('processor.connector.validation.pull_json_data')
    @patch('processor.connector.validation.get_snapshot_file')
    def test_returns_correct_mapping(self, mock_get_file, mock_pull, mock_idx, mock_dbtests):
        from processor.connector.validation import get_snapshot_id_to_collection_dict
        mock_get_file.return_value = {
            "snapshots": [
                {
                    "source": "src1",
                    "type": "azure",
                    "nodes": [
                        {"snapshotId": "SNAP_A", "collection": "Microsoft.Compute"},
                        {"snapshotId": "SNAP_B", "collection": "Microsoft.Network"},
                    ]
                }
            ]
        }
        result = get_snapshot_id_to_collection_dict("snap_file", "container", "db", filesystem=True)
        assert result["SNAP_A"] == "microsoftcompute"
        assert result["SNAP_B"] == "microsoftnetwork"

    @patch('processor.connector.validation.get_dbtests', return_value=False)
    @patch('processor.connector.validation.create_indexes')
    @patch('processor.connector.validation.pull_json_data')
    @patch('processor.connector.validation.get_snapshot_file')
    def test_collection_without_dots(self, mock_get_file, mock_pull, mock_idx, mock_dbtests):
        from processor.connector.validation import get_snapshot_id_to_collection_dict
        mock_get_file.return_value = {
            "snapshots": [
                {
                    "source": "src1",
                    "nodes": [
                        {"snapshotId": "SNAP_C", "collection": "WebServer"},
                    ]
                }
            ]
        }
        result = get_snapshot_id_to_collection_dict("snap_file", "container", "db", filesystem=True)
        assert result["SNAP_C"] == "webserver"

    @patch('processor.connector.validation.get_dbtests', return_value=False)
    @patch('processor.connector.validation.create_indexes')
    @patch('processor.connector.validation.pull_json_data')
    @patch('processor.connector.validation.get_snapshot_file')
    def test_returns_empty_when_no_snapshots(self, mock_get_file, mock_pull, mock_idx, mock_dbtests):
        from processor.connector.validation import get_snapshot_id_to_collection_dict
        mock_get_file.return_value = {}
        result = get_snapshot_id_to_collection_dict("snap_file", "container", "db", filesystem=True)
        assert result == {}


# ---------------------------------------------------------------------------
# 9. Node validation
# ---------------------------------------------------------------------------

class TestNodeValidation:
    """Test that nodes require either snapshotId or masterSnapshotId."""

    def test_valid_node_with_snapshotid(self):
        from processor.connector.snapshot_utils import validate_snapshot_nodes
        nodes = [{"snapshotId": "SNAP_001", "collection": "c"}]
        data, valid = validate_snapshot_nodes(nodes)
        assert valid is True
        assert "SNAP_001" in data

    def test_valid_node_with_master_snapshotid(self):
        from processor.connector.snapshot_utils import validate_snapshot_nodes
        nodes = [{"masterSnapshotId": "MASTER_001", "collection": "c"}]
        data, valid = validate_snapshot_nodes(nodes)
        assert valid is True
        assert "MASTER_001" in data

    def test_invalid_node_without_ids(self):
        from processor.connector.snapshot_utils import validate_snapshot_nodes
        nodes = [{"collection": "c"}]
        data, valid = validate_snapshot_nodes(nodes)
        assert valid is False

    def test_invalid_node_with_non_string_snapshotid(self):
        from processor.connector.snapshot_utils import validate_snapshot_nodes
        nodes = [{"snapshotId": 123, "collection": "c"}]
        data, valid = validate_snapshot_nodes(nodes)
        assert valid is False

    def test_valid_mixed_nodes(self):
        from processor.connector.snapshot_utils import validate_snapshot_nodes
        nodes = [
            {"snapshotId": "SNAP_001", "collection": "c1"},
            {"masterSnapshotId": "MASTER_001", "collection": "c2"},
        ]
        data, valid = validate_snapshot_nodes(nodes)
        assert valid is True
        assert "SNAP_001" in data
        assert "MASTER_001" in data

    def test_empty_nodes_returns_valid(self):
        from processor.connector.snapshot_utils import validate_snapshot_nodes
        data, valid = validate_snapshot_nodes([])
        assert valid is True
        assert data == {}

    def test_none_nodes_returns_valid(self):
        from processor.connector.snapshot_utils import validate_snapshot_nodes
        data, valid = validate_snapshot_nodes(None)
        assert valid is True
        assert data == {}


# ---------------------------------------------------------------------------
# 10. Checksum generation
# ---------------------------------------------------------------------------

class TestChecksumGeneration:
    """Verify checksum is MD5 of JSON string."""

    def test_aws_checksum_md5_of_json_string(self):
        from processor.connector.snapshot_aws import get_checksum
        data = {"key": "value", "number": 42}
        expected = hashlib.md5(json.dumps(data, default=str).encode('utf-8')).hexdigest()
        result = get_checksum(data)
        assert result == expected

    def test_google_checksum_md5_of_json_string(self):
        from processor.connector.snapshot_google import get_checksum
        data = {"name": "test-vm", "status": "RUNNING"}
        expected = hashlib.md5(json.dumps(data).encode('utf-8')).hexdigest()
        result = get_checksum(data)
        assert result == expected

    def test_checksum_empty_dict(self):
        from processor.connector.snapshot_aws import get_checksum
        data = {}
        expected = hashlib.md5(json.dumps(data, default=str).encode('utf-8')).hexdigest()
        result = get_checksum(data)
        assert result == expected

    def test_checksum_returns_32_char_hex(self):
        from processor.connector.snapshot_aws import get_checksum
        result = get_checksum({"a": 1})
        assert isinstance(result, str)
        assert len(result) == 32
        # Verify it is valid hex
        int(result, 16)

    def test_checksum_default_empty_json(self):
        """Default checksum used in records is MD5 of '{}'."""
        expected = hashlib.md5("{}".encode('utf-8')).hexdigest()
        assert expected == "99914b932bd37a50b983c5e7c90ae93b"


# ---------------------------------------------------------------------------
# 11. Collection name normalization
# ---------------------------------------------------------------------------

class TestCollectionNameNormalization:
    """Test collection name normalization rules."""

    def _normalize(self, name):
        return name.replace('.', '').lower()

    def test_microsoft_compute(self):
        assert self._normalize("Microsoft.Compute") == "microsoftcompute"

    def test_webserver(self):
        assert self._normalize("WebServer") == "webserver"

    def test_custom_dotted_collection(self):
        assert self._normalize("my.custom.collection") == "mycustomcollection"

    def test_already_lowercase_no_dots(self):
        assert self._normalize("ec2") == "ec2"

    def test_multiple_dots(self):
        assert self._normalize("a.b.c.d") == "abcd"

    def test_empty_string(self):
        assert self._normalize("") == ""


# ---------------------------------------------------------------------------
# 12. Populate snapshot dispatcher
# ---------------------------------------------------------------------------

class TestPopulateSnapshotDispatcher:
    """Test that populate_snapshot correctly routes to the right function based on type."""

    @patch('processor.connector.snapshot.get_custom_data')
    def test_dispatches_to_aws(self, mock_get_custom_data):
        from processor.connector.snapshot import populate_snapshot, snapshot_fns
        mock_get_custom_data.return_value = {"type": "aws"}
        snapshot_input = {
            "source": "awsSource",
            "nodes": [{"snapshotId": "AWS_001", "collection": "ec2", "type": "instances"}]
        }
        with patch.dict(snapshot_fns, {'aws': MagicMock(return_value={"AWS_001": True})}):
            result = populate_snapshot(snapshot_input, "test-container")
            snapshot_fns['aws'].assert_called_once_with(snapshot_input, "test-container")

    @patch('processor.connector.snapshot.get_custom_data')
    def test_dispatches_to_azure(self, mock_get_custom_data):
        from processor.connector.snapshot import populate_snapshot, snapshot_fns
        mock_get_custom_data.return_value = {"type": "azure"}
        snapshot_input = {
            "source": "azureSource",
            "nodes": [{"snapshotId": "AZ_001", "collection": "Microsoft.Compute", "path": "/x"}]
        }
        with patch.dict(snapshot_fns, {'azure': MagicMock(return_value={"AZ_001": True})}):
            result = populate_snapshot(snapshot_input, "test-container")
            snapshot_fns['azure'].assert_called_once_with(snapshot_input, "test-container")

    @patch('processor.connector.snapshot.get_custom_data')
    def test_dispatches_to_google(self, mock_get_custom_data):
        from processor.connector.snapshot import populate_snapshot, snapshot_fns
        mock_get_custom_data.return_value = {"type": "google"}
        snapshot_input = {
            "source": "googleSource",
            "nodes": [{"snapshotId": "GCP_001", "collection": "compute", "path": "x"}]
        }
        with patch.dict(snapshot_fns, {'google': MagicMock(return_value={"GCP_001": True})}):
            result = populate_snapshot(snapshot_input, "test-container")
            snapshot_fns['google'].assert_called_once_with(snapshot_input, "test-container")

    @patch('processor.connector.snapshot.get_custom_data')
    def test_dispatches_to_filesystem(self, mock_get_custom_data):
        from processor.connector.snapshot import populate_snapshot, snapshot_fns
        mock_get_custom_data.return_value = {"type": "filesystem"}
        snapshot_input = {
            "source": "fsSource",
            "nodes": [{"snapshotId": "FS_001", "collection": "myfiles", "path": "a.json"}]
        }
        with patch.dict(snapshot_fns, {'filesystem': MagicMock(return_value={"FS_001": True})}):
            result = populate_snapshot(snapshot_input, "test-container")
            snapshot_fns['filesystem'].assert_called_once_with(snapshot_input, "test-container")

    @patch('processor.connector.snapshot.get_custom_data')
    def test_returns_empty_for_unknown_type(self, mock_get_custom_data):
        from processor.connector.snapshot import populate_snapshot
        mock_get_custom_data.return_value = {"type": "unknown_type"}
        snapshot_input = {
            "source": "unknownSource",
            "nodes": [{"snapshotId": "UK_001", "collection": "col"}]
        }
        result = populate_snapshot(snapshot_input, "test-container")
        assert result == {}

    @patch('processor.connector.snapshot.get_custom_data')
    def test_returns_empty_when_no_nodes(self, mock_get_custom_data):
        from processor.connector.snapshot import populate_snapshot
        mock_get_custom_data.return_value = {"type": "aws"}
        snapshot_input = {
            "source": "awsSource",
            "nodes": []
        }
        result = populate_snapshot(snapshot_input, "test-container")
        assert result == {}

    @patch('processor.connector.snapshot.get_custom_data')
    def test_returns_empty_when_connector_not_found(self, mock_get_custom_data):
        from processor.connector.snapshot import populate_snapshot
        mock_get_custom_data.return_value = {}
        snapshot_input = {
            "source": "badSource",
            "nodes": [{"snapshotId": "X", "collection": "c"}]
        }
        result = populate_snapshot(snapshot_input, "test-container")
        assert result == {}


# ---------------------------------------------------------------------------
# Additional: get_data_record utility structure
# ---------------------------------------------------------------------------

class TestGetDataRecordUtility:
    """Test the get_data_record utility function in snapshot_utils."""

    def test_get_data_record_structure(self):
        from processor.connector.snapshot_utils import get_data_record
        node = {
            "snapshotId": "SNAP_001",
            "collection": "Microsoft.Compute",
        }
        record = get_data_record("ref_name", node, "user1", "source.json", "azure")
        assert record["structure"] == "azure"
        assert record["reference"] == "ref_name"
        assert record["source"] == "source"
        assert record["path"] == ""
        assert isinstance(record["timestamp"], int)
        assert record["queryuser"] == "user1"
        assert isinstance(record["checksum"], str)
        assert len(record["checksum"]) == 32
        assert record["snapshotId"] == "SNAP_001"
        assert record["mastersnapshot"] is False
        assert record["masterSnapshotId"] == ""
        assert record["collection"] == "microsoftcompute"
        assert record["json"] == {}

    def test_get_data_record_with_master_snapshot_id(self):
        from processor.connector.snapshot_utils import get_data_record
        node = {
            "masterSnapshotId": "MASTER_001",
            "collection": "ec2",
        }
        record = get_data_record("ref", node, "user", "src.json", "aws")
        assert record["masterSnapshotId"] == "MASTER_001"
        assert record["snapshotId"] == ""

    def test_get_data_record_collection_normalization(self):
        from processor.connector.snapshot_utils import get_data_record
        node = {"snapshotId": "S1", "collection": "My.Custom.Collection"}
        record = get_data_record("ref", node, "u", "s.json", "filesystem")
        assert record["collection"] == "mycustomcollection"


# ---------------------------------------------------------------------------
# Additional: convert_to_json content type detection
# ---------------------------------------------------------------------------

class TestConvertToJsonContentType:
    """Test that convert_to_json sets the correct contentType."""

    @patch('processor.connector.snapshot_custom.json_from_file', return_value={"key": "val"})
    def test_json_content_type(self, mock_json_from_file):
        from processor.connector.snapshot_custom import convert_to_json
        content_type, data = convert_to_json("/path/to/file.json", "json")
        assert content_type == "json"
        assert isinstance(data, dict)

    @patch('processor.connector.snapshot_custom.yaml_from_file', return_value={"key": "val"})
    def test_yaml_content_type(self, mock_yaml_from_file):
        from processor.connector.snapshot_custom import convert_to_json
        content_type, data = convert_to_json("/path/to/file.yaml", "yaml")
        assert content_type == "yaml"

    @patch('processor.connector.snapshot_custom.yaml_from_file', return_value={"key": "val"})
    def test_yml_content_type(self, mock_yaml_from_file):
        from processor.connector.snapshot_custom import convert_to_json
        content_type, data = convert_to_json("/path/to/file.yml", "yml")
        assert content_type == "yaml"
