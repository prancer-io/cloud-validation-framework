from processor.template_processor.aws_template_processor import AWSTemplateProcessor
from processor.template_processor.azure_template_processor import AzureTemplateProcessor
from processor.template_processor.google_template_processor import GoogleTemplateProcessor

TEMPLATE_NODE_TYPES = {
    "cloudformation": AWSTemplateProcessor,
    "arm" : AzureTemplateProcessor,
    "deploymentmanager" : GoogleTemplateProcessor,
}