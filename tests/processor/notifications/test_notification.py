""" Tests for vault"""
import os
from unittest.mock import Mock
frameworkdir = '/tmp'


def mock_framework_dir():
    return frameworkdir

def mock_config_value(section, key, default=None):
    if key == 'type':
        return 'slack'
    elif key == 'webhook':
        return None
    elif key == 'enabled':
        return 'True'
    return 'pytestdb'


def mock_url_config_value(section, key, default=None):
    return 'http://a.b.c/'


def mock_valid_http_post_request(url, mapdata, headers=None, json_type=False, name='POST'):
    return 200, {'access_token': 'abcd'}


def mock_get_vault_data(client_id):
    return None


def mock_nonempty_get_vault_data(client_id):
    return 'abcd'


def mock_SMTP(*args, **kwargs):
    return Mock()


def mock_exception_SMTP(*args, **kwargs):
    raise Exception("SMTP connection error!")


def test_send_notification(create_temp_dir, create_temp_json, monkeypatch):
    monkeypatch.setattr('processor_enterprise.notifications.notification.framework_dir', mock_framework_dir)
    monkeypatch.setattr('processor_enterprise.notifications.notification.config_value', mock_config_value)
    monkeypatch.setattr('processor_enterprise.notifications.notification.get_vault_data',
                        mock_nonempty_get_vault_data)
    monkeypatch.setattr('processor_enterprise.notifications.notification.http_post_request',
                        mock_valid_http_post_request)
    monkeypatch.setattr('processor_enterprise.notifications.notification.SMTP',
                        mock_exception_SMTP)
    monkeypatch.setattr('processor.connector.validation.get_test_json_dir',
                        mock_framework_dir)
    ns = {
        "fileType": "structure",
        "notifications": [
            {
                "notificationId": "1",
                "type": "slack",
                "webhookkey": "notification-slack-1"
            },
            {
                "notificationId": "2",
                "type": "email",
                "user": "ajey.khanapuri@gmail.com",
                "userkey": "ajey-khanapuri-gmail-com",
                "to": "kbajey@gmail.com",
                "smtp": {
                    "server": "smtp.gmail.com",
                    "port": 587,
                    "tls": True
                }
            },
            {
                "notificationId": "3",
                "type": "telegram",
                "webhookkey": "notification-telegram-1"
            }
        ]
    }
    global frameworkdir
    frameworkdir = create_temp_dir()
    newpath = frameworkdir
    os.mkdir('%s/pytestdb' % newpath)
    fname = create_temp_json(newpath, data=ns, fname='notifications.json')
    f = '%s/%s' % (newpath, fname)
    print(f)
    assert True == os.path.exists(f)
    from processor_enterprise.notifications.notification import send_notification, check_send_notification
    val = send_notification('container6', 'Send Test')
    assert val is None
    val = check_send_notification('container6', 'Send Test')
    assert val is None


def test_get_azure_vault_data(monkeypatch):
    monkeypatch.setattr('processor_enterprise.notifications.notification.config_value',
                        mock_url_config_value)
    monkeypatch.setattr('processor_enterprise.notifications.notification.http_post_request',
                        mock_valid_http_post_request)
    monkeypatch.setattr('processor_enterprise.notifications.notification.get_vault_data',
                        mock_nonempty_get_vault_data)
    from processor_enterprise.notifications.notification import send_slack_notification
    send_slack_notification({}, 'Send Test')


def test_nourl_send_slack_notification(monkeypatch):
    monkeypatch.setattr('processor_enterprise.notifications.notification.get_vault_data',
                        mock_get_vault_data)
    monkeypatch.setattr('processor_enterprise.notifications.notification.http_post_request',
                        mock_valid_http_post_request)
    from processor_enterprise.notifications.notification import send_slack_notification
    send_slack_notification({}, 'Send Test')


def test_send_slack_notification(monkeypatch):
    monkeypatch.setattr('processor_enterprise.notifications.notification.get_vault_data',
                        mock_nonempty_get_vault_data)
    monkeypatch.setattr('processor_enterprise.notifications.notification.http_post_request',
                        mock_valid_http_post_request)
    from processor_enterprise.notifications.notification import send_slack_notification
    send_slack_notification({}, 'Send Test')
    notification = {
      "notificationId": "1",
      "type": "slack",
      "webhookkey": "notification-slack-1"
    }
    send_slack_notification(notification, 'Send Test')


def test_send_email_notification(monkeypatch):
    monkeypatch.setattr('processor_enterprise.notifications.notification.get_vault_data',
                        mock_nonempty_get_vault_data)
    monkeypatch.setattr('processor_enterprise.notifications.notification.SMTP',
                        mock_SMTP)
    from processor_enterprise.notifications.notification import send_email_notification
    notification = {
        "notificationId": "2",
        "type": "email",
        "user": "ajey.khanapuri@gmail.com",
        "userkey": "ajey-khanapuri-gmail-com",
        "to": "kbajey@gmail.com",
        "smtp": {
            "server": "smtp.gmail.com",
            "port": 587,
            "tls": True
        }
    }
    message = "Test Message"
    val = send_email_notification(notification, message)
    assert val is None


def test_exception_send_email_notification(monkeypatch):
    monkeypatch.setattr('processor_enterprise.notifications.notification.get_vault_data',
                        mock_nonempty_get_vault_data)
    monkeypatch.setattr('processor_enterprise.notifications.notification.SMTP',
                        mock_exception_SMTP)
    from processor_enterprise.notifications.notification import send_email_notification
    notification = {
        "notificationId": "2",
        "type": "email",
        "user": "ajey.khanapuri@gmail.com",
        "userkey": "ajey-khanapuri-gmail-com",
        "to": "kbajey@gmail.com",
        "smtp": {
            "server": "smtp.gmail.com",
            "port": 587,
            "tls": True
        }
    }
    message = "Test Message"
    val = send_email_notification(notification, message)
    assert val is None


def test_missing_send_email_notification(monkeypatch):
    monkeypatch.setattr('processor_enterprise.notifications.notification.get_vault_data',
                        mock_nonempty_get_vault_data)
    monkeypatch.setattr('processor_enterprise.notifications.notification.SMTP',
                        mock_exception_SMTP)
    from processor_enterprise.notifications.notification import send_email_notification
    notification = {
        "notificationId": "2",
        "type": "email",
        "user": "ajey.khanapuri@gmail.com",
        "userkey": "ajey-khanapuri-gmail-com",
        "to": "kbajey@gmail.com"
    }
    message = "Test Message"
    val = send_email_notification(notification, message)
    assert val is None
