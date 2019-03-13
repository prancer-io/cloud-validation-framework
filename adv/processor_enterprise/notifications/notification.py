"""
   Common file for notification functionality.
"""
import platform
import json
import copy
from smtplib import SMTP
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_json_files, STRUCTURE,\
    json_from_file, get_field_value, OUTPUT, TEST, collectiontypes
from processor.helper.httpapi.http_utils import http_post_request
from processor.helper.config.config_utils import config_value, framework_dir,\
    DATABASE, DBNAME
from processor.database.database import sort_field, get_documents
from processor.connector.vault import get_vault_data
from processor_enterprise.api.utils import parsebool
from processor_enterprise.api.utils import parseint


logger = getlogger()


def check_send_notification(container, db):
    notification_enabled = parsebool(config_value('NOTIFICATION', 'enabled'))
    logger.info('Notification: %s, %s', notification_enabled, type(notification_enabled))
    if not notification_enabled:
        return
    # if notification_enabled:
    #     msg = 'Completed tests for container: %s using %s.' % \
    #           (container, 'database' if db else 'filesystem')
    #     uname = platform.node()
    #     system = platform.system()
    #     msg = '%s on %s/%s' % (msg[:-1], uname, system)
    #     send_notification(container, msg)
    logger.info("Starting to send notifications.")
    if db:
        dbname = config_value(DATABASE, DBNAME)
        outputcollection = config_value(DATABASE, collectiontypes[OUTPUT])
        testcollection = config_value(DATABASE, collectiontypes[TEST])
        qry = {'container': container}
        sort = [sort_field('timestamp', False)]
        outputdocs = get_documents(outputcollection, dbname=dbname, sort=sort, query=qry)
        if outputdocs and len(outputdocs):
            logger.info('Number of output Documents: %s', len(outputdocs))
            processed_outputs = []
            for outputdoc in outputdocs:
                name = get_field_value(outputdoc, 'name')
                if name and name not in processed_outputs:
                    processed_outputs.append(name)
                    if outputdoc['json']:
                        output_json = outputdoc['json']
                        tstqry = {'container': container, 'name': name}
                        testdocs = get_documents(testcollection, dbname=dbname, sort=sort,
                                                 query=tstqry, limit=1)
                        if testdocs and len(testdocs):
                            logger.info('Number of test Documents: %s', len(testdocs))
                            if testdocs[0]['json']:
                                test_json = testdocs[0]['json']
                                process_output_notfication(container, output_json, test_json)
    else:
        reporting_path = config_value('REPORTING', 'reportOutputFolder')
        json_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)
        logger.info(json_dir)
        output_files = get_json_files(json_dir, OUTPUT)
        logger.info('\n'.join(output_files))
        for output_file in output_files:
            output_json = json_from_file(output_file)
            if output_json:
                test_filename = get_field_value(output_json, 'test')
                if test_filename:
                    # TODO check if filename needs a .json extension
                    test_file = '%s/%s' % (json_dir, test_filename)
                    test_json = json_from_file(test_file)
                    process_output_notfication(container, output_json, test_json)


def process_output_notfication(container, output_json, test_json):
    """Process the output json and its test json data"""
    if test_json and output_json:
        notifications = get_field_value(test_json, 'notification')
        for notification in notifications:
            level = get_field_value(notification, 'level')
            level = level if level and level in ['all', 'failed', 'passed', 'skipped'] else 'all'
            if level != 'all':
                new_res = []
                results = get_field_value(output_json, 'results')
                for res in results:
                    res_val = get_field_value(res, 'result')
                    if res_val and res_val == level:
                        new_res.append(res)
                output_data = copy.copy(output_json)
                output_data['results'] = new_res
            logger.info('Data: %s', output_data)
            send_notify(container, json.dumps(output_data), notification)


def send_notify(container, message, notify):
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
        notify_id = get_field_value(notify, 'notificationId')
        if notifications:
            for notification in notifications:
                notification_id = get_field_value(notification, 'notificationId')
                logger.info(notification)
                if notify_id and notification_id and notify_id == notification_id:
                    noti = copy.copy(notification)
                    noti.update(notify)
                    notification_type = get_field_value(noti, 'type')
                    if notification_type:
                        if notification_type == 'slack':
                            send_slack_notification(noti, message)
                        elif notification_type == 'email':
                            send_email_notification(noti, message)
                        else:
                            logger.info('Unsupported notification type!')


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
    logger.info('smtp_cfg: %s, username: %s, pwd: %s, to: %s',
                smtp_cfg, user_name, user_pwd, touser)
    if smtp_cfg and user_name and user_pwd and touser:
        try:
            # creates SMTP session
            smtp_server = get_field_value(smtp_cfg, 'server')
            smtp_port = parseint(get_field_value(smtp_cfg, 'port'), 587)
            smtp_session = SMTP(smtp_server, smtp_port)
            istls = get_field_value(smtp_cfg, "tls")
            if istls:
                # start TLS for security
                smtp_session.starttls()
            # Authentication
            smtp_session.login(user_name, user_pwd)
            msg = ("From: %s\r\nTo: %s\r\n\r\n %s\n"
             % (user_name, touser, message))
            # sending the mail
            smtp_session.sendmail(user_name, touser, msg)
            # terminating the session
            smtp_session.quit()
        except Exception as ex:
            logger.info('Email notification failed exception: %s!', ex)
    else:
        logger.info('Invalid email config for notification!')
