import pytest
import os

path = os.path.dirname(os.path.abspath(__file__))

paths = [[
	'sample_1/main.tf'
],[
	'sample_2/main.tf',
 	'sample_2/terraform.tfvars',
  	'sample_2/vars.tf'
],[
	'sample_3/ec2/main.tf',
 	'sample_3/ec2/terraform.tfvars',
  	'sample_3/ec2/vars.tf'
],[
	'sample_4/lambda/main.tf',
 	'sample_4/lambda/terraform.tfvars',
  	'sample_4/lambda/vars.tf'
],[
	'sample_5/sg/main.tf'
]]

template_processor_kwargs = {
	'container': 'terraform_template', 
	'snapshot_source': 'fsTerraformConnector', 
	'repopath': '/tmp/tmp2u5r6vxn', 
	'connector_data': { 
		'fileType' : 'structure', 
		'type' : 'filesystem',
		'companyName' : 'prancer-test',
		'folderPath' : "%s/%s" % (path, "samples"),
		'username' : 'test'
	}, 
	'dbname': 'validator', 
	'snapshot': {
		'source': 'base-template-connector',
		'nodes' : [
			{
				'snapshotId': 'SNAPSHOT_1',
				'type': 'terraform',
				'collection': 'terraform',
				'paths' : [],
				'status': 'active'
			}
		]
	},
	'snapshot_data': {
		'SNAPSHOT_1': False, 
	}
}

def mock_get_collection_size(collection_name):
    return 0

def mock_create_indexes(collection, database, indexes):
    return True

def mock_insert_one_document(doc, collection, dbname, check_keys=False):
    pass

def mock_process_template(self, paths):
    return {
        "resources" : []
    }

def test_terraform_single_file(monkeypatch):
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.get_collection_size', mock_get_collection_size)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.create_indexes', mock_create_indexes)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.insert_one_document', mock_insert_one_document)
	from processor.template_processor.terraform_template_processor import TerraformTemplateProcessor

	node_data = template_processor_kwargs["snapshot"]["nodes"][0]
 
	template_processor_kwargs["snapshot"]["nodes"][0]["paths"] = paths[0]

	template_processor = TerraformTemplateProcessor(node_data, **template_processor_kwargs)
	snapshot_data = template_processor.populate_template_snapshot()

	assert snapshot_data == {
		'SNAPSHOT_1': True
	}

	assert template_processor.processed_template != None
 
	assert template_processor.processed_template["resources"][0]["properties"]["name"] == "prancer-vnet"
	assert template_processor.processed_template["resources"][0]["properties"]["address_space"] == ["10.254.0.0/16"]
	assert template_processor.processed_template["resources"][0]["properties"]["tags"] == {
		"environment" : "Production",
		"project" : "Prancer"
	}

def test_terraform_variable_declaration(monkeypatch):
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.get_collection_size', mock_get_collection_size)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.create_indexes', mock_create_indexes)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.insert_one_document', mock_insert_one_document)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.TemplateProcessor.process_template', mock_process_template)
	from processor.template_processor.terraform_template_processor import TerraformTemplateProcessor

	node_data = template_processor_kwargs["snapshot"]["nodes"][0]
 
	template_processor_kwargs["snapshot"]["nodes"][0]["paths"] = paths[1]

	template_processor = TerraformTemplateProcessor(node_data, **template_processor_kwargs)
	snapshot_data = template_processor.populate_template_snapshot()

	assert snapshot_data == {
		'SNAPSHOT_1': True
	}

	assert template_processor.processed_template != None
	
	# variable declare in terraform.tfvars
	assert template_processor.processed_template["resources"][0]["properties"]["resource_group_name"] == "storage-rg"
	
 	# variable declare in vars.tf
	assert template_processor.processed_template["resources"][0]["properties"]["location"] == "eastus2"
	
	# variable missing should keep the orignal reference
	assert template_processor.processed_template["resources"][0]["properties"]["account_tier"] == "${var.account_tier}"
 
def test_terraform_module_dir(monkeypatch):
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.get_collection_size', mock_get_collection_size)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.create_indexes', mock_create_indexes)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.insert_one_document', mock_insert_one_document)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.TemplateProcessor.process_template', mock_process_template)
	from processor.template_processor.terraform_template_processor import TerraformTemplateProcessor

	node_data = template_processor_kwargs["snapshot"]["nodes"][0]

	template_processor_kwargs["snapshot"]["nodes"][0]["paths"] = paths[2]

	template_processor = TerraformTemplateProcessor(node_data, **template_processor_kwargs)
	snapshot_data = template_processor.populate_template_snapshot()

	assert snapshot_data == {
		'SNAPSHOT_1': True
	}

	assert template_processor.processed_template != None
 
	for resource in template_processor.processed_template["resources"]:
		if resource["type"] == "aws_instance":
			properties = resource["properties"]
			assert properties.get("private_ip") == None
			assert properties.get("root_block_device") == []
			assert properties.get("ami") == "${data.aws_ami.ubuntu.id}"

		if resource["type"] == "aws_ebs_volume":
			properties = resource["properties"]
			assert properties.get("availability_zone") == "us-east-2a"
			assert properties.get("encrypted") == False
			assert properties.get("tags") == {
				"Name": "prancer-ec2",
				"Environment": "Production",
				"Project": "Prancer",
			}

def test_terraform_module_git(monkeypatch):
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.get_collection_size', mock_get_collection_size)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.create_indexes', mock_create_indexes)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.insert_one_document', mock_insert_one_document)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.TemplateProcessor.process_template', mock_process_template)
	from processor.template_processor.terraform_template_processor import TerraformTemplateProcessor

	node_data = template_processor_kwargs["snapshot"]["nodes"][0]

	template_processor_kwargs["snapshot"]["nodes"][0]["paths"] = paths[3]

	template_processor = TerraformTemplateProcessor(node_data, **template_processor_kwargs)
	snapshot_data = template_processor.populate_template_snapshot()

	assert snapshot_data == {
		'SNAPSHOT_1': True
	}

	assert template_processor.processed_template != None
 
	lambda_resource = False
  
	for resource in template_processor.processed_template["resources"]:
		
		if resource["type"] == "aws_lambda_function":
			lambda_resource = True
			properties = resource["properties"]
			assert properties["filename"] == "function.py.zip"
			assert properties["vpc_config"] == [
				{
					"security_group_ids": ["${module.security_group.id}"],
					"subnet_ids": ["${module.subnet.id}"],
				}]

	assert lambda_resource == True
 
 
def test_terraform_multiple_blocks(monkeypatch):
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.get_collection_size', mock_get_collection_size)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.create_indexes', mock_create_indexes)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.insert_one_document', mock_insert_one_document)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.TemplateProcessor.process_template', mock_process_template)
	from processor.template_processor.terraform_template_processor import TerraformTemplateProcessor

	node_data = template_processor_kwargs["snapshot"]["nodes"][0]

	template_processor_kwargs["snapshot"]["nodes"][0]["paths"] = paths[4]

	template_processor = TerraformTemplateProcessor(node_data, **template_processor_kwargs)
	snapshot_data = template_processor.populate_template_snapshot()

	assert snapshot_data == {
		'SNAPSHOT_1': True
	}

	assert template_processor.processed_template != None

	aws_security_group = False
	for resource in template_processor.processed_template["resources"]:
		
		if resource["type"] == "aws_security_group" and resource["name"] == "default":
			aws_security_group = True
			properties = resource["properties"]
			assert properties.get("ingress") != None
			assert len(properties["ingress"]) == 2
			assert properties["ingress"] == [
				{
					"from_port": 22,
					"to_port": 22,
					"protocol": "tcp",
					"cidr_blocks": ["0.0.0.0/0"],
				},
				{
					"from_port": 80,
					"to_port": 80,
					"protocol": "tcp",
					"cidr_blocks": ["0.0.0.0/0"],
				},
			]

	assert aws_security_group == True