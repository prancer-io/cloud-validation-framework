""" Tests for vault"""

def mock_config_value(section, key, default=None):
    if key == 'type':
        return 'slack'
    elif key == 'webhook':
        return None
    return 'pytestdb'

def mock_url_config_value(section, key, default=None):
    return 'http://a.b.c/'

def mock_valid_http_post_request(url, mapdata, headers=None, json_type=False, name='POST'):
    return 200, {'access_token': 'abcd'}

def mock_get_vault_data(client_id):
    return None

def test_send_notification(monkeypatch):
    monkeypatch.setattr('processor.notifications.notification.config_value', mock_config_value)
    monkeypatch.setattr('processor.notifications.notification.get_vault_data', mock_get_vault_data)
    from processor.notifications.notification import send_notification
    send_notification({}, 'Send Test')


def test_get_azure_vault_data(monkeypatch):
    monkeypatch.setattr('processor.notifications.notification.config_value', mock_url_config_value)
    monkeypatch.setattr('processor.notifications.notification.http_post_request',
                        mock_valid_http_post_request)
    monkeypatch.setattr('processor.notifications.notification.get_vault_data', mock_get_vault_data)
    from processor.notifications.notification import send_slack_notification
    send_slack_notification({}, 'Send Test')

