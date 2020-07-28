import pytest

node_data = {
	'snapshotId' : 'SNAPSHOT_1',
	'type': 'deploymentmanager',
	'collection': 'deploymentmanager',
	'paths': [
		'google_template/template_files/jinja/cloudbuild.yaml'
	]
}

master_node_data = {
	'snapshotId' : 'MASTER_SNAPSHOT_1',
	'type': 'deploymentmanager',
	'collection': 'deploymentmanager',
	'paths': [
		'jinja/cloudbuild.yaml'
	]
}

template_processor_kwargs = {
	'container': 'google_template', 
	'snapshot_source': 'fsGoogleConnector', 
	'repopath': '/tmp/tmp2u5r6vxn', 
	'connector_data': { 
		'fileType' : 'structure', 
		'type' : 'filesystem',
		'companyName' : 'prancer-test',
		'gitProvider' : 'https://github.com/GoogleCloudPlatform/deploymentmanager-samples.git',
		'username' : 'test',
		'httpsUser' : 'test',
		'branchName' : 'master',
		'private' : False
	}, 
	'dbname': 'validator', 
	'snapshot': {
		'source': 'base-template-connector',
		'nodes' : [
			{
				'snapshotId': 'SNAPSHOT_1',
				'type': 'deploymentmanager',
				'collection': 'deploymentmanager',
				'paths' : [
					'google_template/template_files/python/cloudbuild.yaml'
				],
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

def mock_config_value(section, key, default=None):
    if key == 'dbname':
        return 'dbname'
    return ''

def mock_process_template(self, paths):
    return {
        "resources" : []
    }

def test_populate_template_snapshot_false(monkeypatch):
    monkeypatch.setattr('processor.template_processor.base.base_template_processor.config_value', mock_config_value)
    monkeypatch.setattr('processor.template_processor.base.base_template_processor.get_collection_size', mock_get_collection_size)
    monkeypatch.setattr('processor.template_processor.base.base_template_processor.create_indexes', mock_create_indexes)
    monkeypatch.setattr('processor.template_processor.base.base_template_processor.insert_one_document', mock_insert_one_document)
    from processor.template_processor.base.base_template_processor import TemplateProcessor

    template_processor = TemplateProcessor(node_data, **template_processor_kwargs)
    snapshot_data = template_processor.populate_template_snapshot()
    assert snapshot_data == {
		'SNAPSHOT_1': False
	}

def test_populate_template_snapshot_true(monkeypatch):
    monkeypatch.setattr('processor.template_processor.base.base_template_processor.config_value', mock_config_value)
    monkeypatch.setattr('processor.template_processor.base.base_template_processor.get_collection_size', mock_get_collection_size)
    monkeypatch.setattr('processor.template_processor.base.base_template_processor.create_indexes', mock_create_indexes)
    monkeypatch.setattr('processor.template_processor.base.base_template_processor.insert_one_document', mock_insert_one_document)
    monkeypatch.setattr('processor.template_processor.base.base_template_processor.TemplateProcessor.process_template', mock_process_template)
    from processor.template_processor.base.base_template_processor import TemplateProcessor

    template_processor = TemplateProcessor(node_data, **template_processor_kwargs)
    snapshot_data = template_processor.populate_template_snapshot()
    assert snapshot_data == {
		'SNAPSHOT_1': True
	}
