"Test controller for test invocation"
from flask import Blueprint, jsonify, request
from processor.api.app_init import app, LOGGER
from processor.api.utils import ERROR, OK, NOK, STATUS, VALUE
from processor.connector.validation import run_container_validation_tests_database
from processor.database.database import sort_field, get_documents

# Define the blueprint: 'test'
MODAPI = Blueprint('MODAPI', __name__, url_prefix=app.config['APIPREFIX'])

@MODAPI.route('/version/', methods=['POST', 'GET'])
def app_version():
    """Return the current version of the application"""
    data = {STATUS: OK, 'app': app.config['APPVERSION']}
    return jsonify(data)


@MODAPI.route('/tests/', methods=['POST'])
def run_framework_test():
    data = {STATUS: OK, VALUE: None}
    indata = request.json
    container = indata.get('container', None) if indata else None
    LOGGER.info('Input: %s', indata)
    # test = indata.get('test', None)
    if container:
        run_container_validation_tests_database(container)
        qry = {'container': container}
        sort = [sort_field('timestamp', False)]
        docs = get_documents('outputs', dbname='validator', sort=sort, query=qry)
        if docs:
            json = docs[0]['json']
            data[VALUE] = json
        else:
            data[VALUE] = []
    else:
        data[STATUS] = NOK
        data[ERROR] = 'Need a test container'
    return jsonify(data)
