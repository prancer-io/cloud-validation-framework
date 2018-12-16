""" Tests for snapshot azure"""


def mock_http_get_request_happy(url, headers=None):
    data = {'a': 'b'}
    return 200, data


def mock_http_get_request_error(url, headers=None):
    data = {'a': 'b'}
    return 400, data


def test_get_version_for_type():
    from processor.connector.snapshot_azure import get_version_for_type
    assert None == get_version_for_type({})
    assert '2018-07-01' == get_version_for_type({'type': 'Microsoft.Network/virtualNetworks'})


def test_get_node_happy(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.http_get_request', mock_http_get_request_happy)
    from processor.connector.snapshot_azure import get_node
    data = {
        'type': 'Microsoft.Network/virtualNetworks',
        'snapshotId': '1',
        'path': "/resourceGroups/mno-nonprod-shared-cet-eastus2-networkWatcher/providers/"
                "Microsoft.Compute/availabilitySets/mno-nonprod-shared-cet-eastus2-tab-as03"

    }
    ret = get_node(None, None, data, 'abc')
    assert True == isinstance(ret, dict)
    ret = get_node('abcd', 'xyz', data, 'abc')
    assert True == isinstance(ret, dict)
    assert {'a': 'b'} == ret['json']


def test_get_node_error(monkeypatch):
    monkeypatch.setattr('processor.connector.snapshot_azure.http_get_request', mock_http_get_request_error)
    from processor.connector.snapshot_azure import get_node
    data = {
        'type': 'Microsoft.Network/virtualNetworks',
        'snapshotId': '1',
        'path': "/resourceGroups/mno-nonprod-shared-cet-eastus2-networkWatcher/providers/"
                "Microsoft.Compute/availabilitySets/mno-nonprod-shared-cet-eastus2-tab-as03"

    }
    ret = get_node(None, None, data, 'abc')
    assert True == isinstance(ret, dict)
    ret = get_node('abcd', 'xyz', data, 'abc')
    assert True == isinstance(ret, dict)
    assert {} == ret['json']