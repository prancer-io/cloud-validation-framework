from processor.template_processor.aws_template_processor import AWSTemplateProcessor
from processor.template_processor.azure_template_processor import AzureTemplateProcessor
from processor.template_processor.google_template_processor import GoogleTemplateProcessor
from processor.template_processor.terraform_template_processor import TerraformTemplateProcessor
from processor.template_processor.yaml_template_processor import YamlTemplateProcessor
from processor.template_processor.json_template_processor import JsonTemplateProcessor

TEMPLATE_NODE_TYPES = {
    "cloudformation": AWSTemplateProcessor,
    "arm" : AzureTemplateProcessor,
    "deploymentmanager" : GoogleTemplateProcessor,
    "terraform" : TerraformTemplateProcessor,
    "yaml" : YamlTemplateProcessor,
    "json": JsonTemplateProcessor
}