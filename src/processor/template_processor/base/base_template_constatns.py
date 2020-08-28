from processor.template_processor.aws_template_processor import AWSTemplateProcessor
from processor.template_processor.azure_template_processor import AzureTemplateProcessor
from processor.template_processor.google_template_processor import GoogleTemplateProcessor
from processor.template_processor.terraform_template_processor import TerraformTemplateProcessor

TEMPLATE_NODE_TYPES = {
    "cloudformation": AWSTemplateProcessor,
    "arm" : AzureTemplateProcessor,
    "deploymentmanager" : GoogleTemplateProcessor,
    "terraform" : TerraformTemplateProcessor,
}