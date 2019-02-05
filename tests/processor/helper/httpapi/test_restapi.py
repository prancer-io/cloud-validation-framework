from unittest.mock import MagicMock
from requests.exceptions import HTTPError


def my_side_effect():
    raise Exception("Test")

def mock_urlopen(url, **kwargs):
    cm = MagicMock()
    cm.status_code = 200
    cm.json.return_value = {"a": "b"}
    return cm


def mock_urlopen_exception(url, **kwargs):
    cm = MagicMock()
    cm.status_code = 404
    cm.json.side_effect = HTTPError(url, 404, 'not found', {}, None)
    # cm.raiseError.side_effect = Mock(side_effect=Exception('Test'))
    return cm


def test_json_get_request(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi.requests.get', mock_urlopen)
    from processor.helper.httpapi.restapi import json_get_request
    st, ret = json_get_request('http://a.b.c')
    assert True == isinstance(ret, dict)
    assert 200 == st
    st, ret = json_get_request(None)
    assert ret is None
    assert st is None
    st, ret = json_get_request('http://a.b.c', {'Content-Type': 'application/json'})
    assert True == isinstance(ret, dict)
    assert 200 == st


def test_json_get_request_exception(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi.requests.get', mock_urlopen_exception)
    from processor.helper.httpapi.restapi import json_get_request
    st, ret = json_get_request('http://a.b.c')
    assert ret is None
    assert st == 404


def test_json_delete_request(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi.requests.delete', mock_urlopen)
    from processor.helper.httpapi.restapi import json_delete_request
    st, ret = json_delete_request('http://a.b.c')
    assert True == isinstance(ret, dict)
    assert 200 == st
    st, ret = json_delete_request(None)
    assert ret is None
    assert st is None
    st, ret = json_delete_request('http://a.b.c', {'a':'b'}, {'Content-Type': 'application/json'})
    assert True == isinstance(ret, dict)
    assert 200 == st


def test_json_delete_request_exception(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi.requests.delete', mock_urlopen_exception)
    from processor.helper.httpapi.restapi import json_delete_request
    st, ret = json_delete_request('http://a.b.c')
    assert ret is None
    assert st == 404


def test_json_put_request(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi.requests.put', mock_urlopen)
    from processor.helper.httpapi.restapi import json_put_request
    st, ret = json_put_request('http://a.b.c', {})
    assert True == isinstance(ret, dict)
    assert 200 == st
    st, ret = json_put_request(None, None)
    assert ret is None
    assert st is None
    st, ret = json_put_request('http://a.b.c', {'a':'b'}, {'Content-Type': 'application/json'})
    assert True == isinstance(ret, dict)
    assert 200 == st


def test_json_put_request_exception(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi.requests.put', mock_urlopen_exception)
    from processor.helper.httpapi.restapi import json_put_request
    st, ret = json_put_request('http://a.b.c', {})
    assert ret is None
    assert st == 404


def test_json_post_request(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi.requests.post', mock_urlopen)
    from processor.helper.httpapi.restapi import json_post_request
    st, ret = json_post_request('http://a.b.c', {})
    assert True == isinstance(ret, dict)
    assert 200 == st
    st, ret = json_post_request(None, None)
    assert ret is None
    assert st is None
    st, ret = json_post_request('http://a.b.c', {'a':'b'}, {'Content-Type': 'application/json'})
    assert True == isinstance(ret, dict)
    assert 200 == st


def test_json_post_request_exception(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.restapi.requests.post', mock_urlopen_exception)
    from processor.helper.httpapi.restapi import json_post_request
    st, ret = json_post_request('http://a.b.c', {})
    assert ret is None
    assert st == 404