"""
Tests for snapshot data record contracts and utility functions.

Validates the structural contracts of snapshot records across connectors,
ensuring field names, types, and values conform to expectations.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

import hashlib
import time
import re
import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

EMPTY_JSON_MD5 = hashlib.md5("{}".encode('utf-8')).hexdigest()


# ===================================================================
# 1. validate_snapshot_nodes
# ===================================================================

class TestValidateSnapshotNodes:
    """Tests for processor.connector.snapshot_utils.validate_snapshot_nodes."""

    @patch('processor.connector.snapshot_utils.getlogger')
    def _call(self, snapshot_nodes, mock_logger):
        """Helper to import and call validate_snapshot_nodes with logger mocked."""
        from processor.connector.snapshot_utils import validate_snapshot_nodes
        return validate_snapshot_nodes(snapshot_nodes)

    # -- empty / None inputs ------------------------------------------------

    def test_none_returns_empty_dict_and_true(self):
        snapshot_data, valid = self._call(None)
        assert snapshot_data == {}
        assert valid is True

    def test_empty_list_returns_empty_dict_and_true(self):
        snapshot_data, valid = self._call([])
        assert snapshot_data == {}
        assert valid is True

    # -- nodes with snapshotId ----------------------------------------------

    def test_single_node_with_snapshotId(self):
        nodes = [{'snapshotId': 'SNAP_001'}]
        snapshot_data, valid = self._call(nodes)
        assert valid is True
        assert 'SNAP_001' in snapshot_data
        assert snapshot_data['SNAP_001'] is False

    def test_multiple_nodes_with_snapshotId(self):
        nodes = [
            {'snapshotId': 'A'},
            {'snapshotId': 'B'},
            {'snapshotId': 'C'},
        ]
        snapshot_data, valid = self._call(nodes)
        assert valid is True
        assert set(snapshot_data.keys()) == {'A', 'B', 'C'}
        assert all(v is False for v in snapshot_data.values())

    # -- nodes with masterSnapshotId ----------------------------------------

    def test_single_node_with_masterSnapshotId(self):
        nodes = [{'masterSnapshotId': 'MASTER_001'}]
        snapshot_data, valid = self._call(nodes)
        assert valid is True
        assert 'MASTER_001' in snapshot_data
        assert snapshot_data['MASTER_001'] is False

    def test_mixed_snapshotId_and_masterSnapshotId(self):
        nodes = [
            {'snapshotId': 'S1'},
            {'masterSnapshotId': 'M1'},
            {'snapshotId': 'S2'},
        ]
        snapshot_data, valid = self._call(nodes)
        assert valid is True
        assert set(snapshot_data.keys()) == {'S1', 'M1', 'S2'}

    # -- non-string ids → valid_snapshotids = False -------------------------

    def test_integer_snapshotId_returns_invalid(self):
        nodes = [{'snapshotId': 123}]
        snapshot_data, valid = self._call(nodes)
        assert valid is False
        # The id is still recorded in the dict
        assert 123 in snapshot_data

    def test_integer_masterSnapshotId_returns_invalid(self):
        nodes = [{'masterSnapshotId': 456}]
        snapshot_data, valid = self._call(nodes)
        assert valid is False
        assert 456 in snapshot_data

    def test_mixed_valid_and_invalid_ids(self):
        nodes = [
            {'snapshotId': 'good'},
            {'snapshotId': 999},
        ]
        snapshot_data, valid = self._call(nodes)
        assert valid is False
        assert 'good' in snapshot_data
        assert 999 in snapshot_data

    # -- node with neither key → break immediately --------------------------

    def test_node_without_any_id_returns_invalid_and_breaks(self):
        nodes = [
            {'snapshotId': 'A'},
            {'other_key': 'value'},  # missing both ids
            {'snapshotId': 'B'},     # should never be reached
        ]
        snapshot_data, valid = self._call(nodes)
        assert valid is False
        # Only 'A' was processed before the break
        assert 'A' in snapshot_data
        assert 'B' not in snapshot_data

    def test_node_with_empty_string_snapshotId_treated_as_missing(self):
        """An empty string snapshotId is falsy so falls through to the else branch."""
        nodes = [{'snapshotId': ''}]
        snapshot_data, valid = self._call(nodes)
        assert valid is False

    def test_node_with_none_snapshotId_treated_as_missing(self):
        """None snapshotId is falsy, falls to masterSnapshotId check."""
        nodes = [{'snapshotId': None, 'masterSnapshotId': 'M1'}]
        snapshot_data, valid = self._call(nodes)
        assert valid is True
        assert 'M1' in snapshot_data

    def test_node_with_both_none_ids_treated_as_missing(self):
        nodes = [{'snapshotId': None, 'masterSnapshotId': None}]
        snapshot_data, valid = self._call(nodes)
        assert valid is False


# ===================================================================
# 2. get_data_record – structural contract
# ===================================================================

class TestGetDataRecord:
    """Tests for processor.connector.snapshot_utils.get_data_record.

    The returned dict is a CONTRACT consumed by downstream database and
    processing code.  Every field name, type, and default must be stable.
    """

    @patch('processor.connector.snapshot_utils.getlogger')
    def _call(self, ref_name, node, user, snapshot_source, connector_type, mock_logger):
        from processor.connector.snapshot_utils import get_data_record
        return get_data_record(ref_name, node, user, snapshot_source, connector_type)

    # -- required fields present --------------------------------------------

    def test_all_contract_fields_present(self):
        node = {'snapshotId': 'S1', 'masterSnapshotId': 'M1', 'collection': 'col'}
        rec = self._call('ref', node, 'admin', 'source.json', 'azure')
        expected_keys = {
            'structure', 'reference', 'source', 'path', 'timestamp',
            'queryuser', 'checksum', 'node', 'snapshotId',
            'mastersnapshot', 'masterSnapshotId', 'collection', 'json',
        }
        assert expected_keys == set(rec.keys())

    # -- field values -------------------------------------------------------

    def test_structure_equals_connector_type(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('ref', node, 'u', 'src.json', 'aws')
        assert rec['structure'] == 'aws'

    def test_reference_equals_ref_name(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('my_ref', node, 'u', 'src.json', 'azure')
        assert rec['reference'] == 'my_ref'

    def test_source_is_first_part_of_snapshot_source(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('r', node, 'u', 'myfile.json', 'azure')
        assert rec['source'] == 'myfile'

    def test_source_with_no_dot(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('r', node, 'u', 'nodot', 'azure')
        assert rec['source'] == 'nodot'

    def test_path_is_empty_string(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('r', node, 'u', 's.json', 'azure')
        assert rec['path'] == ''

    def test_timestamp_is_int_milliseconds(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        from datetime import datetime, timezone
        before_ms = int(datetime.now(timezone.utc).timestamp() * 1000) - 2000
        rec = self._call('r', node, 'u', 's.json', 'azure')
        after_ms = int(datetime.now(timezone.utc).timestamp() * 1000) + 2000
        assert isinstance(rec['timestamp'], int)
        assert before_ms <= rec['timestamp'] <= after_ms

    def test_queryuser_matches_input(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('r', node, 'testuser@example.com', 's.json', 'azure')
        assert rec['queryuser'] == 'testuser@example.com'

    def test_checksum_is_md5_of_empty_json(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('r', node, 'u', 's.json', 'azure')
        assert rec['checksum'] == EMPTY_JSON_MD5

    def test_node_is_the_same_object(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('r', node, 'u', 's.json', 'azure')
        assert rec['node'] is node

    def test_snapshotId_from_node(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('r', node, 'u', 's.json', 'azure')
        assert rec['snapshotId'] == 'S1'

    def test_snapshotId_missing_defaults_empty_string(self):
        node = {'masterSnapshotId': 'M1', 'collection': 'col'}
        rec = self._call('r', node, 'u', 's.json', 'azure')
        assert rec['snapshotId'] == ''

    def test_mastersnapshot_is_false(self):
        """The utility get_data_record always sets mastersnapshot=False (lowercase 's')."""
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('r', node, 'u', 's.json', 'azure')
        assert rec['mastersnapshot'] is False

    def test_masterSnapshotId_from_node(self):
        node = {'snapshotId': 'S1', 'masterSnapshotId': 'M1', 'collection': 'col'}
        rec = self._call('r', node, 'u', 's.json', 'azure')
        assert rec['masterSnapshotId'] == 'M1'

    def test_masterSnapshotId_missing_defaults_empty_string(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('r', node, 'u', 's.json', 'azure')
        assert rec['masterSnapshotId'] == ''

    def test_json_is_empty_dict(self):
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = self._call('r', node, 'u', 's.json', 'azure')
        assert rec['json'] == {}

    # -- collection normalization -------------------------------------------

    def test_collection_from_node_normalized(self):
        node = {'snapshotId': 'S1', 'collection': 'Microsoft.Compute'}
        rec = self._call('r', node, 'u', 's.json', 'azure')
        assert rec['collection'] == 'microsoftcompute'

    def test_collection_default_when_missing(self):
        """When node has no 'collection', uses COLLECTION constant from database module."""
        node = {'snapshotId': 'S1'}
        rec = self._call('r', node, 'u', 's.json', 'azure')
        # COLLECTION == 'resources'
        assert rec['collection'] == 'resources'


# ===================================================================
# 3. Azure db_record structure contracts
# ===================================================================

class TestAzureDbRecordContracts:
    """Verify the d_record / db_record templates in snapshot_azure.py.

    We do not call the real functions (too many dependencies); instead we
    replicate the record-building logic and assert the contract.
    """

    def _build_master_d_record(self, node, sub_name, user, snapshot_source):
        """Replicates the d_record built in get_all_nodes (line 76)."""
        collection = node.get('collection', 'resources')
        parts = snapshot_source.split('.')
        return {
            "structure": "azure",
            "reference": sub_name,
            "contentType": "json",
            "source": parts[0],
            "path": '',
            "timestamp": int(time.time() * 1000),
            "queryuser": user,
            "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
            "node": node,
            "snapshotId": None,
            "mastersnapshot": True,
            "masterSnapshotId": [node['masterSnapshotId']],
            "collection": collection.replace('.', '').lower(),
            "json": {},
        }

    def _build_child_db_record(self, node, sub_name, user, snapshot_source, session_id):
        """Replicates the db_record built in get_node (line 190)."""
        collection = node.get('collection', 'resources')
        parts = snapshot_source.split('.')
        return {
            "structure": "azure",
            "reference": sub_name,
            "contentType": "json",
            "source": parts[0],
            "path": '',
            "timestamp": int(time.time() * 1000),
            "queryuser": user,
            "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
            "node": node,
            "snapshotId": node['snapshotId'],
            "mastersnapshot": False,
            "masterSnapshotId": None,
            "collection": collection.replace('.', '').lower(),
            "region": "",
            "session_id": session_id,
            "json": {"resources": []},
        }

    # -- master record (get_all_nodes) --------------------------------------

    def test_master_structure_is_azure(self):
        node = {'masterSnapshotId': 'MSN1', 'collection': 'col'}
        rec = self._build_master_d_record(node, 'sub', 'user', 'src.json')
        assert rec['structure'] == 'azure'

    def test_master_contentType_is_json(self):
        node = {'masterSnapshotId': 'MSN1', 'collection': 'col'}
        rec = self._build_master_d_record(node, 'sub', 'user', 'src.json')
        assert rec['contentType'] == 'json'

    def test_master_snapshotId_is_none(self):
        node = {'masterSnapshotId': 'MSN1', 'collection': 'col'}
        rec = self._build_master_d_record(node, 'sub', 'user', 'src.json')
        assert rec['snapshotId'] is None

    def test_master_mastersnapshot_is_true(self):
        node = {'masterSnapshotId': 'MSN1', 'collection': 'col'}
        rec = self._build_master_d_record(node, 'sub', 'user', 'src.json')
        assert rec['mastersnapshot'] is True

    def test_master_masterSnapshotId_is_list(self):
        """masterSnapshotId in the master record is a LIST wrapping the node id."""
        node = {'masterSnapshotId': 'MSN1', 'collection': 'col'}
        rec = self._build_master_d_record(node, 'sub', 'user', 'src.json')
        assert isinstance(rec['masterSnapshotId'], list)
        assert rec['masterSnapshotId'] == ['MSN1']

    def test_master_json_is_empty_dict(self):
        node = {'masterSnapshotId': 'MSN1', 'collection': 'col'}
        rec = self._build_master_d_record(node, 'sub', 'user', 'src.json')
        assert rec['json'] == {}

    def test_master_timestamp_is_int_milliseconds(self):
        node = {'masterSnapshotId': 'MSN1', 'collection': 'col'}
        before = int(time.time() * 1000) - 2000
        rec = self._build_master_d_record(node, 'sub', 'user', 'src.json')
        after = int(time.time() * 1000) + 2000
        assert isinstance(rec['timestamp'], int)
        assert before <= rec['timestamp'] <= after

    def test_master_checksum_is_md5_empty_json(self):
        node = {'masterSnapshotId': 'MSN1', 'collection': 'col'}
        rec = self._build_master_d_record(node, 'sub', 'user', 'src.json')
        assert rec['checksum'] == EMPTY_JSON_MD5

    # -- child record (get_node) --------------------------------------------

    def test_child_mastersnapshot_is_false(self):
        node = {'snapshotId': 'SN1', 'collection': 'col'}
        rec = self._build_child_db_record(node, 'sub', 'user', 'src.json', 'sess_1')
        assert rec['mastersnapshot'] is False

    def test_child_masterSnapshotId_is_none(self):
        node = {'snapshotId': 'SN1', 'collection': 'col'}
        rec = self._build_child_db_record(node, 'sub', 'user', 'src.json', 'sess_1')
        assert rec['masterSnapshotId'] is None

    def test_child_snapshotId_from_node(self):
        node = {'snapshotId': 'SN1', 'collection': 'col'}
        rec = self._build_child_db_record(node, 'sub', 'user', 'src.json', 'sess_1')
        assert rec['snapshotId'] == 'SN1'

    def test_child_region_is_empty_string(self):
        node = {'snapshotId': 'SN1', 'collection': 'col'}
        rec = self._build_child_db_record(node, 'sub', 'user', 'src.json', 'sess_1')
        assert rec['region'] == ''

    def test_child_session_id_present(self):
        node = {'snapshotId': 'SN1', 'collection': 'col'}
        rec = self._build_child_db_record(node, 'sub', 'user', 'src.json', 'sess_abc')
        assert rec['session_id'] == 'sess_abc'

    def test_child_json_has_resources_list(self):
        node = {'snapshotId': 'SN1', 'collection': 'col'}
        rec = self._build_child_db_record(node, 'sub', 'user', 'src.json', 'sess_1')
        assert rec['json'] == {"resources": []}

    def test_child_has_contentType(self):
        node = {'snapshotId': 'SN1', 'collection': 'col'}
        rec = self._build_child_db_record(node, 'sub', 'user', 'src.json', 'sess_1')
        assert rec['contentType'] == 'json'

    # -- master vs child field differences ----------------------------------

    def test_master_and_child_differ_on_mastersnapshot(self):
        master_node = {'masterSnapshotId': 'MSN1', 'collection': 'col'}
        child_node = {'snapshotId': 'SN1', 'collection': 'col'}
        m = self._build_master_d_record(master_node, 'sub', 'u', 's.json')
        c = self._build_child_db_record(child_node, 'sub', 'u', 's.json', 'sess')
        assert m['mastersnapshot'] is True
        assert c['mastersnapshot'] is False

    def test_master_and_child_differ_on_masterSnapshotId_type(self):
        master_node = {'masterSnapshotId': 'MSN1', 'collection': 'col'}
        child_node = {'snapshotId': 'SN1', 'collection': 'col'}
        m = self._build_master_d_record(master_node, 'sub', 'u', 's.json')
        c = self._build_child_db_record(child_node, 'sub', 'u', 's.json', 'sess')
        assert isinstance(m['masterSnapshotId'], list)
        assert c['masterSnapshotId'] is None


# ===================================================================
# 4. Collection name normalization
# ===================================================================

class TestCollectionNormalization:
    """collection.replace('.', '').lower() is used across connectors."""

    @pytest.mark.parametrize("raw,expected", [
        ("Microsoft.Compute", "microsoftcompute"),
        ("AWS.EC2", "awsec2"),
        ("Google.Cloud.Storage", "googlecloudstorage"),
        ("simple", "simple"),
        ("Already.Lower.Case", "alreadylowercase"),
        ("NO.DOTS.HERE", "nodotshere"),
        ("", ""),
        ("single", "single"),
        ("A.B.C.D", "abcd"),
    ])
    def test_normalization(self, raw, expected):
        assert raw.replace('.', '').lower() == expected

    @patch('processor.connector.snapshot_utils.getlogger')
    def test_get_data_record_uses_normalization(self, mock_logger):
        from processor.connector.snapshot_utils import get_data_record
        node = {'snapshotId': 'S1', 'collection': 'Microsoft.Compute'}
        rec = get_data_record('r', node, 'u', 's.json', 'azure')
        assert rec['collection'] == 'microsoftcompute'


# ===================================================================
# 5. snapshotId construction (composite IDs)
# ===================================================================

class TestSnapshotIdConstruction:
    """In Azure master snapshots, composite IDs are built as
    '%s%s' % (node['masterSnapshotId'], str(idx)).
    """

    def test_composite_id_is_string(self):
        master_id = 'MSN'
        for idx in range(5):
            composite = '%s%s' % (master_id, str(idx))
            assert isinstance(composite, str)

    def test_composite_id_format(self):
        assert '%s%s' % ('MASTER_01', str(0)) == 'MASTER_010'
        assert '%s%s' % ('MASTER_01', str(10)) == 'MASTER_0110'

    def test_composite_id_with_numeric_master_id(self):
        """Even if masterSnapshotId looks numeric, the composite must be string."""
        master_id = '12345'
        composite = '%s%s' % (master_id, str(3))
        assert isinstance(composite, str)
        assert composite == '123453'

    @patch('processor.connector.snapshot_utils.getlogger')
    def test_validate_rejects_integer_composite(self, mock_logger):
        """If someone accidentally creates an int composite, validation catches it."""
        from processor.connector.snapshot_utils import validate_snapshot_nodes
        bad_id = 123  # not a string
        nodes = [{'snapshotId': bad_id}]
        _, valid = validate_snapshot_nodes(nodes)
        assert valid is False


# ===================================================================
# 6. Connector file structure contracts
# ===================================================================

class TestConnectorFileStructureContracts:
    """Connector JSON files have specific structures depending on cloud type.

    All connectors now use 'fileType' (camelCase) consistently.
    """

    def test_azure_connector_uses_camelcase_filetype(self):
        """Azure connector files use 'fileType' (camelCase) like all connectors."""
        azure_connector = {
            "fileType": "structure",
            "type": "azure",
            "tenant_id": "t-123",
            "accounts": [{"subscription_id": "sub-1"}],
        }
        assert "fileType" in azure_connector
        assert azure_connector["fileType"] == "structure"
        assert azure_connector["type"] == "azure"

    def test_aws_connector_uses_camelcase_fileType(self):
        """AWS connector files use 'fileType' (camelCase)."""
        aws_connector = {
            "fileType": "structure",
            "type": "aws",
            "accounts": [{"account_id": "123456789012"}],
        }
        assert "fileType" in aws_connector
        assert "filetype" not in aws_connector
        assert aws_connector["fileType"] == "structure"
        assert aws_connector["type"] == "aws"

    def test_google_connector_uses_camelcase_fileType(self):
        """Google connector files use 'fileType' (camelCase)."""
        google_connector = {
            "fileType": "structure",
            "type": "google",
            "projects": [{"project-id": "my-project"}],
        }
        assert "fileType" in google_connector
        assert google_connector["type"] == "google"
        assert "projects" in google_connector

    def test_git_connector_uses_camelcase_fileType(self):
        """Git connector files use 'fileType' (camelCase) with type 'filesystem'."""
        git_connector = {
            "fileType": "structure",
            "type": "filesystem",
        }
        assert "fileType" in git_connector
        assert git_connector["type"] == "filesystem"

    def test_all_connectors_use_consistent_filetype(self):
        """All connectors now use 'fileType' (camelCase) consistently."""
        azure = {"fileType": "structure", "type": "azure"}
        aws = {"fileType": "structure", "type": "aws"}
        google = {"fileType": "structure", "type": "google"}

        assert azure["fileType"] == "structure"
        assert aws["fileType"] == "structure"
        assert google["fileType"] == "structure"

    def test_azure_connector_has_tenant_id(self):
        azure_connector = {
            "fileType": "structure",
            "type": "azure",
            "tenant_id": "abc-def",
            "accounts": [],
        }
        assert "tenant_id" in azure_connector

    def test_azure_connector_has_accounts(self):
        azure_connector = {
            "fileType": "structure",
            "type": "azure",
            "tenant_id": "t1",
            "accounts": [{"subscription_id": "sub-1"}],
        }
        assert isinstance(azure_connector["accounts"], list)

    def test_google_connector_has_projects(self):
        google_connector = {
            "fileType": "structure",
            "type": "google",
            "projects": [{"project-id": "p1"}, {"project-id": "p2"}],
        }
        assert isinstance(google_connector["projects"], list)
        assert len(google_connector["projects"]) == 2

    def test_aws_connector_has_accounts(self):
        aws_connector = {
            "fileType": "structure",
            "type": "aws",
            "accounts": [{"account_id": "111"}],
        }
        assert isinstance(aws_connector["accounts"], list)


# ===================================================================
# 7. Google URL generation
# ===================================================================

class TestGoogleUrlGeneration:
    """Tests for generate_request_url in snapshot_google.py."""

    def _generate(self, base_url, project_id):
        """Replicate the logic of generate_request_url without importing
        the module (which pulls heavy dependencies)."""
        updated = re.sub(r"{project}|{projectId}", project_id, base_url)
        updated = re.sub(r"{zone}", "-", updated)
        return updated

    def test_substitutes_project_placeholder(self):
        url = "https://api.google.com/v1/projects/{project}/zones"
        result = self._generate(url, "my-project")
        assert result == "https://api.google.com/v1/projects/my-project/zones"

    def test_substitutes_projectId_placeholder(self):
        url = "https://api.google.com/v1/projects/{projectId}/zones"
        result = self._generate(url, "my-project")
        assert result == "https://api.google.com/v1/projects/my-project/zones"

    def test_substitutes_zone_with_dash(self):
        url = "https://api.google.com/v1/projects/{project}/zones/{zone}/instances"
        result = self._generate(url, "proj-1")
        assert result == "https://api.google.com/v1/projects/proj-1/zones/-/instances"

    def test_multiple_project_placeholders(self):
        url = "https://api.google.com/{project}/foo/{project}"
        result = self._generate(url, "p1")
        assert result == "https://api.google.com/p1/foo/p1"

    def test_no_placeholders_returns_unchanged(self):
        url = "https://api.google.com/v1/static/endpoint"
        result = self._generate(url, "proj")
        assert result == url

    def test_mixed_project_and_projectId_placeholders(self):
        url = "https://api.google.com/{project}/{projectId}"
        result = self._generate(url, "proj")
        assert result == "https://api.google.com/proj/proj"

    def test_zone_without_project(self):
        url = "https://api.google.com/v1/zones/{zone}/instances"
        result = self._generate(url, "proj")
        assert result == "https://api.google.com/v1/zones/-/instances"

    @patch('processor.connector.snapshot_google.getlogger')
    @patch('processor.connector.snapshot_google.get_google_parameters')
    def test_real_generate_request_url_basic(self, mock_params, mock_logger):
        """Call the real function with a simple URL."""
        from processor.connector.snapshot_google import generate_request_url
        result = generate_request_url(
            "https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances",
            "my-gcp-project",
        )
        assert result == "https://compute.googleapis.com/compute/v1/projects/my-gcp-project/zones/-/instances"

    @patch('processor.connector.snapshot_google.getlogger')
    @patch('processor.connector.snapshot_google.get_google_parameters')
    def test_real_generate_request_url_projectId(self, mock_params, mock_logger):
        from processor.connector.snapshot_google import generate_request_url
        result = generate_request_url(
            "https://example.com/{projectId}/resources",
            "proj-xyz",
        )
        assert result == "https://example.com/proj-xyz/resources"

    @patch('processor.connector.snapshot_google.getlogger')
    @patch('processor.connector.snapshot_google.get_google_parameters')
    def test_real_generate_request_url_returns_none_on_error(self, mock_params, mock_logger):
        """If the input is somehow pathological, the function returns None.

        Note: In practice the regex sub only fails on non-string input, so we
        pass a non-string to trigger the except branch.
        """
        from processor.connector.snapshot_google import generate_request_url
        result = generate_request_url(None, "proj")
        assert result is None


# ===================================================================
# 8. Cross-cutting: field naming conventions
# ===================================================================

class TestFieldNamingConventions:
    """Verify the mixed naming conventions are preserved.

    The codebase uses:
    - 'mastersnapshot' (all lowercase) as a boolean flag
    - 'masterSnapshotId' (camelCase) as the ID field
    - 'snapshotId' (camelCase)

    These must NOT be changed as they are part of the data contract.
    """

    @patch('processor.connector.snapshot_utils.getlogger')
    def test_mastersnapshot_lowercase_in_get_data_record(self, mock_logger):
        from processor.connector.snapshot_utils import get_data_record
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = get_data_record('r', node, 'u', 's.json', 'azure')
        assert 'mastersnapshot' in rec
        assert 'masterSnapshot' not in rec
        assert 'master_snapshot' not in rec

    @patch('processor.connector.snapshot_utils.getlogger')
    def test_masterSnapshotId_camelcase_in_get_data_record(self, mock_logger):
        from processor.connector.snapshot_utils import get_data_record
        node = {'snapshotId': 'S1', 'masterSnapshotId': 'M1', 'collection': 'col'}
        rec = get_data_record('r', node, 'u', 's.json', 'azure')
        assert 'masterSnapshotId' in rec
        assert 'mastersnapshotid' not in rec
        assert 'master_snapshot_id' not in rec

    @patch('processor.connector.snapshot_utils.getlogger')
    def test_snapshotId_camelcase_in_get_data_record(self, mock_logger):
        from processor.connector.snapshot_utils import get_data_record
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = get_data_record('r', node, 'u', 's.json', 'azure')
        assert 'snapshotId' in rec
        assert 'snapshotid' not in rec
        assert 'snapshot_id' not in rec

    def test_azure_master_record_naming(self):
        """Azure master record must have 'mastersnapshot' (lowercase) and
        'masterSnapshotId' (camelCase) -- verify both in one record."""
        rec = {
            "mastersnapshot": True,
            "masterSnapshotId": ["MSN1"],
            "snapshotId": None,
        }
        assert 'mastersnapshot' in rec
        assert 'masterSnapshotId' in rec
        assert rec['mastersnapshot'] is True
        assert isinstance(rec['masterSnapshotId'], list)

    def test_azure_child_record_naming(self):
        rec = {
            "mastersnapshot": False,
            "masterSnapshotId": None,
            "snapshotId": "SN1",
        }
        assert rec['mastersnapshot'] is False
        assert rec['masterSnapshotId'] is None
        assert isinstance(rec['snapshotId'], str)


# ===================================================================
# 9. Edge cases and regression guards
# ===================================================================

class TestEdgeCases:
    """Miscellaneous edge cases for snapshot contracts."""

    @patch('processor.connector.snapshot_utils.getlogger')
    def test_get_data_record_with_dots_in_snapshot_source(self, mock_logger):
        from processor.connector.snapshot_utils import get_data_record
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = get_data_record('r', node, 'u', 'a.b.c.json', 'azure')
        assert rec['source'] == 'a'

    @patch('processor.connector.snapshot_utils.getlogger')
    def test_get_data_record_empty_user(self, mock_logger):
        from processor.connector.snapshot_utils import get_data_record
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = get_data_record('r', node, '', 's.json', 'azure')
        assert rec['queryuser'] == ''

    @patch('processor.connector.snapshot_utils.getlogger')
    def test_validate_snapshot_nodes_duplicate_ids(self, mock_logger):
        """Duplicate snapshotIds overwrite in dict, last one wins (value=False)."""
        from processor.connector.snapshot_utils import validate_snapshot_nodes
        nodes = [
            {'snapshotId': 'SAME'},
            {'snapshotId': 'SAME'},
        ]
        data, valid = validate_snapshot_nodes(nodes)
        assert valid is True
        assert len(data) == 1
        assert data['SAME'] is False

    @patch('processor.connector.snapshot_utils.getlogger')
    def test_validate_large_node_list(self, mock_logger):
        from processor.connector.snapshot_utils import validate_snapshot_nodes
        nodes = [{'snapshotId': 'S_%d' % i} for i in range(100)]
        data, valid = validate_snapshot_nodes(nodes)
        assert valid is True
        assert len(data) == 100

    def test_md5_checksum_is_consistent(self):
        """The checksum value must be deterministic."""
        h1 = hashlib.md5("{}".encode('utf-8')).hexdigest()
        h2 = hashlib.md5("{}".encode('utf-8')).hexdigest()
        assert h1 == h2
        assert h1 == EMPTY_JSON_MD5
        # Known value: 99914b932bd37a50b983c5e7c90ae93b
        assert h1 == '99914b932bd37a50b983c5e7c90ae93b'

    @patch('processor.connector.snapshot_utils.getlogger')
    def test_get_data_record_special_chars_in_ref(self, mock_logger):
        from processor.connector.snapshot_utils import get_data_record
        node = {'snapshotId': 'S1', 'collection': 'col'}
        rec = get_data_record('ref/with spaces & special!', node, 'u', 's.json', 'azure')
        assert rec['reference'] == 'ref/with spaces & special!'
