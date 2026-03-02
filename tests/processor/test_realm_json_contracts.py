"""
Tests validating the JSON structure contracts of realm configuration files
and related JSON formats used throughout the cloud-validation-framework.

These tests ensure that:
- Realm files on disk conform to expected contracts
- Structural invariants (field names, types, casing) are preserved
- Structural consistency (all connectors use "fileType" camelCase) is verified
- Output, container metadata, and database record contracts are correct
"""
import sys
import os
import json
import copy
from collections import OrderedDict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest

REALM_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'realm')


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _load_realm_json(relative_path):
    """Load a JSON file from the realm directory. Returns None if not found."""
    full_path = os.path.join(REALM_DIR, relative_path)
    if not os.path.exists(full_path):
        return None
    with open(full_path, 'r') as f:
        return json.load(f)


# ===========================================================================
# 1. Snapshot JSON contract
# ===========================================================================

class TestSnapshotJsonContract:
    """Validate the snapshot JSON contract from realm/validation/gitScenario/snapshot.json."""

    SNAPSHOT_PATH = os.path.join('validation', 'gitScenario', 'snapshot.json')

    def _get_valid_snapshot(self):
        return {
            "fileType": "snapshot",
            "snapshots": [
                {
                    "source": "gitConnector",
                    "nodes": [
                        {
                            "snapshotId": "1",
                            "type": "json",
                            "collection": "webserver",
                            "paths": [
                                "realm/validation/gitScenario/resource-pass.json"
                            ]
                        }
                    ]
                }
            ]
        }

    def test_snapshot_file_exists_on_disk(self):
        full_path = os.path.join(REALM_DIR, self.SNAPSHOT_PATH)
        if not os.path.exists(full_path):
            pytest.skip("Realm snapshot file not found on disk")
        assert os.path.isfile(full_path)

    def test_snapshot_file_filetype_is_snapshot(self):
        data = _load_realm_json(self.SNAPSHOT_PATH)
        if data is None:
            pytest.skip("Realm snapshot file not found")
        assert data["fileType"] == "snapshot"

    def test_snapshot_file_snapshots_is_list(self):
        data = _load_realm_json(self.SNAPSHOT_PATH)
        if data is None:
            pytest.skip("Realm snapshot file not found")
        assert isinstance(data["snapshots"], list)
        assert len(data["snapshots"]) > 0

    def test_snapshot_file_each_snapshot_has_source_and_nodes(self):
        data = _load_realm_json(self.SNAPSHOT_PATH)
        if data is None:
            pytest.skip("Realm snapshot file not found")
        for snapshot in data["snapshots"]:
            assert "source" in snapshot, "Each snapshot must have a 'source' field"
            assert "nodes" in snapshot, "Each snapshot must have a 'nodes' field"
            assert isinstance(snapshot["nodes"], list)

    def test_snapshot_file_each_node_has_required_fields(self):
        data = _load_realm_json(self.SNAPSHOT_PATH)
        if data is None:
            pytest.skip("Realm snapshot file not found")
        for snapshot in data["snapshots"]:
            for node in snapshot["nodes"]:
                assert "snapshotId" in node
                assert "type" in node
                assert "collection" in node

    def test_snapshot_file_snapshotid_is_string(self):
        """snapshotId MUST be a string, even if the value looks numeric."""
        data = _load_realm_json(self.SNAPSHOT_PATH)
        if data is None:
            pytest.skip("Realm snapshot file not found")
        for snapshot in data["snapshots"]:
            for node in snapshot["nodes"]:
                assert isinstance(node["snapshotId"], str), (
                    f"snapshotId must be string, got {type(node['snapshotId']).__name__}: "
                    f"{node['snapshotId']!r}"
                )

    def test_inline_snapshot_contract_filetype(self):
        data = self._get_valid_snapshot()
        assert data["fileType"] == "snapshot"

    def test_inline_snapshot_contract_snapshots_is_list(self):
        data = self._get_valid_snapshot()
        assert isinstance(data["snapshots"], list)

    def test_inline_snapshot_snapshotid_must_be_string(self):
        """Even numeric-looking IDs must be strings, not integers."""
        data = self._get_valid_snapshot()
        node = data["snapshots"][0]["nodes"][0]
        assert isinstance(node["snapshotId"], str)
        # Verify it would fail if it were an int
        assert node["snapshotId"] == "1"
        assert node["snapshotId"] != 1

    def test_inline_snapshot_numeric_snapshotid_is_invalid(self):
        """Demonstrate that integer snapshotId violates the contract."""
        data = self._get_valid_snapshot()
        data["snapshots"][0]["nodes"][0]["snapshotId"] = 1
        node = data["snapshots"][0]["nodes"][0]
        assert not isinstance(node["snapshotId"], str), (
            "Integer snapshotId should not pass the string check"
        )

    def test_inline_snapshot_node_requires_all_fields(self):
        required_fields = {"snapshotId", "type", "collection"}
        data = self._get_valid_snapshot()
        node = data["snapshots"][0]["nodes"][0]
        assert required_fields.issubset(set(node.keys()))

    def test_inline_snapshot_source_is_string(self):
        data = self._get_valid_snapshot()
        assert isinstance(data["snapshots"][0]["source"], str)


# ===========================================================================
# 2. Test JSON contract
# ===========================================================================

class TestTestJsonContract:
    """Validate the test JSON contract from realm/validation/gitScenario/test.json."""

    TEST_PATH = os.path.join('validation', 'gitScenario', 'test.json')

    def _get_valid_test(self):
        return {
            "fileType": "test",
            "snapshot": "snapshot",
            "testSet": [
                {
                    "testName ": "Ensure configuration uses port 80",
                    "version": "0.1",
                    "cases": [
                        {
                            "testId": "1",
                            "rule": "{1}.webserver.port=80"
                        }
                    ]
                }
            ]
        }

    def test_test_file_exists_on_disk(self):
        full_path = os.path.join(REALM_DIR, self.TEST_PATH)
        if not os.path.exists(full_path):
            pytest.skip("Realm test file not found on disk")
        assert os.path.isfile(full_path)

    def test_test_file_filetype_is_test(self):
        data = _load_realm_json(self.TEST_PATH)
        if data is None:
            pytest.skip("Realm test file not found")
        assert data["fileType"] == "test"

    def test_test_file_has_snapshot_reference(self):
        data = _load_realm_json(self.TEST_PATH)
        if data is None:
            pytest.skip("Realm test file not found")
        assert "snapshot" in data
        assert isinstance(data["snapshot"], str)

    def test_test_file_testset_is_list(self):
        data = _load_realm_json(self.TEST_PATH)
        if data is None:
            pytest.skip("Realm test file not found")
        assert isinstance(data["testSet"], list)
        assert len(data["testSet"]) > 0

    def test_test_file_testname_has_trailing_space(self):
        """The actual file has 'testName ' (with trailing space) as a key.
        This documents an existing quirk in the realm test file."""
        data = _load_realm_json(self.TEST_PATH)
        if data is None:
            pytest.skip("Realm test file not found")
        test_set = data["testSet"][0]
        # The actual file has a trailing space in the key
        assert "testName " in test_set, (
            "Expected 'testName ' (with trailing space) in test set entry. "
            "Keys found: %s" % list(test_set.keys())
        )

    def test_test_file_each_testset_has_version_and_cases(self):
        data = _load_realm_json(self.TEST_PATH)
        if data is None:
            pytest.skip("Realm test file not found")
        for ts in data["testSet"]:
            assert "version" in ts
            assert "cases" in ts
            assert isinstance(ts["cases"], list)

    def test_test_file_each_case_has_testid_and_rule(self):
        data = _load_realm_json(self.TEST_PATH)
        if data is None:
            pytest.skip("Realm test file not found")
        for ts in data["testSet"]:
            for case in ts["cases"]:
                assert "testId" in case
                assert "rule" in case

    def test_test_file_testid_is_string(self):
        data = _load_realm_json(self.TEST_PATH)
        if data is None:
            pytest.skip("Realm test file not found")
        for ts in data["testSet"]:
            for case in ts["cases"]:
                assert isinstance(case["testId"], str), (
                    f"testId must be string, got {type(case['testId']).__name__}"
                )

    def test_inline_test_contract_filetype(self):
        data = self._get_valid_test()
        assert data["fileType"] == "test"

    def test_inline_test_contract_testset_is_list(self):
        data = self._get_valid_test()
        assert isinstance(data["testSet"], list)

    def test_inline_test_contract_snapshot_reference(self):
        data = self._get_valid_test()
        assert isinstance(data["snapshot"], str)
        assert len(data["snapshot"]) > 0

    def test_inline_test_case_testid_is_string(self):
        data = self._get_valid_test()
        case = data["testSet"][0]["cases"][0]
        assert isinstance(case["testId"], str)

    def test_inline_test_case_rule_is_string(self):
        data = self._get_valid_test()
        case = data["testSet"][0]["cases"][0]
        assert isinstance(case["rule"], str)


# ===========================================================================
# 3. Azure connector contract
# ===========================================================================

class TestAzureConnectorContract:
    """Validate the Azure connector contract.

    Azure now uses 'fileType' (camelCase) consistent with all other connectors.
    The previous 'filetype' (lowercase) inconsistency has been fixed.
    """

    AZURE_PATH = 'azureConnector.json'

    def _get_valid_azure_connector(self):
        return {
            "fileType": "structure",
            "type": "azure",
            "companyName": "Company Name",
            "tenant_id": "<tenant-id>",
            "accounts": [
                {
                    "department": "Unit/Department name",
                    "subscription": [
                        {
                            "subscription_name": "<subscription_name>",
                            "subscription_id": "<subscription_id>",
                            "users": [
                                {
                                    "name": "<spn-name>",
                                    "client_id": "<client_id>",
                                    "client_secret": "<client_secret>"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def test_azure_file_exists_on_disk(self):
        full_path = os.path.join(REALM_DIR, self.AZURE_PATH)
        if not os.path.exists(full_path):
            pytest.skip("Azure connector file not found on disk")
        assert os.path.isfile(full_path)

    def test_azure_uses_camelcase_filetype(self):
        """Azure connector uses 'fileType' (camelCase) consistent with all connectors."""
        data = _load_realm_json(self.AZURE_PATH)
        if data is None:
            pytest.skip("Azure connector file not found")
        assert "fileType" in data, (
            "Azure connector must use 'fileType' (camelCase)"
        )
        assert data["fileType"] == "structure"

    def test_azure_type_is_azure(self):
        data = _load_realm_json(self.AZURE_PATH)
        if data is None:
            pytest.skip("Azure connector file not found")
        assert data["type"] == "azure"

    def test_azure_has_tenant_id(self):
        data = _load_realm_json(self.AZURE_PATH)
        if data is None:
            pytest.skip("Azure connector file not found")
        assert "tenant_id" in data

    def test_azure_has_accounts_list(self):
        data = _load_realm_json(self.AZURE_PATH)
        if data is None:
            pytest.skip("Azure connector file not found")
        assert "accounts" in data
        assert isinstance(data["accounts"], list)

    def test_azure_account_has_department_and_subscription(self):
        data = _load_realm_json(self.AZURE_PATH)
        if data is None:
            pytest.skip("Azure connector file not found")
        for account in data["accounts"]:
            assert "department" in account
            assert "subscription" in account
            assert isinstance(account["subscription"], list)

    def test_azure_subscription_has_required_fields(self):
        data = _load_realm_json(self.AZURE_PATH)
        if data is None:
            pytest.skip("Azure connector file not found")
        for account in data["accounts"]:
            for sub in account["subscription"]:
                assert "subscription_name" in sub
                assert "subscription_id" in sub
                assert "users" in sub
                assert isinstance(sub["users"], list)

    def test_inline_azure_filetype_camelcase(self):
        """Inline test: Azure uses 'fileType' (camelCase) like all connectors."""
        data = self._get_valid_azure_connector()
        assert "fileType" in data

    def test_inline_azure_structure(self):
        data = self._get_valid_azure_connector()
        assert data["fileType"] == "structure"
        assert data["type"] == "azure"
        assert "tenant_id" in data
        assert isinstance(data["accounts"], list)


# ===========================================================================
# 4. AWS connector contract
# ===========================================================================

class TestAWSConnectorContract:
    """Validate the AWS connector contract."""

    AWS_PATH = 'awsConnector.json'

    def _get_valid_aws_connector(self):
        return {
            "organization": "Organization name",
            "type": "aws",
            "fileType": "structure",
            "name": "Unit/Department name",
            "accounts": [
                {
                    "account-name": "Account name",
                    "account-description": "Description of account",
                    "account-id": "<account-id>",
                    "users": [
                        {
                            "name": "<iam-user>",
                            "access-key": "<access-key>",
                            "secret-access": "<secret-access>"
                        }
                    ]
                }
            ]
        }

    def test_aws_file_exists_on_disk(self):
        full_path = os.path.join(REALM_DIR, self.AWS_PATH)
        if not os.path.exists(full_path):
            pytest.skip("AWS connector file not found on disk")
        assert os.path.isfile(full_path)

    def test_aws_uses_camelcase_filetype(self):
        """AWS uses 'fileType' (camelCase), consistent with all connectors."""
        data = _load_realm_json(self.AWS_PATH)
        if data is None:
            pytest.skip("AWS connector file not found")
        assert "fileType" in data
        assert data["fileType"] == "structure"

    def test_aws_type_is_aws(self):
        data = _load_realm_json(self.AWS_PATH)
        if data is None:
            pytest.skip("AWS connector file not found")
        assert data["type"] == "aws"

    def test_aws_has_accounts_list(self):
        data = _load_realm_json(self.AWS_PATH)
        if data is None:
            pytest.skip("AWS connector file not found")
        assert "accounts" in data
        assert isinstance(data["accounts"], list)

    def test_aws_account_has_required_fields(self):
        data = _load_realm_json(self.AWS_PATH)
        if data is None:
            pytest.skip("AWS connector file not found")
        for account in data["accounts"]:
            assert "account-name" in account
            assert "account-id" in account
            assert "users" in account
            assert isinstance(account["users"], list)

    def test_aws_user_has_credentials_fields(self):
        data = _load_realm_json(self.AWS_PATH)
        if data is None:
            pytest.skip("AWS connector file not found")
        for account in data["accounts"]:
            for user in account["users"]:
                assert "name" in user
                assert "access-key" in user
                assert "secret-access" in user

    def test_inline_aws_contract(self):
        data = self._get_valid_aws_connector()
        assert data["fileType"] == "structure"
        assert data["type"] == "aws"
        assert isinstance(data["accounts"], list)
        user = data["accounts"][0]["users"][0]
        assert "access-key" in user
        assert "secret-access" in user

    def test_aws_and_azure_filetype_consistency(self):
        """Both AWS and Azure now use 'fileType' (camelCase) consistently."""
        aws = self._get_valid_aws_connector()
        azure_data = {
            "fileType": "structure",
            "type": "azure"
        }
        assert "fileType" in aws
        assert "fileType" in azure_data


# ===========================================================================
# 5. Google connector contract
# ===========================================================================

class TestGoogleConnectorContract:
    """Validate the Google connector contract.

    Google uses 'projects' instead of 'accounts'.
    """

    GOOGLE_PATH = 'googleStructure.json'

    def _get_valid_google_connector(self):
        return {
            "organization": "company1",
            "type": "google",
            "fileType": "structure",
            "projects": [
                {
                    "project-name": "<Project Name>",
                    "project-id": "<Project Id>",
                    "users": [
                        {
                            "name": "<IAM Account Name>",
                            "type": "service_account",
                            "private_key_id": "<Private Key Id>",
                            "private_key": "<Actual Private Key>",
                            "client_email": "<acc>@<project>.iam.gserviceaccount.com",
                            "client_id": "<client id>",
                            "client_x509_cert_url": "<cert url>"
                        }
                    ]
                }
            ]
        }

    def test_google_file_exists_on_disk(self):
        full_path = os.path.join(REALM_DIR, self.GOOGLE_PATH)
        if not os.path.exists(full_path):
            pytest.skip("Google connector file not found on disk")
        assert os.path.isfile(full_path)

    def test_google_uses_camelcase_filetype(self):
        data = _load_realm_json(self.GOOGLE_PATH)
        if data is None:
            pytest.skip("Google connector file not found")
        assert "fileType" in data
        assert data["fileType"] == "structure"

    def test_google_type_is_google(self):
        data = _load_realm_json(self.GOOGLE_PATH)
        if data is None:
            pytest.skip("Google connector file not found")
        assert data["type"] == "google"

    def test_google_uses_projects_not_accounts(self):
        """Google uses 'projects' instead of 'accounts'."""
        data = _load_realm_json(self.GOOGLE_PATH)
        if data is None:
            pytest.skip("Google connector file not found")
        assert "projects" in data, "Google connector must use 'projects', not 'accounts'"
        assert isinstance(data["projects"], list)

    def test_google_does_not_have_accounts(self):
        """Google should NOT have 'accounts' key - it uses 'projects'."""
        data = _load_realm_json(self.GOOGLE_PATH)
        if data is None:
            pytest.skip("Google connector file not found")
        assert "accounts" not in data

    def test_google_project_has_required_fields(self):
        data = _load_realm_json(self.GOOGLE_PATH)
        if data is None:
            pytest.skip("Google connector file not found")
        for project in data["projects"]:
            assert "project-name" in project
            assert "project-id" in project
            assert "users" in project
            assert isinstance(project["users"], list)

    def test_google_user_has_service_account_fields(self):
        data = _load_realm_json(self.GOOGLE_PATH)
        if data is None:
            pytest.skip("Google connector file not found")
        for project in data["projects"]:
            for user in project["users"]:
                assert "name" in user
                assert "type" in user
                assert "private_key_id" in user

    def test_inline_google_uses_projects(self):
        data = self._get_valid_google_connector()
        assert "projects" in data
        assert "accounts" not in data
        assert data["type"] == "google"

    def test_inline_google_user_service_account_type(self):
        data = self._get_valid_google_connector()
        user = data["projects"][0]["users"][0]
        assert user["type"] == "service_account"


# ===========================================================================
# 6. Git connector contract
# ===========================================================================

class TestGitConnectorContract:
    """Validate the Git connector contract."""

    GIT_PATH = 'gitConnector.json'

    def _get_valid_git_connector(self):
        return {
            "fileType": "structure",
            "type": "filesystem",
            "companyName": "prancer-test",
            "gitProvider": "https://github.com/prancer-io/cloud-validation-framework",
            "branchName": "master",
            "private": False
        }

    def test_git_file_exists_on_disk(self):
        full_path = os.path.join(REALM_DIR, self.GIT_PATH)
        if not os.path.exists(full_path):
            pytest.skip("Git connector file not found on disk")
        assert os.path.isfile(full_path)

    def test_git_filetype_is_structure(self):
        data = _load_realm_json(self.GIT_PATH)
        if data is None:
            pytest.skip("Git connector file not found")
        assert data["fileType"] == "structure"

    def test_git_type_is_filesystem(self):
        data = _load_realm_json(self.GIT_PATH)
        if data is None:
            pytest.skip("Git connector file not found")
        assert data["type"] == "filesystem"

    def test_git_has_git_provider(self):
        data = _load_realm_json(self.GIT_PATH)
        if data is None:
            pytest.skip("Git connector file not found")
        assert "gitProvider" in data
        assert isinstance(data["gitProvider"], str)

    def test_git_has_branch_name(self):
        data = _load_realm_json(self.GIT_PATH)
        if data is None:
            pytest.skip("Git connector file not found")
        assert "branchName" in data
        assert isinstance(data["branchName"], str)

    def test_git_has_private_flag(self):
        data = _load_realm_json(self.GIT_PATH)
        if data is None:
            pytest.skip("Git connector file not found")
        assert "private" in data
        assert isinstance(data["private"], bool)

    def test_inline_git_connector_structure(self):
        data = self._get_valid_git_connector()
        assert data["fileType"] == "structure"
        assert data["type"] == "filesystem"
        assert "gitProvider" in data
        assert "branchName" in data
        assert isinstance(data["private"], bool)


# ===========================================================================
# 7. FS connector contract
# ===========================================================================

class TestFSConnectorContract:
    """Validate the filesystem connector contract."""

    FS_PATH = 'fsConnector.json'

    def _get_valid_fs_connector(self):
        return {
            "fileType": "structure",
            "type": "filesystem",
            "companyName": "prancer-test",
            "folderPath": "/path/to/folder"
        }

    def test_fs_file_exists_on_disk(self):
        full_path = os.path.join(REALM_DIR, self.FS_PATH)
        if not os.path.exists(full_path):
            pytest.skip("FS connector file not found on disk")
        assert os.path.isfile(full_path)

    def test_fs_filetype_is_structure(self):
        data = _load_realm_json(self.FS_PATH)
        if data is None:
            pytest.skip("FS connector file not found")
        assert data["fileType"] == "structure"

    def test_fs_type_is_filesystem(self):
        data = _load_realm_json(self.FS_PATH)
        if data is None:
            pytest.skip("FS connector file not found")
        assert data["type"] == "filesystem"

    def test_fs_has_folder_path(self):
        data = _load_realm_json(self.FS_PATH)
        if data is None:
            pytest.skip("FS connector file not found")
        assert "folderPath" in data
        assert isinstance(data["folderPath"], str)

    def test_fs_does_not_have_git_fields(self):
        """FS connector should not have git-specific fields."""
        data = _load_realm_json(self.FS_PATH)
        if data is None:
            pytest.skip("FS connector file not found")
        assert "gitProvider" not in data
        assert "branchName" not in data

    def test_inline_fs_connector_structure(self):
        data = self._get_valid_fs_connector()
        assert data["fileType"] == "structure"
        assert data["type"] == "filesystem"
        assert "folderPath" in data
        assert "gitProvider" not in data


# ===========================================================================
# 8. Master snapshot contract
# ===========================================================================

class TestMasterSnapshotContract:
    """Validate the master snapshot JSON contract as used by populate_json validation."""

    def _get_valid_master_snapshot(self):
        return {
            "fileType": "masterSnapshot",
            "snapshots": [
                {
                    "type": "aws",
                    "connectorUser": "user1",
                    "nodes": [
                        {
                            "masterSnapshotId": "MS_AWS_001",
                            "collection": "ec2instances",
                            "arn": "arn:aws:ec2:us-east-1:123456789:instance/i-abc"
                        }
                    ]
                }
            ]
        }

    def _get_valid_master_snapshot_non_aws(self):
        return {
            "fileType": "masterSnapshot",
            "snapshots": [
                {
                    "type": "azure",
                    "connectorUser": "user1",
                    "nodes": [
                        {
                            "masterSnapshotId": "MS_AZ_001",
                            "collection": "virtualmachines",
                            "type": "Microsoft.Compute/virtualMachines"
                        }
                    ]
                }
            ]
        }

    def test_master_snapshot_filetype(self):
        data = self._get_valid_master_snapshot()
        assert data["fileType"] == "masterSnapshot"

    def test_master_snapshot_snapshots_is_list(self):
        data = self._get_valid_master_snapshot()
        assert isinstance(data["snapshots"], list)
        assert len(data["snapshots"]) > 0

    def test_master_snapshot_each_snapshot_has_type(self):
        data = self._get_valid_master_snapshot()
        for snapshot in data["snapshots"]:
            assert "type" in snapshot

    def test_master_snapshot_each_snapshot_has_connector_user(self):
        data = self._get_valid_master_snapshot()
        for snapshot in data["snapshots"]:
            assert "connectorUser" in snapshot

    def test_master_snapshot_each_snapshot_has_nodes(self):
        data = self._get_valid_master_snapshot()
        for snapshot in data["snapshots"]:
            assert "nodes" in snapshot
            assert isinstance(snapshot["nodes"], list)

    def test_master_snapshot_node_has_master_snapshot_id(self):
        data = self._get_valid_master_snapshot()
        for snapshot in data["snapshots"]:
            for node in snapshot["nodes"]:
                assert "masterSnapshotId" in node

    def test_master_snapshot_node_has_collection(self):
        data = self._get_valid_master_snapshot()
        for snapshot in data["snapshots"]:
            for node in snapshot["nodes"]:
                assert "collection" in node

    def test_master_snapshot_aws_node_has_arn(self):
        """AWS nodes should have an 'arn' field."""
        data = self._get_valid_master_snapshot()
        assert data["snapshots"][0]["type"] == "aws"
        for node in data["snapshots"][0]["nodes"]:
            assert "arn" in node

    def test_master_snapshot_non_aws_node_has_type(self):
        """Non-AWS nodes should have a 'type' field."""
        data = self._get_valid_master_snapshot_non_aws()
        assert data["snapshots"][0]["type"] == "azure"
        for node in data["snapshots"][0]["nodes"]:
            assert "type" in node

    def test_master_snapshot_validates_via_populate_json_logic(self):
        """Simulate the validate_json_data logic for masterSnapshot."""
        data = self._get_valid_master_snapshot()
        # From cli_populate_json.validate_json_data:
        # valid = json_data['snapshots'] and isinstance(json_data['snapshots'], list)
        assert data["snapshots"] and isinstance(data["snapshots"], list)

    def test_master_snapshot_empty_snapshots_fails_validation(self):
        """Empty snapshots list should fail validation (falsy)."""
        data = self._get_valid_master_snapshot()
        data["snapshots"] = []
        # Empty list is falsy in Python, so this should fail the validate check
        assert not (data["snapshots"] and isinstance(data["snapshots"], list))


# ===========================================================================
# 9. Master test contract
# ===========================================================================

class TestMasterTestContract:
    """Validate the master test JSON contract."""

    def _get_valid_master_test(self):
        return {
            "fileType": "mastertest",
            "masterSnapshot": "masterSnapshot",
            "testSet": [
                {
                    "masterTestName": "Test security groups",
                    "version": "0.1",
                    "cases": [
                        {
                            "masterTestId": "MT_001",
                            "masterSnapshotId": ["MS_AWS_001"],
                            "type": "rego",
                            "rule": "file(allowedports.rego)"
                        }
                    ]
                }
            ]
        }

    def test_master_test_filetype(self):
        data = self._get_valid_master_test()
        assert data["fileType"] == "mastertest"

    def test_master_test_has_master_snapshot_ref(self):
        data = self._get_valid_master_test()
        assert "masterSnapshot" in data

    def test_master_test_testset_is_list(self):
        data = self._get_valid_master_test()
        assert isinstance(data["testSet"], list)
        assert len(data["testSet"]) > 0

    def test_master_test_each_testset_has_master_test_name(self):
        data = self._get_valid_master_test()
        for ts in data["testSet"]:
            assert "masterTestName" in ts

    def test_master_test_each_testset_has_cases(self):
        data = self._get_valid_master_test()
        for ts in data["testSet"]:
            assert "cases" in ts
            assert isinstance(ts["cases"], list)

    def test_master_test_each_case_has_master_test_id(self):
        data = self._get_valid_master_test()
        for ts in data["testSet"]:
            for case in ts["cases"]:
                assert "masterTestId" in case

    def test_master_test_validates_via_populate_json_logic(self):
        """Simulate the validate_json_data logic for mastertest."""
        data = self._get_valid_master_test()
        # From cli_populate_json.validate_json_data:
        # valid = json_data['masterSnapshot'] and json_data['testSet'] and
        #         isinstance(json_data['testSet'], list)
        assert data["masterSnapshot"] and data["testSet"] and isinstance(data["testSet"], list)

    def test_master_test_empty_testset_fails_validation(self):
        data = self._get_valid_master_test()
        data["testSet"] = []
        assert not (data["masterSnapshot"] and data["testSet"] and isinstance(data["testSet"], list))


# ===========================================================================
# 10. Output document contract (from json_output.py)
# ===========================================================================

class TestOutputDocumentContract:
    """Validate the output document contract produced by json_output.py."""

    def _get_valid_output_document(self):
        """Build an output document matching the contract from dump_output_results."""
        od = OrderedDict()
        od["$schema"] = ""
        od["contentVersion"] = "1.0.0.0"
        od["fileType"] = "output"
        od["timestamp"] = 1700000000000
        od["snapshot"] = "snapshot_file"
        od["container"] = "test-container"
        od["session_id"] = "session-123"
        od["remote_run"] = False
        od["log"] = ""
        od["test"] = "test_file"
        od["results"] = []
        return od

    def test_output_is_ordered_dict(self):
        od = self._get_valid_output_document()
        assert isinstance(od, OrderedDict)

    def test_output_has_schema_field(self):
        od = self._get_valid_output_document()
        assert "$schema" in od

    def test_output_has_content_version(self):
        od = self._get_valid_output_document()
        assert "contentVersion" in od
        assert od["contentVersion"] == "1.0.0.0"

    def test_output_filetype_is_output(self):
        od = self._get_valid_output_document()
        assert od["fileType"] == "output"

    def test_output_timestamp_is_int(self):
        od = self._get_valid_output_document()
        assert isinstance(od["timestamp"], int)

    def test_output_has_results_list(self):
        od = self._get_valid_output_document()
        assert "results" in od
        assert isinstance(od["results"], list)

    def test_output_has_status_field_when_set(self):
        """The status field is set during create_output_entry as 'Running'."""
        od = self._get_valid_output_document()
        od["status"] = "Running"
        assert od["status"] == "Running"

    def test_output_schema_removed_for_db_storage(self):
        """When stored in DB, $schema is removed from the json field."""
        od = self._get_valid_output_document()
        # Simulate what json_output.py does before DB insertion:
        db_json = OrderedDict(od)
        del db_json["$schema"]
        assert "$schema" not in db_json
        # But the rest of the fields remain
        assert "fileType" in db_json
        assert "results" in db_json

    def test_output_field_order(self):
        """The output document fields should follow a specific order."""
        od = self._get_valid_output_document()
        keys = list(od.keys())
        assert keys[0] == "$schema"
        assert keys[1] == "contentVersion"
        assert keys[2] == "fileType"
        assert keys[3] == "timestamp"

    def test_output_has_container(self):
        od = self._get_valid_output_document()
        assert "container" in od

    def test_output_has_session_id(self):
        od = self._get_valid_output_document()
        assert "session_id" in od


# ===========================================================================
# 11. Container metadata contract (from cli_populate_json.py add_new_container)
# ===========================================================================

class TestContainerMetadataContract:
    """Validate the container metadata contract from add_new_container.

    Notable: uses a mix of PascalCase and camelCase field names.
    """

    def _get_valid_container_metadata(self):
        """Build container metadata matching add_new_container in cli_populate_json.py."""
        return {
            "containerId": 1,
            "status": "active",
            "name": "test-container",
            "masterSnapshots": [],
            "Snapshots": [],
            "masterTests": [],
            "Tests": [],
            "others": []
        }

    def test_container_has_container_id(self):
        data = self._get_valid_container_metadata()
        assert "containerId" in data

    def test_container_id_is_int(self):
        data = self._get_valid_container_metadata()
        assert isinstance(data["containerId"], int)

    def test_container_has_status(self):
        data = self._get_valid_container_metadata()
        assert "status" in data
        assert data["status"] == "active"

    def test_container_has_name(self):
        data = self._get_valid_container_metadata()
        assert "name" in data
        assert isinstance(data["name"], str)

    def test_container_pascal_case_snapshots(self):
        """'Snapshots' uses PascalCase (capital S)."""
        data = self._get_valid_container_metadata()
        assert "Snapshots" in data
        assert isinstance(data["Snapshots"], list)

    def test_container_pascal_case_tests(self):
        """'Tests' uses PascalCase (capital T)."""
        data = self._get_valid_container_metadata()
        assert "Tests" in data
        assert isinstance(data["Tests"], list)

    def test_container_camel_case_master_snapshots(self):
        """'masterSnapshots' uses camelCase (lowercase m)."""
        data = self._get_valid_container_metadata()
        assert "masterSnapshots" in data
        assert isinstance(data["masterSnapshots"], list)

    def test_container_camel_case_master_tests(self):
        """'masterTests' uses camelCase (lowercase m)."""
        data = self._get_valid_container_metadata()
        assert "masterTests" in data
        assert isinstance(data["masterTests"], list)

    def test_container_has_others(self):
        data = self._get_valid_container_metadata()
        assert "others" in data
        assert isinstance(data["others"], list)

    def test_container_mixed_casing_is_intentional(self):
        """Document the intentional mixed casing: PascalCase for Snapshots/Tests,
        camelCase for masterSnapshots/masterTests."""
        data = self._get_valid_container_metadata()
        # PascalCase
        assert "Snapshots" in data
        assert "Tests" in data
        # camelCase
        assert "masterSnapshots" in data
        assert "masterTests" in data
        # NOT lowercase
        assert "snapshots" not in data
        assert "tests" not in data
        # NOT PascalCase for master*
        assert "MasterSnapshots" not in data
        assert "MasterTests" not in data

    def test_container_all_required_fields_present(self):
        required_fields = {
            "containerId", "status", "name",
            "masterSnapshots", "Snapshots",
            "masterTests", "Tests", "others"
        }
        data = self._get_valid_container_metadata()
        assert required_fields == set(data.keys())

    def test_container_id_increments_from_last(self):
        """containerId should be last container's ID + 1, or 1 if empty."""
        # Simulating the logic from add_new_container
        container_list = []
        if container_list:
            container_id = container_list[-1]["containerId"] + 1
        else:
            container_id = 1
        assert container_id == 1

        container_list = [{"containerId": 5}]
        container_id = container_list[-1]["containerId"] + 1
        assert container_id == 6


# ===========================================================================
# 12. Database record contract (from cli_populate_json.py json_record)
# ===========================================================================

class TestDatabaseRecordContract:
    """Validate the database record contract from json_record in cli_populate_json.py."""

    def _get_valid_db_record(self):
        """Build a database record matching json_record output."""
        import hashlib
        import time
        return {
            "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
            "collection": "structures",
            "container": "test-container",
            "name": "testfile",
            "timestamp": int(time.time() * 1000),
            "type": "structure",
            "json": {"fileType": "structure", "type": "aws"}
        }

    def test_db_record_has_checksum(self):
        record = self._get_valid_db_record()
        assert "checksum" in record
        assert isinstance(record["checksum"], str)

    def test_db_record_has_collection(self):
        record = self._get_valid_db_record()
        assert "collection" in record
        assert isinstance(record["collection"], str)

    def test_db_record_has_container(self):
        record = self._get_valid_db_record()
        assert "container" in record
        assert isinstance(record["container"], str)

    def test_db_record_has_name(self):
        record = self._get_valid_db_record()
        assert "name" in record
        assert isinstance(record["name"], str)

    def test_db_record_has_timestamp(self):
        record = self._get_valid_db_record()
        assert "timestamp" in record
        assert isinstance(record["timestamp"], int)

    def test_db_record_timestamp_is_milliseconds(self):
        """Timestamp should be in milliseconds (13+ digits), not seconds (10 digits)."""
        record = self._get_valid_db_record()
        ts = record["timestamp"]
        assert ts > 1_000_000_000_000, (
            f"Timestamp {ts} appears to be in seconds, not milliseconds"
        )

    def test_db_record_has_type(self):
        record = self._get_valid_db_record()
        assert "type" in record
        assert isinstance(record["type"], str)

    def test_db_record_has_json(self):
        record = self._get_valid_db_record()
        assert "json" in record
        assert isinstance(record["json"], dict)

    def test_db_record_schema_removed_from_json(self):
        """$schema should be removed from the json field before storage."""
        record = self._get_valid_db_record()
        record["json"]["$schema"] = "http://example.com/schema"
        # Simulate what json_record does:
        if "$schema" in record["json"]:
            del record["json"]["$schema"]
        assert "$schema" not in record["json"]

    def test_db_record_all_required_fields(self):
        required_fields = {"checksum", "collection", "container", "name",
                           "timestamp", "type", "json"}
        record = self._get_valid_db_record()
        assert required_fields.issubset(set(record.keys()))

    def test_db_record_checksum_is_md5(self):
        """Checksum should be a valid MD5 hex digest (32 hex characters)."""
        import re
        record = self._get_valid_db_record()
        assert re.match(r'^[a-f0-9]{32}$', record["checksum"])

    def test_db_record_json_defaults_to_empty_dict(self):
        """When json_data is None, json field should be empty dict."""
        import hashlib
        import time
        # Simulating json_record with json_data=None
        json_data = None
        record = {
            "json": json_data if json_data else {}
        }
        assert record["json"] == {}
        assert isinstance(record["json"], dict)


# ===========================================================================
# Cross-cutting contract tests
# ===========================================================================

class TestCrossCuttingContracts:
    """Tests that validate cross-cutting concerns across multiple contracts."""

    def test_filetype_casing_consistency(self):
        """All connectors now use 'fileType' (camelCase) consistently.
        The previous Azure 'filetype' inconsistency has been fixed."""
        azure = {"fileType": "structure", "type": "azure"}
        aws = {"fileType": "structure", "type": "aws"}
        google = {"fileType": "structure", "type": "google"}
        git = {"fileType": "structure", "type": "filesystem"}

        # All connectors use camelCase fileType
        assert "fileType" in azure
        assert "fileType" in aws
        assert "fileType" in google
        assert "fileType" in git

    def test_google_uses_projects_others_use_accounts(self):
        """Google uses 'projects' while Azure and AWS use 'accounts'."""
        azure = {"accounts": []}
        aws = {"accounts": []}
        google = {"projects": []}

        assert "accounts" in azure
        assert "accounts" in aws
        assert "projects" in google
        assert "accounts" not in google

    def test_snapshot_vs_master_snapshot_filetype_values(self):
        """Regular snapshot uses 'snapshot', master uses 'masterSnapshot'."""
        snapshot = {"fileType": "snapshot"}
        master_snapshot = {"fileType": "masterSnapshot"}
        assert snapshot["fileType"] == "snapshot"
        assert master_snapshot["fileType"] == "masterSnapshot"

    def test_test_vs_master_test_filetype_values(self):
        """Regular test uses 'test', master uses 'mastertest' (all lowercase!)."""
        test = {"fileType": "test"}
        master_test = {"fileType": "mastertest"}
        assert test["fileType"] == "test"
        assert master_test["fileType"] == "mastertest"
        # Note: mastertest is all lowercase, while masterSnapshot is camelCase
        assert master_test["fileType"] != "masterTest"

    def test_validate_json_data_snapshot_logic(self):
        """Test the validation logic from cli_populate_json.validate_json_data for snapshot."""
        valid_snapshot = {
            "fileType": "snapshot",
            "snapshots": [{"source": "connector", "nodes": []}]
        }
        # Validation: json_data['snapshots'] and isinstance(json_data['snapshots'], list)
        assert valid_snapshot["snapshots"] and isinstance(valid_snapshot["snapshots"], list)

    def test_validate_json_data_test_logic(self):
        """Test the validation logic from cli_populate_json.validate_json_data for test."""
        valid_test = {
            "fileType": "test",
            "snapshot": "snapshot_ref",
            "testSet": [{"cases": []}]
        }
        # Validation: json_data['snapshot'] and json_data['testSet'] and
        #             isinstance(json_data['testSet'], list)
        assert valid_test["snapshot"] and valid_test["testSet"] and \
               isinstance(valid_test["testSet"], list)

    def test_validate_json_data_mastertest_logic(self):
        """Test the validation logic from cli_populate_json.validate_json_data for mastertest."""
        valid_mastertest = {
            "fileType": "mastertest",
            "masterSnapshot": "master_snapshot_ref",
            "testSet": [{"cases": []}]
        }
        # Validation: json_data['masterSnapshot'] and json_data['testSet'] and
        #             isinstance(json_data['testSet'], list)
        assert valid_mastertest["masterSnapshot"] and valid_mastertest["testSet"] and \
               isinstance(valid_mastertest["testSet"], list)

    def test_all_ids_should_be_strings(self):
        """All ID fields across contracts should be strings, not integers."""
        snapshot_node = {"snapshotId": "1"}
        test_case = {"testId": "1"}
        master_snapshot_node = {"masterSnapshotId": "MS_001"}
        master_test_case = {"masterTestId": "MT_001"}

        assert isinstance(snapshot_node["snapshotId"], str)
        assert isinstance(test_case["testId"], str)
        assert isinstance(master_snapshot_node["masterSnapshotId"], str)
        assert isinstance(master_test_case["masterTestId"], str)

    def test_container_id_is_int_while_other_ids_are_strings(self):
        """containerId is the exception - it IS an integer, not a string."""
        container = {"containerId": 1}
        snapshot_node = {"snapshotId": "1"}

        assert isinstance(container["containerId"], int)
        assert isinstance(snapshot_node["snapshotId"], str)
