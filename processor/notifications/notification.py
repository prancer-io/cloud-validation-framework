"""
   Common file for notification functionality.
"""
from processor.logging.log_handler import getlogger
from processor.helper.config.config_utils import config_value
from processor.helper.httpapi.http_utils import http_post_request

logger = getlogger()


def send_notification(message):
    """Send notification data from config"""
    notification_type = config_value('NOTIFICATION', 'type')
    if notification_type:
        if notification_type == 'slack':
            send_slack_notification(message)


def send_slack_notification(message):
    """Send notification to private channel as configured for the user."""
    slackurl = config_value('NOTIFICATION', 'webhook')
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
