import os
import json
import base64
import shutil
import glob
from datetime import datetime
from zipfile import ZipFile, ZIP_BZIP2
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
                apiserver = os.environ['LOCALSERVER'] if 'LOCALSERVER' in os.environ else LOCALSERVER
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
        if 'name' in connector:
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

def encode_base64(data):
    databytes = data.encode('ascii')
    messagebytes = base64.b64encode(databytes)
    base64data = messagebytes.decode('ascii')
    return base64data

def read_in_chunks(file_object, chunk_size=65536):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield encode_base64(data)


def upload_file(container, content_path, content_name, url, logname, fileType, hdrs):
    content_size = os.stat(content_path).st_size
    f = open(content_path)

    index = 0
    offset = 0
    headers = hdrs

    data = read_in_chunks(f)
    chunk = next(data)
    moredata = True
    while True:
        offset = index + len(chunk)
        headers['User-Agent'] = 'Mozilla/5.0'
        # headers['Content-Type'] = 'application/octet-stream'
        # headers['Content-length'] = str(content_size)

        headers['Content-Type'] = 'application/json'
        nextdata = None
        data = read_in_chunks(f)
        try:
            nextdata = next(data)
        except StopIteration as ex:
            moredata = False

        # headers['Content-Range'] = '%s:%s:%s:%d:%s:%s:%s' % (content_name, index, offset,int(moredata), fileType, container, logname)
        index = offset
        try:
            # r = requests.post(url, data=chunk.encode('utf-8'), headers=headers)
            # print("r: %s, Content-Range: %s" % (r, headers['Content-Range']))
            rangeval = '%s:%s:%s:%d:%s:%s:%s' % (content_name, index, offset,int(moredata), fileType, container, logname)
            pdata = {
                'range': rangeval,
                'data': chunk
            }
            r = requests.post(url, data=json.dumps(pdata), headers=headers)
            print("r: %s, range: %s" % (r, rangeval))
        except Exception as e:
            print(e)
        if not moredata:
            break
        chunk = nextdata


def upload_file_multipart(container, content_path, content_name, url, logname, fileType, hdrs, upload_id=None, timestamp=None):
    fileUploaded = False
    headers = hdrs
    headers['User-Agent'] = 'Mozilla/5.0'
    rangeval = '%s:%s:%s:%s:%s' % (content_name, upload_id if upload_id else '', fileType, container, logname)
    with ZipFile(content_name + '.zip', 'w', compression=ZIP_BZIP2) as zf:
        zf.write(content_path, content_name)

    mpdata = {
        'file': (content_name + '.zip', open(content_name + '.zip', 'rb')),
        'uploadid': (None, upload_id if upload_id else ''),
    }
    if timestamp:
        mpdata["timestamp"] = timestamp
    try:
        response = requests.post(url, files=mpdata, headers=headers)
        if response.status_code == 200:
            fileUploaded = True
        else:
            print("response: %s, range: %s" % (response, rangeval))
    except Exception as e:
        print(e)
    return fileUploaded


def upload_complete_process(container, uploadid, url, completedata, hdrs):
    headers = hdrs
    headers['User-Agent'] = 'Mozilla/5.0'
    headers['Content-Type'] = 'application/json'
    data = {
        'container': container,
        'uploadid': uploadid,
        'files': completedata
    }
    try:
        resp = requests.post(url, data=json.dumps(data), headers=headers)
        if resp.status_code == 200:
            print('Uploaded remote results for container: %s successfully!' % container)
        else:
            print('Uploading remote results for container: %s failed: %d' % (container, resp.status_code))
    except Exception as e:
        print(e)


# def upload_compliance_results_chunk(container, opath, server, company, apitoken):
def upload_compliance_results(container, opath, server, company, apitoken):
    from processor.logging.log_handler import FWLOGFILENAME
    fname = FWLOGFILENAME
    name = fname.rsplit('/', 1)
    logs = name[-1].split('.')
    oname = opath.rsplit('/', 1)
    ts = None
    uploadid = 'upload_%s_%s' % (container.replace(' ', '_'), datetime.utcnow().strftime('%d%m%Y%H%M%s'))
    fileUploaded = False
    apiserver = get_api_server(server, company)
    if apiserver:
        collectionUri = get_collection_api(apiserver)
        hdrs = {
            "Authorization": "Bearer %s" % apitoken
        }
        completedata = []
        if exists_file(fname):
            fileUploaded = upload_file_multipart(container, fname, name[-1], collectionUri, logs[0],
                                                 'log', hdrs, upload_id=uploadid, timestamp=ts)
            completedata.append({
                'filename': name[-1],
                'filetype': 'log',
                'log': logs[0]
            })
        snapshotfilenames = {}
        if fileUploaded and exists_file(opath):
            ofilenames = []
            odir = oname[0]
            for filename in glob.glob('%s/output*.json' % odir.replace('//', '/')):
                sjson = json_from_file(filename)
                if sjson and 'snapshot' in sjson:
                    snapshot = '%s.json' % sjson['snapshot']
                    snapshotpath = os.path.join('', odir, snapshot)
                    snapshotfilenames[snapshotpath] = snapshot
                    ofilenames.append(filename)
            for ofile in ofilenames:
                ofilename = ofile.rsplit('/', 1)
                fileUploaded = upload_file_multipart(container, ofile, ofilename[-1], collectionUri, logs[0],
                                                     'output', hdrs, upload_id=uploadid, timestamp=ts)
                completedata.append({
                    'filename': ofilename[-1],
                    'filetype': 'output',
                    'log': logs[0]
                })
                if not fileUploaded:
                    break
        if fileUploaded and snapshotfilenames:
            for sfilepath, sfilename in snapshotfilenames.items():
                fileUploaded = upload_file_multipart(container, sfilepath, sfilename, collectionUri, logs[0],
                                                     'snapshot', hdrs, upload_id=uploadid, timestamp=ts)
                completedata.append({
                    'filename': sfilename,
                    'filetype': 'snapshot',
                    'log': logs[0]
                })
                if not fileUploaded:
                    break
        upload_complete_process(container, uploadid, collectionUri, completedata, hdrs)
    return fileUploaded
