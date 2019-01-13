import json
from unittest.mock import Mock
from processor.api.app_init import get_appdata, LOGGER


def mock_run_container_validation_tests_database(container):
    pass

def mock_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return [{
        "_id": "5c24af787456217c485ad1e6",
        "checksum": "7d814f2f82a32ea91ef37de9e11d0486",
        "collection": "microsoftcompute",
        "json":{
            "id": 124,
            "location": "eastus2",
            "name": "mno-nonprod-shared-cet-eastus2-tab-as03"
        },
        "queryuser": "ajeybk1@kbajeygmail.onmicrosoft.com",
        "snapshotId": 1,
        "timestamp": 1545908086831
    }]

def mock_empty_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return []

def mock_pymongo(app, uri=None, **kwargs):
    return {}

def mock_jsonify(data):
    return data

def mock_response_jsonify(data):
    response = Mock()
    response.data = data
    response.status_code = 200
    response.headers = Mock()
    return response


def mock_session():
    session = Mock()
    session.permanent = False
    return session

def mock_app():
    app = Mock()
    app.config = {'APPVERSION': 'abcd', 'APPNAME': 'XYZ'}
    return app

def test_get_appdata():
    assert LOGGER is not None
    data = get_appdata()
    assert type(data) is dict


def test_create_db(monkeypatch):
    monkeypatch.setattr('processor.api.app_init.PyMongo', mock_pymongo)
    from processor.api.app_init import create_db
    app = mock_app()
    app.config = {}
    appdb = create_db(app)
    assert appdb is not None

def test_make_session_permanent(monkeypatch):
    monkeypatch.setattr('processor.api.app_init.session', mock_session)
    monkeypatch.setattr('processor.api.app_init.app', mock_app)
    import datetime
    from processor.api.app_init import make_session_permanent, app
    lapp = mock_app()
    lapp.permanent_session_lifetime = datetime.timedelta(minutes=10)
    make_session_permanent()
    assert app.permanent_session_lifetime == datetime.timedelta(minutes=60000)


def test_index(monkeypatch):
    monkeypatch.setattr('processor.api.app_init.jsonify', mock_jsonify)
    app = mock_app()
    monkeypatch.setattr('processor.api.app_init.app', app)
    from processor.api.app_init import index
    data = index()
    assert data is not None
    assert data['status'] == 'OK'


def test_not_found(monkeypatch):
    monkeypatch.setattr('processor.api.app_init.jsonify', mock_jsonify)
    app = mock_app()
    monkeypatch.setattr('processor.api.app_init.app', app)
    from processor.api.app_init import not_found
    data = not_found('Error')
    assert data is not None
    assert data['status'] == 'NOK'

def test_create_app():
    from flask import Flask
    from processor.api.app_init import create_app
    app = create_app()
    assert type(app) is Flask

def test_unauthorized(monkeypatch):
    monkeypatch.setattr('processor.api.app_init.jsonify', mock_response_jsonify)
    from processor.api.app_init import unauthorized
    resp = unauthorized()
    assert resp is not None

def test_register_modules(monkeypatch):
    app = mock_app()
    app.config['APIPREFIX'] = '/a/b/c'
    monkeypatch.setattr('processor.api.app_init.app', app)
    app.register_blueprint = lambda x: x
    from processor.api.app_init import register_modules
    register_modules(app)

def test_initapp(monkeypatch):
    monkeypatch.setattr('processor.api.app_init.PyMongo', mock_pymongo)
    from processor.api.app_init import initapp
    db, app = initapp()
    assert db is not None
    assert app is not None

def test_app_version(client):
    from flask import url_for
    response = client.get(url_for('MODAPI.app_version'))
    assert response.status_code == 200
    assert response.json['app'] == 'abcd'


def test_run_framework_test(client, monkeypatch):
    monkeypatch.setattr('processor.api.apicontroller.run_container_validation_tests_database',
                        mock_run_container_validation_tests_database)
    monkeypatch.setattr('processor.api.apicontroller.get_documents', mock_get_documents)
    from flask import url_for
    response = client.post(url_for('MODAPI.run_framework_test'), data={})
    assert response.status_code == 200
    assert response.json['status'] == 'NOK'
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    val = {'container':'abcd'}
    response = client.post(url_for('MODAPI.run_framework_test'), data=json.dumps(val), headers=headers)
    assert response.status_code == 200
    assert response.json is not None
    assert response.json['status'] == 'OK'


def test_empty_run_framework_test(client, monkeypatch):
    monkeypatch.setattr('processor.api.apicontroller.run_container_validation_tests_database',
                        mock_run_container_validation_tests_database)
    monkeypatch.setattr('processor.api.apicontroller.get_documents', mock_empty_get_documents)
    from flask import url_for
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    val = {'container':'abcd'}
    response = client.post(url_for('MODAPI.run_framework_test'), data=json.dumps(val), headers=headers)
    assert response.status_code == 200
    assert response.json is not None
    assert response.json['status'] == 'OK'
