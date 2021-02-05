from unittest.mock import MagicMock, Mock
from urllib.error import HTTPError, URLError


def my_side_effect():
    raise Exception("Test")

def mock_urlopen(url):
    cm = MagicMock()
    cm.status = 200
    cm.read.return_value = str.encode('{"a": "b"}')
    return cm

def mock_urlopen_exception(url):
    cm = MagicMock()
    cm.status = 404
    cm.read.side_effect = HTTPError(url, 404, 'not found', {}, None)
    return cm

def mock_urlopen_URLError_exception(url):
    cm = MagicMock()
    cm.status = 500
    cm.read.side_effect = URLError('Unknown URL Error')
    return cm

def test_http_get_request(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.http_utils.request.urlopen', mock_urlopen)
    from processor.helper.httpapi.http_utils import http_get_request
    st, ret = http_get_request('http://a.b.c')
    assert True == isinstance(ret, dict)
    assert 200 == st
    st, ret = http_get_request(None)
    assert ret is None
    assert st is None
    st, ret = http_get_request('http://a.b.c', {'Content-Type': 'application/json'})
    assert True == isinstance(ret, dict)
    assert 200 == st

def test_http_get_request_exception(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.http_utils.request.urlopen', mock_urlopen_exception)
    from processor.helper.httpapi.http_utils import http_get_request
    st, ret = http_get_request('http://a.b.c')
    assert ret is None
    assert st == 404

def test_http_get_request_URLError_exception(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.http_utils.request.urlopen', mock_urlopen_URLError_exception)
    from processor.helper.httpapi.http_utils import http_get_request
    st, ret = http_get_request('http://a.b.c')
    assert type(ret) is str
    assert st == 500

def test_http_delete_request(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.http_utils.request.urlopen', mock_urlopen)
    from processor.helper.httpapi.http_utils import http_delete_request
    st, ret = http_delete_request('http://a.b.c', {'a':'b'})
    assert True == isinstance(ret, dict)
    assert 200 == st
    st, ret = http_delete_request(None)
    assert ret is None
    assert st is None
    st, ret = http_delete_request('http://a.b.c', {'a': 'b'}, {'Content-Type': 'application/json'})
    assert True == isinstance(ret, dict)
    assert 200 == st


def test_http_delete_request_exception(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.http_utils.request.urlopen', mock_urlopen_exception)
    from processor.helper.httpapi.http_utils import http_delete_request
    st, ret = http_delete_request('http://a.b.c')
    assert ret is None
    assert st == 404


def test_http_put_request(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.http_utils.request.urlopen', mock_urlopen)
    from processor.helper.httpapi.http_utils import http_put_request
    st, ret = http_put_request('http://a.b.c', {'a':'b'})
    assert True == isinstance(ret, dict)
    assert 200 == st
    st, ret = http_put_request(None, None)
    assert ret is None
    assert st is None
    st, ret = http_put_request('http://a.b.c', {'a': 'b'}, {'Content-Type': 'application/json'})
    assert True == isinstance(ret, dict)
    assert 200 == st


def test_http_put_request_exception(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.http_utils.request.urlopen', mock_urlopen_exception)
    from processor.helper.httpapi.http_utils import http_put_request
    st, ret = http_put_request('http://a.b.c', {'a': 'b'})
    assert ret is None
    assert st == 404


def test_http_post_request(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.http_utils.request.urlopen', mock_urlopen)
    from processor.helper.httpapi.http_utils import http_post_request
    st, ret = http_post_request('http://a.b.c', {'a':'b'})
    assert True == isinstance(ret, dict)
    assert 200 == st
    st, ret = http_post_request('http://a.b.c', {'a': 'b'}, {}, True)
    assert True == isinstance(ret, dict)
    assert 200 == st
    st, ret = http_post_request(None, None)
    assert ret is None
    assert st is None
    st, ret = http_post_request('http://a.b.c', {'a': 'b'}, {'Content-Type': 'application/json'})
    assert True == isinstance(ret, dict)
    assert 200 == st


def test_http_post_request_exception(monkeypatch):
    monkeypatch.setattr('processor.helper.httpapi.http_utils.request.urlopen', mock_urlopen_exception)
    from processor.helper.httpapi.http_utils import http_post_request
    st, ret = http_post_request('http://a.b.c', {'a': 'b'})
    assert ret is None
    assert st == 404


def test_check_and_add_error():
    from processor.helper.httpapi.http_utils import check_and_add_error
    from processor.helper.config.rundata_utils import save_currentdata, get_from_currentdata
    save_currentdata(None)
    check_and_add_error(200, 'Failed http get')
    value = get_from_currentdata('errors')
    assert value is None
    check_and_add_error(400, 'Failed http get')
    value = get_from_currentdata('errors')
    assert value is not None
