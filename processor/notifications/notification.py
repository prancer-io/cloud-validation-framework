"""
   Common file for notification functionality.
"""
import platform
import smtplib
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_json_files, STRUCTURE,\
    json_from_file, get_field_value
from processor.helper.httpapi.http_utils import http_post_request
from processor.helper.config.config_utils import config_value, framework_dir
from processor.api.utils import parsebool
from processor.connector.vault import get_vault_data


logger = getlogger()


def check_send_notification(container, db):
    notification_enabled = parsebool(config_value('NOTIFICATION', 'enabled'))
    logger.info('Notification: %s, %s', notification_enabled, type(notification_enabled))
    if notification_enabled:
        msg = 'Completed tests for container: %s using %s.' % \
              (container, 'database' if db else 'filesystem')
        uname = platform.node()
        system = platform.system()
        msg = '%s on %s/%s' % (msg[:-1], uname, system)
        send_notification(container, msg)


def send_notification(container, message):
    """Send notification data from config"""
    logger.info("Starting notifications for container: %s", container)
    reporting_path = config_value('REPORTING', 'reportOutputFolder')
    json_dir = '%s/%s/../' % (framework_dir(), reporting_path)
    logger.info(json_dir)
    structure_files = get_json_files(json_dir, STRUCTURE)
    logger.info('\n'.join(structure_files))
    for structure_file in structure_files:
        json_data = json_from_file(structure_file)
        notifications = get_field_value(json_data, "notifications")
        if notifications:
            for notification in notifications:
                logger.info(notification)
                notification_type = get_field_value(notification, 'type')
                if notification_type:
                    if notification_type == 'slack':
                        send_slack_notification(notification, message)
                    elif notification_type == 'email':
                        send_email_notification(notification, message)
                    else:
                        logger.info('Unsupported notification type!')
    # notification_type = config_value('NOTIFICATION', 'type')
    # if notification_type:
    #     if notification_type == 'slack':
    #         send_slack_notification(message)


def send_slack_notification(notification, message):
    """Send notification to private channel as configured for the user."""
    slackurl = get_field_value(notification, 'webhook')
    if not slackurl:
        slackurlkey = get_field_value(notification, 'webhookkey')
        slackurl = get_vault_data(slackurlkey)
    if slackurl:
        data = {
            "text": message
        }
        headers = {
            'Content-type': 'application/json'
        }
        st, resp = http_post_request(slackurl, data, headers, True)
        logger.info('Status: %s, response: %s', st, resp)
    else:
        logger.info('Invalid slack webhook for notification!')


def send_email_notification(notification, message):
    """Send notification to emails as configured by the notification."""
    smtp_cfg = get_field_value(notification, 'smtp')
    user_name = get_field_value(notification, 'user')
    user_key = get_field_value(notification, 'userkey')
    user_pwd = get_vault_data(user_key)
    touser = get_field_value(notification, 'to')
    if smtp_cfg and user_name and user_pwd and touser:
        try:
            # creates SMTP session
            smtp_session = smtplib.SMTP('smtp.gmail.com', 587)
            istls = get_field_value(smtp_cfg, "tls")
            if istls:
                # start TLS for security
                smtp_session.starttls()
            # Authentication
            smtp_session.login(user_name, user_pwd)
            # sending the mail
            smtp_session.sendmail(user_name, touser, message)
            # terminating the session
            smtp_session.quit()
        except Exception as ex:
            logger.info('Email notification failed exception: %s!', ex)
    else:
        logger.info('Invalid email config for notification!')
