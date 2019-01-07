""" Tests for snapshot custom"""
import os
from tests.conftest import data_dict


def test_get_node(create_temp_json, create_temp_dir):
    from processor.connector.snapshot_custom import get_node
    data = {
        'type': 'Microsoft.Network/virtualNetworks',
        'snapshotId': '1',
        'path': "a/b/c"
    }
    ret = get_node('/tmp', data)
    assert True == isinstance(ret, dict)
    # ret = get_node('abcd', 'xyz', data, 'abc')
    # assert True == isinstance(ret, dict)
    assert {} == ret['json']
    newpath = create_temp_dir()
    os.makedirs('%s/%s' % (newpath, data['path']))
    fname = create_temp_json('%s/%s' % (newpath, data['path']))
    data['path'] = '%s/%s' % (data['path'], fname)
    ret = get_node(newpath, data)
    assert True == isinstance(ret, dict)
    assert data_dict == ret['json']


def test_valid_clone_dir(create_temp_dir):
    from processor.connector.snapshot_custom import valid_clone_dir
    newpath = create_temp_dir()
    exists, empty = valid_clone_dir(newpath)
    assert True == exists
    assert True == empty
    exists, empty = valid_clone_dir('%s/a/b/c' % newpath)
    assert True == exists
    assert True == empty
    # create_temp_json(newpath)
    exists, empty = valid_clone_dir(newpath)
    assert True == exists
    assert False == empty
    exists, empty = valid_clone_dir('/a/b/c')
    assert False == exists
    assert False == empty
