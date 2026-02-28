"""
Comprehensive tests for template processor detection logic and output formats.

These tests protect the IaC parsing pipeline from regressions by verifying:
- TEMPLATE_NODE_TYPES registry completeness and correctness
- AWS CloudFormation template/parameter file detection
- Azure ARM template/parameter file detection
- Google Deployment Manager template file detection
- Terraform template/parameter file detection
- Kubernetes manifest file detection
- Template processor output record structure
- Collection name normalization
- Sensitive file detection
"""

import json
import os
import hashlib
import tempfile
import time

import pytest
from unittest.mock import patch, MagicMock

# ---------------------------------------------------------------------------
# TEMPLATE_NODE_TYPES registry
# ---------------------------------------------------------------------------
from processor.template_processor.base.base_template_constatns import TEMPLATE_NODE_TYPES
from processor.template_processor.aws_template_processor import AWSTemplateProcessor
from processor.template_processor.azure_template_processor import AzureTemplateProcessor
from processor.template_processor.google_template_processor import GoogleTemplateProcessor
from processor.template_processor.terraform_template_processor import TerraformTemplateProcessor
from processor.template_processor.kubernetes_template_processor import KubernetesTemplateProcessor
from processor.template_processor.yaml_template_processor import YamlTemplateProcessor
from processor.template_processor.json_template_processor import JsonTemplateProcessor
from processor.template_processor.helm_chart_template_processor import HelmChartTemplateProcessor
from processor.template_processor.ack_processor import AckTemplateProcessor
from processor.template_processor.aso_processor import AsoTemplateProcessor
from processor.template_processor.kcc_processor import KccTemplateProcessor
from processor.template_processor.base.base_template_processor import TemplateProcessor


# ===================================================================
# Helper: minimal node dict for constructing processors
# ===================================================================

def _minimal_node(**overrides):
    node = {
        "snapshotId": "SNAP001",
        "type": "cloudformation",
        "collection": "test_collection",
        "paths": [],
        "masterSnapshotId": "MASTER001",
        "status": "active",
    }
    node.update(overrides)
    return node


def _base_kwargs(**overrides):
    kw = {
        "container": "test_container",
        "dbname": "test_db",
        "snapshot_source": "source_file.json",
        "connector_data": {"type": "filesystem", "branchName": "master"},
        "snapshot_data": {},
        "repopath": "/tmp/repo",
        "snapshot": {},
    }
    kw.update(overrides)
    return kw


# ===================================================================
# 1. TEMPLATE_NODE_TYPES registry tests
# ===================================================================

class TestTemplateNodeTypesRegistry:
    """Verify the TEMPLATE_NODE_TYPES mapping is correct and complete."""

    EXPECTED_KEYS = {
        "cloudformation",
        "arm",
        "deploymentmanager",
        "terraform",
        "kubernetesObjectFiles",
        "yaml",
        "json",
        "helmChart",
        "ack",
        "aso",
        "kcc",
        "common",
    }

    def test_registry_has_exactly_12_keys(self):
        assert len(TEMPLATE_NODE_TYPES) == 12

    def test_registry_contains_all_expected_keys(self):
        assert set(TEMPLATE_NODE_TYPES.keys()) == self.EXPECTED_KEYS

    def test_no_extra_keys_in_registry(self):
        extra = set(TEMPLATE_NODE_TYPES.keys()) - self.EXPECTED_KEYS
        assert extra == set(), f"Unexpected keys in registry: {extra}"

    def test_cloudformation_maps_to_aws_processor(self):
        assert TEMPLATE_NODE_TYPES["cloudformation"] is AWSTemplateProcessor

    def test_arm_maps_to_azure_processor(self):
        assert TEMPLATE_NODE_TYPES["arm"] is AzureTemplateProcessor

    def test_deploymentmanager_maps_to_google_processor(self):
        assert TEMPLATE_NODE_TYPES["deploymentmanager"] is GoogleTemplateProcessor

    def test_terraform_maps_to_terraform_processor(self):
        assert TEMPLATE_NODE_TYPES["terraform"] is TerraformTemplateProcessor

    def test_kubernetes_maps_to_kubernetes_processor(self):
        assert TEMPLATE_NODE_TYPES["kubernetesObjectFiles"] is KubernetesTemplateProcessor

    def test_yaml_maps_to_yaml_processor(self):
        assert TEMPLATE_NODE_TYPES["yaml"] is YamlTemplateProcessor

    def test_json_maps_to_json_processor(self):
        assert TEMPLATE_NODE_TYPES["json"] is JsonTemplateProcessor

    def test_helmchart_maps_to_helm_processor(self):
        assert TEMPLATE_NODE_TYPES["helmChart"] is HelmChartTemplateProcessor

    def test_ack_maps_to_ack_processor(self):
        assert TEMPLATE_NODE_TYPES["ack"] is AckTemplateProcessor

    def test_aso_maps_to_aso_processor(self):
        assert TEMPLATE_NODE_TYPES["aso"] is AsoTemplateProcessor

    def test_kcc_maps_to_kcc_processor(self):
        assert TEMPLATE_NODE_TYPES["kcc"] is KccTemplateProcessor

    def test_common_maps_to_base_template_processor(self):
        assert TEMPLATE_NODE_TYPES["common"] is TemplateProcessor


# ===================================================================
# 2. AWS Template Processor detection
# ===================================================================

class TestAWSTemplateDetection:
    """Tests for AWSTemplateProcessor.is_template_file and is_parameter_file."""

    @pytest.fixture()
    def processor(self):
        node = _minimal_node(type="cloudformation")
        return AWSTemplateProcessor(node, **_base_kwargs())

    def test_json_with_aws_template_format_version_is_template(self, processor, tmp_path):
        data = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Resources": {"MyBucket": {"Type": "AWS::S3::Bucket"}},
        }
        fpath = tmp_path / "template.json"
        fpath.write_text(json.dumps(data))
        assert processor.is_template_file(str(fpath)) is True

    def test_json_without_aws_format_version_is_not_template(self, processor, tmp_path):
        data = {"Resources": {"MyBucket": {"Type": "AWS::S3::Bucket"}}}
        fpath = tmp_path / "no_version.json"
        fpath.write_text(json.dumps(data))
        assert processor.is_template_file(str(fpath)) is False

    def test_non_json_extension_is_not_template(self, processor, tmp_path):
        data = {"AWSTemplateFormatVersion": "2010-09-09", "Resources": {}}
        fpath = tmp_path / "template.py"
        fpath.write_text(json.dumps(data))
        assert processor.is_template_file(str(fpath)) is False

    def test_parameter_file_with_valid_structure(self, processor, tmp_path):
        data = [{"ParameterKey": "Env", "ParameterValue": "prod"}]
        fpath = tmp_path / "params.json"
        fpath.write_text(json.dumps(data))
        assert processor.is_parameter_file(str(fpath)) is True

    def test_parameter_file_missing_parameter_key(self, processor, tmp_path):
        data = [{"SomeKey": "Env", "ParameterValue": "prod"}]
        fpath = tmp_path / "params.json"
        fpath.write_text(json.dumps(data))
        assert processor.is_parameter_file(str(fpath)) is False

    def test_parameter_file_not_a_list(self, processor, tmp_path):
        data = {"ParameterKey": "Env", "ParameterValue": "prod"}
        fpath = tmp_path / "params.json"
        fpath.write_text(json.dumps(data))
        assert processor.is_parameter_file(str(fpath)) is False

    def test_template_extension_file_with_aws_format_version(self, processor, tmp_path):
        data = {"AWSTemplateFormatVersion": "2010-09-09", "Resources": {}}
        fpath = tmp_path / "stack.template"
        fpath.write_text(json.dumps(data))
        assert processor.is_template_file(str(fpath)) is True


# ===================================================================
# 3. Azure Template Processor detection
# ===================================================================

class TestAzureTemplateDetection:
    """Tests for AzureTemplateProcessor.is_template_file and is_parameter_file."""

    @pytest.fixture()
    def processor(self):
        node = _minimal_node(type="arm")
        return AzureTemplateProcessor(node, **_base_kwargs())

    def test_deployment_template_schema_is_template(self, processor, tmp_path):
        data = {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
            "contentVersion": "1.0.0.0",
            "resources": [],
        }
        fpath = tmp_path / "template.json"
        fpath.write_text(json.dumps(data))
        assert processor.is_template_file(str(fpath)) is True

    def test_deployment_parameters_schema_is_parameter_file(self, processor, tmp_path):
        data = {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {},
        }
        fpath = tmp_path / "params.json"
        fpath.write_text(json.dumps(data))
        assert processor.is_parameter_file(str(fpath)) is True

    def test_template_schema_is_not_parameter_file(self, processor, tmp_path):
        data = {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
            "contentVersion": "1.0.0.0",
            "resources": [],
        }
        fpath = tmp_path / "template.json"
        fpath.write_text(json.dumps(data))
        assert processor.is_parameter_file(str(fpath)) is False

    def test_parameter_schema_is_not_template_file(self, processor, tmp_path):
        data = {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {},
        }
        fpath = tmp_path / "params.json"
        fpath.write_text(json.dumps(data))
        assert processor.is_template_file(str(fpath)) is False

    def test_json_without_schema_is_not_template(self, processor, tmp_path):
        data = {"resources": []}
        fpath = tmp_path / "no_schema.json"
        fpath.write_text(json.dumps(data))
        assert processor.is_template_file(str(fpath)) is False

    def test_non_json_extension_is_not_template(self, processor, tmp_path):
        data = {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        }
        fpath = tmp_path / "template.yaml"
        fpath.write_text(json.dumps(data))
        assert processor.is_template_file(str(fpath)) is False


# ===================================================================
# 4. Google Template Processor detection
# ===================================================================

class TestGoogleTemplateDetection:
    """Tests for GoogleTemplateProcessor.is_template_file."""

    @pytest.fixture()
    def processor(self):
        node = _minimal_node(type="deploymentmanager")
        return GoogleTemplateProcessor(node, **_base_kwargs())

    def test_yaml_with_resources_key_is_template(self, processor, tmp_path):
        content = "resources:\n  - name: my-vm\n    type: compute.v1.instance\n"
        fpath = tmp_path / "config.yaml"
        fpath.write_text(content)
        assert processor.is_template_file(str(fpath)) is True

    def test_yaml_without_resources_key_is_not_template(self, processor, tmp_path):
        content = "imports:\n  - path: vm.jinja\n"
        fpath = tmp_path / "config.yaml"
        fpath.write_text(content)
        assert processor.is_template_file(str(fpath)) is False

    def test_non_yaml_extension_is_not_template(self, processor, tmp_path):
        content = '{"resources": []}'
        fpath = tmp_path / "config.json"
        fpath.write_text(content)
        assert processor.is_template_file(str(fpath)) is False


# ===================================================================
# 5. Terraform Template Processor detection
# ===================================================================

class TestTerraformTemplateDetection:
    """Tests for TerraformTemplateProcessor.is_template_file and is_parameter_file."""

    @pytest.fixture()
    def processor(self):
        node = _minimal_node(type="terraform")
        return TerraformTemplateProcessor(node, **_base_kwargs())

    def test_tf_file_with_resource_block_is_template(self, processor, tmp_path):
        """A .tf file containing a 'resource' key should be detected as template."""
        fpath = tmp_path / "main.tf"
        fpath.write_text('resource "aws_instance" "web" {\n  ami = "abc-123"\n}\n')
        with patch("processor.template_processor.terraform_template_processor.hcl_to_json") as mock_hcl:
            mock_hcl.return_value = {"resource": {"aws_instance": {"web": {"ami": "abc-123"}}}}
            assert processor.is_template_file(str(fpath)) is True

    def test_tf_file_with_module_block_is_template(self, processor, tmp_path):
        """A .tf file containing a 'module' key should be detected as template."""
        fpath = tmp_path / "modules.tf"
        fpath.write_text('module "vpc" {\n  source = "./vpc"\n}\n')
        with patch("processor.template_processor.terraform_template_processor.hcl_to_json") as mock_hcl:
            mock_hcl.return_value = {"module": {"vpc": {"source": "./vpc"}}}
            assert processor.is_template_file(str(fpath)) is True

    def test_tf_file_with_only_variable_is_not_template(self, processor, tmp_path):
        """A .tf file with only 'variable' should NOT be a template file."""
        fpath = tmp_path / "variables.tf"
        fpath.write_text('variable "region" {\n  default = "us-east-1"\n}\n')
        with patch("processor.template_processor.terraform_template_processor.hcl_to_json") as mock_hcl:
            mock_hcl.return_value = {"variable": {"region": {"default": "us-east-1"}}}
            assert processor.is_template_file(str(fpath)) is False

    def test_tf_variable_file_is_parameter_file(self, processor, tmp_path):
        """A .tf file with only variables and no resources should be a parameter file."""
        fpath = tmp_path / "variables.tf"
        fpath.write_text('variable "region" {\n  default = "us-east-1"\n}\n')
        with patch("processor.template_processor.terraform_template_processor.hcl_to_json") as mock_hcl:
            mock_hcl.return_value = {"variable": {"region": {"default": "us-east-1"}}}
            assert processor.is_parameter_file(str(fpath)) is True

    def test_tfvars_file_is_parameter_file(self, processor, tmp_path):
        """A .tfvars file should be detected as a parameter file."""
        fpath = tmp_path / "terraform.tfvars"
        fpath.write_text('region = "us-east-1"\n')
        with patch("processor.template_processor.terraform_template_processor.hcl_to_json") as mock_hcl:
            mock_hcl.return_value = {"region": "us-east-1"}
            assert processor.is_parameter_file(str(fpath)) is True

    def test_json_file_with_resource_is_template(self, processor, tmp_path):
        """A .json file containing 'resource' key should be detected as template."""
        data = {"resource": {"aws_instance": {"web": {"ami": "abc-123"}}}}
        fpath = tmp_path / "main.tf.json"
        fpath.write_text(json.dumps(data))
        with patch("processor.template_processor.terraform_template_processor.json_from_file") as mock_json:
            mock_json.return_value = data
            assert processor.is_template_file(str(fpath)) is True

    def test_non_tf_non_json_extension_is_not_template(self, processor, tmp_path):
        """A file with non-terraform extension should not be detected."""
        fpath = tmp_path / "main.py"
        fpath.write_text('resource = "something"')
        assert processor.is_template_file(str(fpath)) is False


# ===================================================================
# 6. Kubernetes Template Processor detection
# ===================================================================

class TestKubernetesTemplateDetection:
    """Tests for KubernetesTemplateProcessor.is_template_file."""

    @pytest.fixture()
    def processor(self):
        node = _minimal_node(type="kubernetesObjectFiles")
        return KubernetesTemplateProcessor(node, **_base_kwargs())

    def test_yaml_with_apiversion_and_kind_is_template(self, processor, tmp_path):
        content = "apiVersion: v1\nkind: Pod\nmetadata:\n  name: my-pod\nspec:\n  containers: []\n"
        fpath = tmp_path / "pod.yaml"
        fpath.write_text(content)
        assert processor.is_template_file(str(fpath)) is True

    def test_yaml_with_only_kind_is_template(self, processor, tmp_path):
        """Kubernetes detection uses 'any' -- having just 'kind' should suffice."""
        content = "kind: Service\n"
        fpath = tmp_path / "svc.yaml"
        fpath.write_text(content)
        assert processor.is_template_file(str(fpath)) is True

    def test_yaml_without_kube_keys_is_not_template(self, processor, tmp_path):
        content = "name: something\nvalue: 42\n"
        fpath = tmp_path / "random.yaml"
        fpath.write_text(content)
        assert processor.is_template_file(str(fpath)) is False

    def test_non_yaml_extension_is_not_template(self, processor, tmp_path):
        content = '{"apiVersion": "v1", "kind": "Pod"}'
        fpath = tmp_path / "pod.json"
        fpath.write_text(content)
        assert processor.is_template_file(str(fpath)) is False


# ===================================================================
# 7. Template processor output record structure
# ===================================================================

class TestDatabaseRecordStructure:
    """Verify the structure returned by TemplateProcessor.create_database_record."""

    @patch("processor.template_processor.base.base_template_processor.get_from_currentdata")
    def test_record_contains_all_required_keys(self, mock_get_current):
        mock_get_current.return_value = "session-abc-123"
        node = _minimal_node(paths=["template.json"])
        kwargs = _base_kwargs()
        proc = TemplateProcessor(node, **kwargs)
        proc.processed_template = {"key": "value"}

        record = proc.create_database_record()

        expected_keys = {
            "structure", "error", "reference", "contentType", "source",
            "paths", "timestamp", "queryuser", "checksum", "node",
            "snapshotId", "collection", "container", "json", "session_id",
        }
        assert expected_keys.issubset(set(record.keys()))

    @patch("processor.template_processor.base.base_template_processor.get_from_currentdata")
    def test_record_structure_field_is_connector_type(self, mock_get_current):
        mock_get_current.return_value = "session-abc-123"
        node = _minimal_node(paths=["t.json"])
        kwargs = _base_kwargs(connector_data={"type": "git", "branchName": "main"})
        proc = TemplateProcessor(node, **kwargs)
        proc.processed_template = {}

        record = proc.create_database_record()
        assert record["structure"] == "git"

    @patch("processor.template_processor.base.base_template_processor.get_from_currentdata")
    def test_record_reference_is_branch_name(self, mock_get_current):
        mock_get_current.return_value = "sess"
        node = _minimal_node(paths=["t.json"])
        kwargs = _base_kwargs(connector_data={"type": "git", "branchName": "develop"})
        proc = TemplateProcessor(node, **kwargs)
        proc.processed_template = {}

        record = proc.create_database_record()
        assert record["reference"] == "develop"

    @patch("processor.template_processor.base.base_template_processor.get_from_currentdata")
    def test_record_timestamp_is_milliseconds(self, mock_get_current):
        mock_get_current.return_value = "sess"
        node = _minimal_node(paths=["t.json"])
        proc = TemplateProcessor(node, **_base_kwargs())
        proc.processed_template = {}

        before = int(time.time() * 1000)
        record = proc.create_database_record()
        after = int(time.time() * 1000)

        assert before <= record["timestamp"] <= after

    @patch("processor.template_processor.base.base_template_processor.get_from_currentdata")
    def test_record_checksum_is_md5_hex(self, mock_get_current):
        mock_get_current.return_value = "sess"
        node = _minimal_node(paths=["t.json"])
        proc = TemplateProcessor(node, **_base_kwargs())
        proc.processed_template = {}

        record = proc.create_database_record()
        expected = hashlib.md5("{}".encode("utf-8")).hexdigest()
        assert record["checksum"] == expected

    @patch("processor.template_processor.base.base_template_processor.get_from_currentdata")
    def test_record_source_is_first_part_of_snapshot_source(self, mock_get_current):
        mock_get_current.return_value = "sess"
        node = _minimal_node(paths=["t.json"])
        kwargs = _base_kwargs(snapshot_source="myconnector.json")
        proc = TemplateProcessor(node, **kwargs)
        proc.processed_template = {}

        record = proc.create_database_record()
        assert record["source"] == "myconnector"

    @patch("processor.template_processor.base.base_template_processor.get_from_currentdata")
    def test_record_json_field_holds_processed_template(self, mock_get_current):
        mock_get_current.return_value = "sess"
        node = _minimal_node(paths=["t.json"])
        proc = TemplateProcessor(node, **_base_kwargs())
        proc.processed_template = {"Resources": {"Bucket": {}}}

        record = proc.create_database_record()
        assert record["json"] == {"Resources": {"Bucket": {}}}

    @patch("processor.template_processor.base.base_template_processor.get_from_currentdata")
    def test_record_error_is_none_when_no_error(self, mock_get_current):
        mock_get_current.return_value = "sess"
        node = _minimal_node(paths=["t.json"])
        proc = TemplateProcessor(node, **_base_kwargs())
        proc.processed_template = {"key": "val"}

        record = proc.create_database_record()
        assert record["error"] is None


# ===================================================================
# 8. Collection name normalization
# ===================================================================

class TestCollectionNameNormalization:
    """Verify that collection names are lowercased and dots are removed."""

    @patch("processor.template_processor.base.base_template_processor.get_from_currentdata")
    def test_dots_removed_and_lowered(self, mock_get_current):
        mock_get_current.return_value = "sess"
        node = _minimal_node(collection="Microsoft.Compute", paths=["t.json"])
        proc = TemplateProcessor(node, **_base_kwargs())
        proc.processed_template = {}

        record = proc.create_database_record()
        assert record["collection"] == "microsoftcompute"

    @patch("processor.template_processor.base.base_template_processor.get_from_currentdata")
    def test_already_lowercase_no_dots(self, mock_get_current):
        mock_get_current.return_value = "sess"
        node = _minimal_node(collection="myresources", paths=["t.json"])
        proc = TemplateProcessor(node, **_base_kwargs())
        proc.processed_template = {}

        record = proc.create_database_record()
        assert record["collection"] == "myresources"

    @patch("processor.template_processor.base.base_template_processor.get_from_currentdata")
    def test_mixed_case_with_multiple_dots(self, mock_get_current):
        mock_get_current.return_value = "sess"
        node = _minimal_node(collection="Azure.Network.VNet", paths=["t.json"])
        proc = TemplateProcessor(node, **_base_kwargs())
        proc.processed_template = {}

        record = proc.create_database_record()
        assert record["collection"] == "azurenetworkvnet"


# ===================================================================
# 9. Sensitive file detection
# ===================================================================

class TestSensitiveFileDetection:
    """Verify that the base TemplateProcessor correctly flags sensitive file extensions."""

    @pytest.fixture()
    def processor(self):
        node = _minimal_node()
        return TemplateProcessor(node, **_base_kwargs())

    @pytest.mark.parametrize("ext", [".pfx", ".p12", ".cer", ".pem", ".crt", ".crl", ".csr", ".der", ".p7b", ".p7r", ".spc"])
    def test_sensitive_extensions_flagged(self, processor, ext):
        assert processor.is_sensitive_file(f"/some/path/cert{ext}") is True

    @pytest.mark.parametrize("ext", [".json", ".yaml", ".tf", ".py", ".txt", ".md"])
    def test_non_sensitive_extensions_not_flagged(self, processor, ext):
        assert processor.is_sensitive_file(f"/some/path/file{ext}") is False

    def test_sensitive_detection_is_case_insensitive(self, processor):
        assert processor.is_sensitive_file("/path/cert.PEM") is True
        assert processor.is_sensitive_file("/path/cert.Pfx") is True

    def test_key_extension_not_in_sensitive_list(self, processor):
        # .key is NOT in the actual sensitive_extension_list in the source
        assert processor.is_sensitive_file("/path/server.key") is False


# ===================================================================
# 10. Base processor default behaviour
# ===================================================================

class TestBaseProcessorDefaults:
    """Verify default behaviour of the base TemplateProcessor methods."""

    @pytest.fixture()
    def processor(self):
        node = _minimal_node()
        return TemplateProcessor(node, **_base_kwargs())

    def test_base_is_template_file_returns_false(self, processor):
        assert processor.is_template_file("/any/path.json") is False

    def test_base_is_parameter_file_returns_false(self, processor):
        assert processor.is_parameter_file("/any/path.json") is False

    def test_base_process_template_returns_empty_dict(self, processor):
        assert processor.process_template(["path.json"]) == {}

    def test_default_content_type_is_json(self, processor):
        assert processor.contentType == "json"

    def test_exclude_directories_contains_git(self, processor):
        assert ".git" in processor.exclude_directories
