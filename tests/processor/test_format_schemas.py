"""
Comprehensive tests for validating JSON schema/format contracts used by the
cloud-validation-framework.  These formats are critical contracts with
downstream and upstream systems.

No real cloud APIs are called -- every test works with sample data only.
"""

import time
import pytest
from collections import OrderedDict

from processor.helper.json.json_utils import (
    SNAPSHOT,
    MASTERSNAPSHOT,
    MASTERTEST,
    TEST,
    OUTPUT,
    STRUCTURE,
    NOTIFICATIONS,
    EXCLUSIONS,
    collectiontypes,
)
from processor.reporting.json_output import json_record


# ---------------------------------------------------------------------------
# Helpers -- builders for each format
# ---------------------------------------------------------------------------

def _make_aws_connector():
    return {
        "organization": "my-org",
        "type": "aws",
        "fileType": "structure",
        "accounts": [
            {
                "account-name": "prod",
                "account-id": "123456789012",
                "users": [
                    {
                        "name": "deployer",
                        "access-key": "AKIAIOSFODNN7EXAMPLE",
                        "secret-access": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                    }
                ],
            }
        ],
    }


def _make_azure_connector():
    return {
        "filetype": "structure",
        "type": "azure",
        "companyName": "contoso",
        "tenant_id": "aaaabbbb-cccc-dddd-eeee-ffffgggghhhh",
        "accounts": [
            {
                "department": "engineering",
                "subscription": [
                    {"subscription_id": "sub-001"}
                ],
                "users": [
                    {
                        "client_id": "client-001",
                        "client_secret": "s3cret",
                    }
                ],
            }
        ],
    }


def _make_google_connector():
    return {
        "organization": "my-gcp-org",
        "type": "google",
        "fileType": "structure",
        "projects": [
            {"project-id": "my-project-123"}
        ],
        "users": [
            {
                "type": "service_account",
                "private_key": "-----BEGIN RSA PRIVATE KEY-----\nFAKE\n-----END RSA PRIVATE KEY-----\n",
                "client_email": "sa@my-project-123.iam.gserviceaccount.com",
            }
        ],
    }


def _make_filesystem_connector():
    return {
        "fileType": "structure",
        "type": "filesystem",
        "companyName": "acme",
        "folderPath": "/opt/data",
    }


def _make_git_connector():
    return {
        "fileType": "structure",
        "type": "filesystem",
        "companyName": "acme",
        "gitProvider": "https://github.com/acme/repo.git",
        "branchName": "main",
        "private": True,
    }


def _make_private_https_git_connector():
    base = _make_git_connector()
    base.update({
        "httpsUser": "ci-bot",
        "httpsPassword": "tok3n",
    })
    return base


def _make_private_ssh_git_connector():
    base = _make_git_connector()
    base.update({
        "sshKeyfile": "/home/user/.ssh/id_rsa",
        "sshUser": "git",
        "sshHost": "github.com",
    })
    return base


def _make_snapshot():
    return {
        "fileType": "snapshot",
        "snapshots": [
            {
                "source": "awsConnector",
                "nodes": [
                    {
                        "snapshotId": "SNAP001",
                        "type": "aws",
                        "collection": "ec2",
                        "paths": ["/instances"],
                        "path": "/instances",
                    }
                ],
            }
        ],
    }


def _make_master_snapshot():
    return {
        "fileType": "masterSnapshot",
        "snapshots": [
            {
                "type": "aws",
                "source": "awsConnector",
                "nodes": [
                    {
                        "masterSnapshotId": "MSNAP001",
                        "type": "aws",
                        "collection": "ec2",
                        "paths": ["/instances"],
                    }
                ],
            }
        ],
    }


def _make_test():
    return {
        "fileType": "test",
        "snapshot": "snapshot_ec2",
        "testSet": [
            {
                "testName": "Ensure encryption",
                "version": "0.1",
                "cases": [
                    {
                        "testId": "TC001",
                        "rule": "exist({Encrypted}, true)",
                    }
                ],
            }
        ],
    }


def _make_master_test():
    return {
        "fileType": "mastertest",
        "masterSnapshot": "master_snapshot_ec2",
        "testSet": [
            {
                "cases": [
                    {
                        "masterTestId": "MTC001",
                        "snapshotId": ["SNAP001"],
                        "masterSnapshotId": ["MSNAP001"],
                        "type": "aws",
                        "rule": "exist({Encrypted}, true)",
                        "evals": [
                            {"id": "eval1", "eval": "data.Encrypted == true"}
                        ],
                    }
                ]
            }
        ],
    }


def _make_output():
    return OrderedDict([
        ("$schema", ""),
        ("contentVersion", "1.0.0.0"),
        ("fileType", "output"),
        ("timestamp", int(time.time() * 1000)),
        ("snapshot", "snapshot_ec2"),
        ("container", "container1"),
        ("session_id", "sess-abc-123"),
        ("remote_run", False),
        ("log", ""),
        ("test", "test_ec2.json"),
        ("cloud_type", "aws"),
        ("status", "Completed"),
        ("results", [_make_result_object()]),
    ])


def _make_result_object():
    return {
        "eval": "data.Encrypted == true",
        "result": "passed",
        "message": "Encryption is enabled",
        "id": "RES001",
        "remediation_description": "Enable encryption on the resource",
        "remediation_function": "enable_encryption",
        "masterTestId": "MTC001",
        "masterSnapshotId": ["MSNAP001"],
        "snapshotId": ["SNAP001"],
        "type": "aws",
        "rule": "exist({Encrypted}, true)",
        "severity": "High",
        "title": "Encryption Check",
        "description": "Validates that encryption is enabled",
        "tags": [{"cloud": "aws", "service": "ec2"}],
        "status": "enable",
        "snapshots": [_make_snapshot_metadata()],
        "autoRemediate": False,
    }


def _make_snapshot_metadata():
    return {
        "id": "SNAP001",
        "structure": "awsConnector",
        "reference": "ref-001",
        "source": "awsConnector",
        "collection": "ec2",
        "type": "aws",
        "region": "us-east-1",
        "paths": ["/instances"],
        "resourceTypes": ["AWS::EC2::Instance"],
    }


def _make_node_structure(master=False):
    node = {
        "type": "aws",
        "collection": "ec2",
        "paths": ["/instances"],
        "path": "/instances",
    }
    if master:
        node["masterSnapshotId"] = "MSNAP001"
    else:
        node["snapshotId"] = "SNAP001"
    return node


def _make_node_with_optional_fields(master=False):
    node = _make_node_structure(master=master)
    node["validate"] = True
    node["status"] = "active"
    return node


def _make_database_record():
    return {
        "timestamp": int(time.time() * 1000),
        "container": "container1",
        "checksum": "d41d8cd98f00b204e9800998ecf8427e",
        "type": "snapshot",
        "name": "snapshot_ec2.json",
        "collection": "SNAPSHOT",
        "json": {"fileType": "snapshot"},
    }


# ---------------------------------------------------------------------------
# 1. AWS Connector format
# ---------------------------------------------------------------------------

class TestAWSConnectorFormat:

    def test_required_fields_exist(self):
        doc = _make_aws_connector()
        for field in ("organization", "type", "fileType", "accounts"):
            assert field in doc, f"Missing required field: {field}"

    def test_field_types(self):
        doc = _make_aws_connector()
        assert isinstance(doc["organization"], str)
        assert isinstance(doc["type"], str)
        assert isinstance(doc["fileType"], str)
        assert isinstance(doc["accounts"], list)

    def test_type_value(self):
        doc = _make_aws_connector()
        assert doc["type"] == "aws"
        assert doc["fileType"] == "structure"

    def test_account_nested_structure(self):
        acct = _make_aws_connector()["accounts"][0]
        assert "account-name" in acct
        assert "account-id" in acct
        assert isinstance(acct["users"], list)
        user = acct["users"][0]
        assert "name" in user
        assert "access-key" in user
        assert "secret-access" in user


# ---------------------------------------------------------------------------
# 2. Azure Connector format
# ---------------------------------------------------------------------------

class TestAzureConnectorFormat:

    def test_required_fields_exist(self):
        doc = _make_azure_connector()
        for field in ("filetype", "type", "companyName", "tenant_id", "accounts"):
            assert field in doc, f"Missing required field: {field}"

    def test_field_types(self):
        doc = _make_azure_connector()
        assert isinstance(doc["companyName"], str)
        assert isinstance(doc["tenant_id"], str)
        assert isinstance(doc["accounts"], list)

    def test_type_value(self):
        doc = _make_azure_connector()
        assert doc["type"] == "azure"
        assert doc["filetype"] == "structure"

    def test_account_nested_structure(self):
        acct = _make_azure_connector()["accounts"][0]
        assert "department" in acct
        assert isinstance(acct["subscription"], list)
        assert "subscription_id" in acct["subscription"][0]
        user = acct["users"][0]
        assert "client_id" in user
        assert "client_secret" in user


# ---------------------------------------------------------------------------
# 3. Google Connector format
# ---------------------------------------------------------------------------

class TestGoogleConnectorFormat:

    def test_required_fields_exist(self):
        doc = _make_google_connector()
        for field in ("organization", "type", "fileType", "projects", "users"):
            assert field in doc, f"Missing required field: {field}"

    def test_field_types(self):
        doc = _make_google_connector()
        assert isinstance(doc["projects"], list)
        assert isinstance(doc["users"], list)

    def test_type_and_enum_values(self):
        doc = _make_google_connector()
        assert doc["type"] == "google"
        assert doc["fileType"] == "structure"
        assert doc["users"][0]["type"] == "service_account"

    def test_nested_structure(self):
        doc = _make_google_connector()
        assert "project-id" in doc["projects"][0]
        user = doc["users"][0]
        assert "private_key" in user
        assert "client_email" in user


# ---------------------------------------------------------------------------
# 4. Filesystem Connector format
# ---------------------------------------------------------------------------

class TestFilesystemConnectorFormat:

    def test_required_fields_exist(self):
        doc = _make_filesystem_connector()
        for field in ("fileType", "type", "companyName", "folderPath"):
            assert field in doc

    def test_field_types(self):
        doc = _make_filesystem_connector()
        assert isinstance(doc["folderPath"], str)
        assert isinstance(doc["companyName"], str)

    def test_type_value(self):
        doc = _make_filesystem_connector()
        assert doc["type"] == "filesystem"
        assert doc["fileType"] == "structure"


# ---------------------------------------------------------------------------
# 5. Git Connector formats (public, https-private, ssh-private)
# ---------------------------------------------------------------------------

class TestGitConnectorFormat:

    def test_git_required_fields(self):
        doc = _make_git_connector()
        for field in ("fileType", "type", "companyName", "gitProvider",
                       "branchName", "private"):
            assert field in doc

    def test_git_field_types(self):
        doc = _make_git_connector()
        assert isinstance(doc["gitProvider"], str)
        assert isinstance(doc["branchName"], str)
        assert isinstance(doc["private"], bool)

    def test_private_https_extra_fields(self):
        doc = _make_private_https_git_connector()
        assert "httpsUser" in doc
        assert "httpsPassword" in doc
        assert isinstance(doc["httpsUser"], str)
        assert isinstance(doc["httpsPassword"], str)

    def test_private_ssh_extra_fields(self):
        doc = _make_private_ssh_git_connector()
        for field in ("sshKeyfile", "sshUser", "sshHost"):
            assert field in doc
            assert isinstance(doc[field], str)


# ---------------------------------------------------------------------------
# 6. Snapshot format
# ---------------------------------------------------------------------------

class TestSnapshotFormat:

    def test_required_fields(self):
        doc = _make_snapshot()
        assert doc["fileType"] == "snapshot"
        assert isinstance(doc["snapshots"], list)

    def test_snapshot_entry_structure(self):
        entry = _make_snapshot()["snapshots"][0]
        assert "source" in entry
        assert isinstance(entry["source"], str)
        assert isinstance(entry["nodes"], list)

    def test_node_structure(self):
        node = _make_snapshot()["snapshots"][0]["nodes"][0]
        assert "snapshotId" in node
        assert "type" in node
        assert "collection" in node
        assert "paths" in node or "path" in node
        assert isinstance(node["snapshotId"], str)
        assert isinstance(node["collection"], str)


# ---------------------------------------------------------------------------
# 7. Master Snapshot format
# ---------------------------------------------------------------------------

class TestMasterSnapshotFormat:

    def test_required_fields(self):
        doc = _make_master_snapshot()
        assert doc["fileType"] == "masterSnapshot"
        assert isinstance(doc["snapshots"], list)

    def test_snapshot_entry_fields(self):
        entry = _make_master_snapshot()["snapshots"][0]
        assert "type" in entry
        assert "source" in entry

    def test_master_node_structure(self):
        node = _make_master_snapshot()["snapshots"][0]["nodes"][0]
        assert "masterSnapshotId" in node
        assert "type" in node
        assert "collection" in node
        assert "paths" in node
        assert isinstance(node["masterSnapshotId"], str)
        assert isinstance(node["paths"], list)


# ---------------------------------------------------------------------------
# 8. Test format
# ---------------------------------------------------------------------------

class TestTestFormat:

    def test_required_fields(self):
        doc = _make_test()
        assert doc["fileType"] == "test"
        assert isinstance(doc["snapshot"], str)
        assert isinstance(doc["testSet"], list)

    def test_testset_structure(self):
        ts = _make_test()["testSet"][0]
        assert "testName" in ts
        assert "version" in ts
        assert isinstance(ts["cases"], list)

    def test_case_structure(self):
        case = _make_test()["testSet"][0]["cases"][0]
        assert "testId" in case
        assert "rule" in case
        assert isinstance(case["testId"], str)
        assert isinstance(case["rule"], str)


# ---------------------------------------------------------------------------
# 9. Master Test format
# ---------------------------------------------------------------------------

class TestMasterTestFormat:

    def test_required_fields(self):
        doc = _make_master_test()
        assert doc["fileType"] == "mastertest"
        assert isinstance(doc["masterSnapshot"], str)
        assert isinstance(doc["testSet"], list)

    def test_case_fields(self):
        case = _make_master_test()["testSet"][0]["cases"][0]
        for field in ("masterTestId", "snapshotId", "masterSnapshotId",
                       "type", "rule"):
            assert field in case, f"Missing: {field}"

    def test_case_field_types(self):
        case = _make_master_test()["testSet"][0]["cases"][0]
        assert isinstance(case["masterTestId"], str)
        assert isinstance(case["snapshotId"], list)
        assert isinstance(case["masterSnapshotId"], list)
        assert isinstance(case["rule"], str)

    def test_evals_structure(self):
        case = _make_master_test()["testSet"][0]["cases"][0]
        assert "evals" in case or "eval" in case
        if "evals" in case:
            assert isinstance(case["evals"], list)
            assert "id" in case["evals"][0]
            assert "eval" in case["evals"][0]


# ---------------------------------------------------------------------------
# 10. Output format
# ---------------------------------------------------------------------------

class TestOutputFormat:

    def test_required_fields(self):
        doc = _make_output()
        required = (
            "$schema", "contentVersion", "fileType", "timestamp",
            "snapshot", "container", "session_id", "remote_run",
            "log", "test", "cloud_type", "status", "results",
        )
        for field in required:
            assert field in doc, f"Missing: {field}"

    def test_field_types(self):
        doc = _make_output()
        assert isinstance(doc["contentVersion"], str)
        assert isinstance(doc["timestamp"], int)
        assert isinstance(doc["remote_run"], bool)
        assert isinstance(doc["results"], list)

    def test_enum_values(self):
        doc = _make_output()
        assert doc["contentVersion"] == "1.0.0.0"
        assert doc["fileType"] == "output"


# ---------------------------------------------------------------------------
# 11. Result object within output
# ---------------------------------------------------------------------------

class TestResultObjectFormat:

    def test_required_fields(self):
        res = _make_result_object()
        required = (
            "eval", "result", "message", "id",
            "remediation_description", "remediation_function",
            "masterTestId", "masterSnapshotId", "snapshotId",
            "type", "rule", "severity", "title", "description",
            "tags", "status", "snapshots", "autoRemediate",
        )
        for field in required:
            assert field in res, f"Missing: {field}"

    def test_field_types(self):
        res = _make_result_object()
        assert isinstance(res["eval"], str)
        assert isinstance(res["result"], str)
        assert isinstance(res["masterSnapshotId"], list)
        assert isinstance(res["snapshotId"], list)
        assert isinstance(res["tags"], list)
        assert isinstance(res["snapshots"], list)
        assert isinstance(res["autoRemediate"], bool)

    def test_result_enum(self):
        res = _make_result_object()
        assert res["result"] in ("passed", "failed", "skipped")

    def test_severity_enum(self):
        res = _make_result_object()
        assert res["severity"] in ("Low", "Medium", "High")

    def test_status_enum(self):
        res = _make_result_object()
        assert res["status"] in ("enable", "disable")


# ---------------------------------------------------------------------------
# 12. Snapshot metadata in result
# ---------------------------------------------------------------------------

class TestSnapshotMetadataFormat:

    def test_required_fields(self):
        meta = _make_snapshot_metadata()
        required = (
            "id", "structure", "reference", "source",
            "collection", "type", "region", "paths", "resourceTypes",
        )
        for field in required:
            assert field in meta, f"Missing: {field}"

    def test_field_types(self):
        meta = _make_snapshot_metadata()
        assert isinstance(meta["id"], str)
        assert isinstance(meta["paths"], list)
        assert isinstance(meta["resourceTypes"], list)
        assert isinstance(meta["region"], str)


# ---------------------------------------------------------------------------
# 13. Database record wrapper
# ---------------------------------------------------------------------------

class TestDatabaseRecordFormat:

    def test_required_fields(self):
        rec = _make_database_record()
        for field in ("timestamp", "container", "checksum", "type",
                       "name", "collection", "json"):
            assert field in rec, f"Missing: {field}"

    def test_field_types(self):
        rec = _make_database_record()
        assert isinstance(rec["timestamp"], int)
        assert isinstance(rec["container"], str)
        assert isinstance(rec["checksum"], str)
        assert isinstance(rec["type"], str)
        assert isinstance(rec["name"], str)
        assert isinstance(rec["collection"], str)
        assert isinstance(rec["json"], dict)


# ---------------------------------------------------------------------------
# 14. collectiontypes mapping
# ---------------------------------------------------------------------------

class TestCollectionTypesMapping:

    def test_expected_keys_exist(self):
        expected_keys = {TEST, STRUCTURE, SNAPSHOT, MASTERSNAPSHOT,
                         MASTERTEST, OUTPUT, NOTIFICATIONS, EXCLUSIONS}
        assert expected_keys.issubset(set(collectiontypes.keys()))

    def test_expected_values(self):
        assert collectiontypes[TEST] == "TEST"
        assert collectiontypes[STRUCTURE] == "STRUCTURE"
        assert collectiontypes[SNAPSHOT] == "SNAPSHOT"
        assert collectiontypes[MASTERSNAPSHOT] == "MASTERSNAPSHOT"
        assert collectiontypes[MASTERTEST] == "MASTERTEST"
        assert collectiontypes[OUTPUT] == "OUTPUT"
        assert collectiontypes[NOTIFICATIONS] == "NOTIFICATIONS"
        assert collectiontypes[EXCLUSIONS] == "EXCLUSIONS"

    def test_constant_string_values(self):
        """Verify the raw constant values haven't shifted."""
        assert SNAPSHOT == "snapshot"
        assert MASTERSNAPSHOT == "masterSnapshot"
        assert TEST == "test"
        assert MASTERTEST == "mastertest"
        assert OUTPUT == "output"
        assert STRUCTURE == "structure"
        assert NOTIFICATIONS == "notifications"
        assert EXCLUSIONS == "exclusions"


# ---------------------------------------------------------------------------
# 15. Node structure
# ---------------------------------------------------------------------------

class TestNodeStructure:

    def test_snapshot_node_has_snapshotId(self):
        node = _make_node_structure(master=False)
        assert "snapshotId" in node
        assert "masterSnapshotId" not in node

    def test_master_node_has_masterSnapshotId(self):
        node = _make_node_structure(master=True)
        assert "masterSnapshotId" in node
        assert "snapshotId" not in node

    def test_common_fields(self):
        for master in (True, False):
            node = _make_node_structure(master=master)
            assert "type" in node
            assert "collection" in node
            assert "paths" in node or "path" in node

    def test_optional_validate_field(self):
        node = _make_node_with_optional_fields()
        assert isinstance(node["validate"], bool)

    def test_optional_status_field(self):
        node = _make_node_with_optional_fields()
        assert "status" in node
        assert isinstance(node["status"], str)


# ---------------------------------------------------------------------------
# 16. json_record() from processor.reporting.json_output
# ---------------------------------------------------------------------------

class TestJsonRecordFunction:

    def test_json_record_returns_expected_keys(self, monkeypatch):
        monkeypatch.setattr(
            "processor.reporting.json_output.config_value",
            lambda *a, **kw: "outputs",
        )
        rec = json_record("mycontainer", OUTPUT, "test_file.json")
        for field in ("timestamp", "container", "checksum", "type",
                       "name", "collection", "json"):
            assert field in rec, f"Missing: {field}"

    def test_json_record_field_types(self, monkeypatch):
        monkeypatch.setattr(
            "processor.reporting.json_output.config_value",
            lambda *a, **kw: "outputs",
        )
        rec = json_record("c1", OUTPUT, "f.json", {"key": "val"})
        assert isinstance(rec["timestamp"], int)
        assert isinstance(rec["checksum"], str)
        assert isinstance(rec["json"], dict)
        assert isinstance(rec["container"], str)

    def test_json_record_default_json_is_empty_dict(self, monkeypatch):
        monkeypatch.setattr(
            "processor.reporting.json_output.config_value",
            lambda *a, **kw: "outputs",
        )
        rec = json_record("c1", OUTPUT, "f.json")
        assert rec["json"] == {}

    def test_json_record_strips_dollar_schema(self, monkeypatch):
        monkeypatch.setattr(
            "processor.reporting.json_output.config_value",
            lambda *a, **kw: "outputs",
        )
        rec = json_record("c1", OUTPUT, "f.json", {"$schema": "http://x", "a": 1})
        assert "$schema" not in rec["json"]
        assert rec["json"]["a"] == 1

    def test_json_record_container_passthrough(self, monkeypatch):
        monkeypatch.setattr(
            "processor.reporting.json_output.config_value",
            lambda *a, **kw: "outputs",
        )
        rec = json_record("my-container", OUTPUT, "out.json")
        assert rec["container"] == "my-container"
        assert rec["name"] == "out.json"
        assert rec["type"] == OUTPUT

    def test_json_record_collection_uses_collectiontype(self, monkeypatch):
        monkeypatch.setattr(
            "processor.reporting.json_output.config_value",
            lambda *a, **kw: "outputs",
        )
        rec = json_record("c1", OUTPUT, "f.json")
        assert rec["collection"] == "outputs"


# ---------------------------------------------------------------------------
# 17. Cross-format consistency checks
# ---------------------------------------------------------------------------

class TestCrossFormatConsistency:

    def test_output_results_contain_valid_result_objects(self):
        output = _make_output()
        for res in output["results"]:
            assert res["result"] in ("passed", "failed", "skipped")
            assert res["severity"] in ("Low", "Medium", "High")

    def test_result_snapshots_match_metadata_schema(self):
        res = _make_result_object()
        for meta in res["snapshots"]:
            assert "id" in meta
            assert "collection" in meta
            assert "paths" in meta
            assert isinstance(meta["paths"], list)

    def test_master_test_references_master_snapshot_ids(self):
        mt = _make_master_test()
        case = mt["testSet"][0]["cases"][0]
        ms = _make_master_snapshot()
        ms_ids = [n["masterSnapshotId"]
                  for s in ms["snapshots"] for n in s["nodes"]]
        for ref in case["masterSnapshotId"]:
            assert ref in ms_ids

    def test_snapshot_node_ids_referenced_in_test(self):
        snap = _make_snapshot()
        snap_ids = [n["snapshotId"]
                    for s in snap["snapshots"] for n in s["nodes"]]
        mt = _make_master_test()
        case = mt["testSet"][0]["cases"][0]
        for ref in case["snapshotId"]:
            assert ref in snap_ids
