import os
import shutil
import requests
import urllib.parse
from processor.helper.json.json_utils import save_json_to_file, json_from_file
from processor.helper.config.config_utils import config_value, framework_dir
from processor.helper.file.file_utils import mkdir_path, remove_file, exists_file
from processor.logging.log_handler import getlogger

LOCAL='LOCAL'
DEV='DEV'
QA='QA'
PROD='PROD'
SERVERENVS = [LOCAL, DEV, QA, PROD]

LOCALSERVER='http://localhost:8080/api/'
SERVERS = {
    DEV: 'portaldev',
    QA: 'portalqa',
    PROD: 'portal'
}
COLLECTIONAPI = 'vs/container/'
VALIDATIONAPI = 'validate/accesstoken/'

logger = getlogger()

def get_company_prefix(company):
    company_prefix = company
    if company and not company.startswith('prancer-'):
        company_prefix = 'prancer-%s' % company
    return company_prefix


def get_api_server(server, company):
    apiserver = None
    if server:
        if server in SERVERENVS:
            if server == LOCAL:
                apiserver = LOCALSERVER
            else:
                if company:
                    company_prefix = get_company_prefix(company)
                    apiserver = 'https://%s.prancer.io/%s/api/' % (SERVERS[server], company_prefix)
    return apiserver

def get_validate_token_api(apiserver):
    validationApi = None
    if apiserver:
        validationApi = apiserver + VALIDATIONAPI
    return validationApi

def get_collection_api(apiserver, collection=None):
    collectionApi = None
    if apiserver:
        collectionApi = apiserver + COLLECTIONAPI
        if collection:
         collectionApi = collectionApi + '?collection=' + urllib.parse.quote_plus(collection)
    return collectionApi


def create_container_compliance(container, data):
    """ Create mastersnapshot, mastertest and connectors for the container in the framework directory"""
    validFolder = config_value('TESTS', 'containerFolder')
    validpath = '%s/%s/%s' % (framework_dir(), validFolder, container)
    strFolder = config_value('AZURE', 'azureStructureFolder')
    if strFolder:
        strpath = '%s/%s' % (framework_dir(), strFolder)
        mkdir_path(strpath)
    else:
        strpath = '%s/%s/..' % (framework_dir(), validFolder)
    shutil.rmtree(validpath, ignore_errors=True)
    mkdir_path(validpath)
    outputpath = None
    for connector in data['connectors']:
        cname = '%s/%s.json' % (strpath, connector['name'])
        remove_file(cname)
        save_json_to_file(connector['json'], cname)
    for mastersnapshot in data['masersnapshots']:
        cname = '%s/%s.json' % (validpath, mastersnapshot['name'])
        remove_file(cname)
        save_json_to_file(mastersnapshot['json'], cname)
    for mastertest in data['mastertests']:
        cname = '%s/%s.json' % (validpath, mastertest['name'])
        outputpath = '%s/output-%s.json' % (validpath, mastertest['name'])
        remove_file(cname)
        save_json_to_file(mastertest['json'], cname)
    for exclusion in data['exclusions']:
        cname = '%s/exclusions.json' % validpath
        remove_file(cname)
        save_json_to_file(exclusion, cname)
    return outputpath

# def upload_compliance_results(container, opath, server, company, apitoken):
def upload_compliance_results_multipart(container, opath, server, company, apitoken):
    from processor.logging.log_handler import get_dblog_name, FWLOGFILENAME, FWLOGGER
    dlog = get_dblog_name()
    fname = FWLOGFILENAME
    name = fname.rsplit('/', 1)
    oname = opath.rsplit('/', 1)
    apiserver = get_api_server(server, company)
    if apiserver:
        collectionUri = get_collection_api(apiserver)
        hdrs = {
            "Authorization": "Bearer %s" % apitoken
        }
        files = (
            ('collection', (None, container)),
            ('log', ('logs_' + name[-1], open(fname, 'r'), 'application/octet-stream', {'Expires': '0', 'chunk': 0})),
            ('output', (oname[-1], open(opath, 'r'), 'application/octet-stream', {'Expires': '0'}))
        )
        resp = requests.post(collectionUri, headers=hdrs, files=files)
        if resp.status_code == 200:
            logger.info(resp.json())

def read_in_chunks(file_object, chunk_size=65536):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def upload_file(container, content_path, content_name, url, logname, fileType, hdrs):
    # content_name = str(file)
    # content_path = os.path.abspath(file)
    content_size = os.stat(content_path).st_size

    # logger.info(content_name, content_path, content_size)

    f = open(content_path)

    index = 0
    offset = 0
    headers = hdrs
    # paths = content_name.rsplit('/', 1)

    data = read_in_chunks(f)
    chunk = next(data)
    moredata = True
    while True:
        offset = index + len(chunk)
        headers['Content-Type'] = 'application/octet-stream'
        headers['Content-length'] = str(content_size)
        nextdata = None
        data = read_in_chunks(f)
        try:
            nextdata = next(data)
        except StopIteration as ex:
            moredata = False

        # Content-Range'] = '<filename>:<offset start>:<offset end>:<0:file end, 1: file more> :<log|output|snapshot> :<container>:<logname>
        headers['Content-Range'] = '%s:%s:%s:%d:%s:%s:%s' % (content_name, index, offset,int(moredata), fileType, container, logname)
        index = offset
        try:
            r = requests.post(url, data=chunk.encode('utf-8'), headers=headers)
            # print("r: %s, Content-Range: %s" % (r, headers['Content-Range']))
        except Exception as e:
            print(e)
        if not moredata:
            break
        chunk = nextdata

# def upload_compliance_results_chunk(container, opath, server, company, apitoken):
def upload_compliance_results(container, opath, server, company, apitoken):
    from processor.logging.log_handler import get_dblog_name, FWLOGFILENAME, FWLOGGER
    fname = FWLOGFILENAME
    name = fname.rsplit('/', 1)
    logs = name[-1].split('.')
    oname = opath.rsplit('/', 1)
    ojson = json_from_file(opath)
    snapshotpath = None
    snapshot = None
    if ojson and 'snapshot' in ojson:
        snapshot = '%s.json' % ojson['snapshot']
        snapshotpath = os.path.join('', oname[0], snapshot)
        ojson = None
    apiserver = get_api_server(server, company)
    if apiserver:
        collectionUri = get_collection_api(apiserver)
        hdrs = {
            "Authorization": "Bearer %s" % apitoken
        }
        if exists_file(fname):
            upload_file(container, fname, name[-1], collectionUri, logs[0], 'log', hdrs)
        if exists_file(opath):
            upload_file(container, opath, oname[-1], collectionUri, logs[0], 'output', hdrs)
        if snapshot and snapshotpath and exists_file(snapshotpath):
            upload_file(container, snapshotpath, snapshot, collectionUri, logs[0], 'snapshot', hdrs)