import os

path = os.path.dirname(os.path.abspath(__file__))

def test_valid_yaml(monkeypatch):
    from processor.templates.aws.aws_parser import AWSTemplateParser
    parameter_file = None
    template_file = '%s/sample/EC2InstanceWithSecurityGroupSample.yaml' % path
    aws_template_parser = AWSTemplateParser(template_file, parameter_file=parameter_file)
    template_json = aws_template_parser.parse()
    assert template_json != None
    assert template_json["AWSTemplateFormatVersion"] == "2010-09-09"

def test_valid_json(monkeypatch):
	from processor.templates.aws.aws_parser import AWSTemplateParser
	parameter_file = None
	template_file = '%s/sample/SingleENIwithMultipleEIPs.json' % path
	aws_template_parser = AWSTemplateParser(template_file, parameter_file=parameter_file)
	template_json = aws_template_parser.parse()
	assert template_json != None
	assert template_json["AWSTemplateFormatVersion"] == "2010-09-09"

def test_valid_template_as_json(monkeypatch):
    from processor.templates.aws.aws_parser import AWSTemplateParser
    parameter_file = None
    template_file = '%s/sample/SQS_With_CloudWatch_Alarms.template' % path
    aws_template_parser = AWSTemplateParser(template_file, parameter_file=parameter_file)
    template_json = aws_template_parser.parse()
    assert template_json != None
    assert template_json["AWSTemplateFormatVersion"] == "2010-09-09"

def test_valid_text_as_json(monkeypatch):
	from processor.templates.aws.aws_parser import AWSTemplateParser
	parameter_file = None
	template_file = '%s/sample/SQS_With_CloudWatch_Alarms.txt' % path
	aws_template_parser = AWSTemplateParser(template_file, parameter_file=parameter_file)
	template_json = aws_template_parser.parse()
	assert template_json != None
	assert template_json["AWSTemplateFormatVersion"] == "2010-09-09"

def test_invalid_text(monkeypatch):
	from processor.templates.aws.aws_parser import AWSTemplateParser
	parameter_file = None
	template_file = '%s/sample/InvalidTemplate.txt' % path
	aws_template_parser = AWSTemplateParser(template_file, parameter_file=parameter_file)
	template_json = aws_template_parser.parse()
	assert template_json is None


def test_valid_text_invalid_template(monkeypatch):
	from processor.templates.aws.aws_parser import AWSTemplateParser
	parameter_file = None
	template_file = '%s/sample/ValidJsonInvalidTemplate.txt' % path
	aws_template_parser = AWSTemplateParser(template_file, parameter_file=parameter_file)
	template_json = aws_template_parser.parse()
	assert template_json is None