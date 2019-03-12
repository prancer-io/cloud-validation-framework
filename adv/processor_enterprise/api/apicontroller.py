"Test controller for test invocation"
import pymongo
from flask import Blueprint, jsonify, request
from processor_enterprise.api.app_init import app, LOGGER
from processor_enterprise.api.utils import ERROR, OK, NOK, STATUS, VALUE, parsebool
from processor.connector.validation import run_container_validation_tests_database
from processor.database.database import sort_field, get_documents, count_documents,\
    distinct_documents, DATABASE, DBNAME
from processor.helper.json.json_utils import collectiontypes, OUTPUT, TEST
from processor.helper.config.config_utils import config_value
from processor.connector.validation import run_json_validation_tests
from processor.reporting.json_output import dump_output_results
SORTDATE = 'date'
SORTFIELDS = {SORTDATE: 'timestamp'}


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


@MODAPI.route('/execute/<container>/', methods=['GET'])
@MODAPI.route('/execute/<container>/<name>/', methods=['GET'])
def tests_run(container, name=None):
    data = {STATUS: OK, VALUE: None}
    sort = [(SORTFIELDS[SORTDATE], pymongo.DESCENDING)]
    qry = {'container': container}
    limit = 10
    if name:
        qry['name'] = name
        limit = 1
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[TEST])
    docs = get_documents(collection, dbname=dbname,
                         sort=sort, query=qry, limit=limit)
    LOGGER.info('Number of test Documents: %s', len(docs))
    if docs and len(docs):
        for doc in docs:
            if doc['json']:
                resultset = run_json_validation_tests(doc['json'], container, False)
                data[VALUE] = resultset
                if resultset:
                    snapshot = doc['json']['snapshot'] if 'snapshot' in doc['json'] else ''
                    test_file = doc['name'] if 'name' in doc else ''
                    dump_output_results(resultset, container, test_file, snapshot, False)
    else:
        data[VALUE] = []
    return jsonify(data)


@MODAPI.route('/results/<container>/', methods=['GET'])
@MODAPI.route('/results/<container>/<name>/', methods=['GET'])
def outputs_container(container, name=None):
    data = {STATUS: OK, VALUE: None}
    indata = request.args if request.args else {}
    alldata = parsebool(indata['all']) if 'all' in indata else True
    sortval = indata.get('sort', SORTDATE)
    sortfield = SORTFIELDS[sortval] if sortval in SORTFIELDS else SORTFIELDS[SORTDATE]
    sort = [(sortfield, pymongo.DESCENDING)]
    qry = {'container': container}
    projection = {'_id': 0}
    if name:
        qry['name'] = name
    projection['json'] = 1 if alldata else 0
    size = int(request.args.get('pagesize', '10'))
    page = int(request.args.get('page', '0'))
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[OUTPUT])
    total = count_documents(collection, dbname=dbname, query=qry)
    docs = get_documents(collection, dbname=dbname, proj=projection,
                         sort=sort, query=qry, limit=size, skip=page*size)
    LOGGER.info('Number of test Documents: %s', len(docs))
    if docs and len(docs):
        data[VALUE] = docs
    else:
        data[VALUE] = []
    data['total'] = total
    data['page'] = page
    data['pagesize'] = size
    return jsonify(data)


@MODAPI.route('/containers/', methods=['GET'])
def container_list():
    data = {STATUS: OK, VALUE: None}
    dbname = config_value(DATABASE, DBNAME)
    collection = config_value(DATABASE, collectiontypes[OUTPUT])
    docs = distinct_documents(collection, dbname=dbname, field='container')
    LOGGER.info('Number of test Documents: %s', len(docs))
    data[VALUE] = docs
    return jsonify(data)