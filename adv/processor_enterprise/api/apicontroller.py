"Test controller for test invocation"
import pymongo
import string
import random
from flask import Blueprint, jsonify, request
from processor_enterprise.api.app_init import app, LOGGER, scheduler
from processor_enterprise.api.utils import ERROR, OK, NOK, STATUS, VALUE, parsebool
from processor.connector.validation import run_container_validation_tests_database
from processor.database.database import sort_field, get_documents, count_documents,\
    distinct_documents, DATABASE, DBNAME
from processor.helper.json.json_utils import collectiontypes, OUTPUT, TEST
from processor.helper.config.config_utils import config_value
from processor.connector.validation import run_json_validation_tests
from processor.reporting.json_output import dump_output_results
from processor_enterprise.api.parser_scheduler_value import parse_value
SORTDATE = 'date'
SORTFIELDS = {SORTDATE: 'timestamp'}


# Define the blueprint: 'test'
MODAPI = Blueprint('MODAPI', __name__, url_prefix=app.config['APIPREFIX'])

def myjob(indata, idstr):
    LOGGER.info("Scheduled job invoked!: %s, %s", idstr, indata)


def reschedule_action(indata):
   LOGGER.info("Add the job")
   schedule_val = indata['schedule']
   alarm_time, trigger_values = parse_value(schedule_val)
   id_str = "" + str(indata["id"])
   if schedule_val.startswith('once'):
       job_val = scheduler.add_job(myjob, 'date', id=id_str, args=[indata, id_str], **trigger_values)
   else:
       trigger_values['start_date'] = alarm_time
       job_val = scheduler.add_job(myjob, 'cron', id=id_str, args=[indata, id_str], **trigger_values)
   LOGGER.info("Trigger values: %s", trigger_values)
   return job_val

def add_action(indata, name):

   LOGGER.info("Add the job")
   schedule_val = indata['schedule']
   alarm_time, trigger_values = parse_value(schedule_val)
   # trigger_values['name'] = name
   id_str = "" + str(indata["id"]) if 'id' in indata else generateid(name)
   if schedule_val.startswith('once'):
       job_val = scheduler.add_job(myjob, 'date', name=name, id=id_str, args=[indata, id_str], **trigger_values)
   else:
       trigger_values['start_date'] = alarm_time
       job_val = scheduler.add_job(myjob, 'cron', name=name, id=id_str, args=[indata, id_str], **trigger_values)
   LOGGER.info("Trigger values: %s", trigger_values)
   return job_val


def generateid(name):
    pwdSize = 5
    digits = False
    chars = string.digits if digits else string.ascii_letters
    numval = (random.choice(chars) for x in range(pwdSize))
    pwdSize = 4
    digits = True
    chars1 = string.digits if digits else string.ascii_letters
    charval = (random.choice(chars1) for x in range(pwdSize))
    idval = '%s_%s_%s' % (name, ''.join(numval), ''.join(charval))
    return idval.lower()


def delete_action(indata):
   LOGGER.info("Delete the job")
   id_str = "" + str(indata["id"])
   try:
       scheduler.remove_job(id_str)
       return True
   except:
       pass
   return False


@MODAPI.route('/jobs/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def jobs_scheduled():
    """Return the jobs scheduled"""
    LOGGER.info("Method: %s, %s", request.method, request.json)
    jbs = []
    data = {STATUS: NOK, 'jobs': jbs}
    if request.method == 'POST':
        indata = request.json
        container = indata.get('container', None) if indata else None
        LOGGER.info('Input: %s', indata)
        if container:
           status, job = add_action(indata, container)
           val = {
               'id': job.id,
               'name': job.name,
               'next_run_time': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')
           }
           jbs.append(val)
           data = {STATUS: status, 'jobs': jbs}
    elif request.method == 'DELETE':
        indata = request.json
        idval = indata.get('id', None) if indata else None
        LOGGER.info('Input: %s', idval)
        st = OK if delete_action(indata) else NOK
        data = {STATUS: st, 'jobs': jbs}
    else:
        jobs = scheduler.get_jobs()
        for job in jobs:
            val = {
            'id': job.id,
            # 'args': job.args,
            'name': job.name,
            'next_run_time': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            jbs.append(val)
        # print(jobs)
        data = {STATUS: OK, 'jobs': jbs}
    return jsonify(data)


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