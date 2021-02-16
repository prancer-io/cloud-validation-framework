import pytest
import os

path = os.path.dirname(os.path.abspath(__file__))

template_processor_kwargs = {
	'container': 'aws_template', 
	'snapshot_source': 'fsAwsConnector', 
	'repopath': '/tmp/tmp2u5r6vxn', 
	'connector_data': { 
		'fileType' : 'structure', 
		'type' : 'filesystem',
		'companyName' : 'prancer-test',
		'folderPath' : path,
		'username' : 'test'
	}, 
	'dbname': 'validator', 
	'snapshot': {
		'source': 'base-template-connector',
		'nodes' : [
			{
				'snapshotId': 'SNAPSHOT_1',
				'type': 'cloudformation',
				'collection': 'cloudformation',
				'paths' : [
					'sample/keyvault.json',
					'sample/vars.keyvaultrg.json'
				],
				'status': 'active'
			}
		]
	},
	'snapshot_data': {
		'SNAPSHOT_1': False, 
	}
}

master_template_processor_kwargs = {
	'container': 'google_template', 
	'snapshot_source': 'fsGoogleConnector', 
	'repopath': '/tmp/tmp2u5r6vxn', 
	'connector_data': { 
		'fileType' : 'structure', 
		'type' : 'filesystem',
		'companyName' : 'prancer-test',
		'folderPath' : path,
		'username' : 'test'
	}, 
	'dbname': 'validator', 
	'snapshot': {
		'source': 'base-template-connector',
		'nodes' : [
			{
				'masterSnapshotId': 'MASTER_SNAPSHOT_',
				'type': 'cloudformation',
				'collection': 'cloudformation',
				'paths' : [
					'/sample'
				],
				'status': 'active'
			}
		]
	},
	'snapshot_data': {
		"MASTER_SNAPSHOT_": "MASTER_SNAPSHOT_1", 
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

def test_populate_template_snapshot_true(monkeypatch):
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.get_collection_size', mock_get_collection_size)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.create_indexes', mock_create_indexes)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.insert_one_document', mock_insert_one_document)
	from processor.template_processor.azure_template_processor import AzureTemplateProcessor

	node_data = template_processor_kwargs["snapshot"]["nodes"][0]

	template_processor = AzureTemplateProcessor(node_data, **template_processor_kwargs)
	snapshot_data = template_processor.populate_template_snapshot()

	assert snapshot_data == {
		'SNAPSHOT_1': True
	}

	assert template_processor.processed_template != None
	assert template_processor.processed_template["resources"][0]["name"] == "cetsharednpdeus2akv02"

def test_populate_all_template_snapshot(monkeypatch):
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.get_collection_size', mock_get_collection_size)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.create_indexes', mock_create_indexes)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.insert_one_document', mock_insert_one_document)
	monkeypatch.setattr('processor.template_processor.base.base_template_processor.TemplateProcessor.process_template', mock_process_template)
	from processor.template_processor.azure_template_processor import AzureTemplateProcessor

	node_data = master_template_processor_kwargs["snapshot"]["nodes"][0]

	template_processor = AzureTemplateProcessor(node_data, **master_template_processor_kwargs)
	snapshot_data = template_processor.populate_all_template_snapshot()

	print("snapshot data Azure")
	print(snapshot_data)
	
	assert snapshot_data == {
		"MASTER_SNAPSHOT_": [
			{
				"snapshotId": "MASTER_SNAPSHOT_1",
				"type": "cloudformation",
				"collection": "cloudformation",
				"paths": ["/sample/vars.keyvaultrg.json"],
				"status": "inactive",
				"validate": True,
			},
			{
				"snapshotId": "MASTER_SNAPSHOT_2",
				"type": "cloudformation",
				"collection": "cloudformation",
				"paths": ["/sample/keyvault.json"],
				"status": "active",
				"validate": True,
			},
		]
	}
