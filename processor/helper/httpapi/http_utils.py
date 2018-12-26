"""
   http utils using urllib default packaged with python3.
"""
import json
from urllib import request, parse
from urllib.error import HTTPError
from processor.helper.json.json_utils import load_json_input
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import put_in_currentdata

logger = getlogger()
hdrs = {
    'Cache-Control': "no-cache",
    "Accept": "application/json"
}


def check_and_add_error(status, errmsg):
    if status and isinstance(status, int) and status != 200:
        if status >= 400:
            put_in_currentdata('errors', errmsg)
        logger.info(errmsg)


def http_delete_request(url, deldata=None, headers=None):
    "Delete method sends and accepts JSON format with basic authentication"
    logger.info("Deleting %s  .......", url)
    data = None
    st_code = None
    if headers:
        headers.update(hdrs)
    else:
        headers = hdrs
    logger.info('DELETE: header: %s, url: %s', json.dumps(headers), url)
    if url: #Do something only valid URL
        if deldata:
            encdata = parse.urlencode(deldata).encode()
            logger.info('DELETE: data: %s', encdata)
            urlreq = request.Request(url, data=encdata, headers=headers,
                                     method='DELETE')
        else:
            urlreq = request.Request(url, headers=headers, method='DELETE')
        try:
            urlresp = request.urlopen(urlreq)
            respdata = urlresp.read()
            logger.info("DELETE status: %d, response: %s", urlresp.status, respdata)
            st_code = urlresp.status
            check_and_add_error(st_code, "Delete Status: %d" % st_code)
            if isinstance(respdata, bytes):
                respdata = respdata.decode()
            data = load_json_input(respdata)
        except:
            pass # Can we do anything here, not anything i can think of immediately
    else:
        pass # Do nothing.
    return st_code, data


def http_get_request(url, headers=None):
    "Get method sends and accepts JSON format."
    logger.info("Getting %s  .......", url)
    data = None
    st_code = None
    if headers:
        headers.update(hdrs)
    else:
        headers = hdrs
    logger.debug('GET: header: %s, url: %s', json.dumps(headers), url)
    if url: #Do something only valid URL
        try:
            urlreq = request.Request(url, headers=headers, method='GET')
            urlresp = request.urlopen(urlreq)
            respdata = urlresp.read()
            logger.debug("GET status: %d, response: %s", urlresp.status, respdata)
            st_code = urlresp.status
            check_and_add_error(st_code, "Get Status: %d" % st_code)
            if isinstance(respdata, bytes):
                respdata = respdata.decode()
            data = load_json_input(respdata)
        except:
            pass # Can we do anything here, not anything i can think of immediately
    else:
        pass # Do nothing.
    return st_code, data


def http_put_request(url, mapdata, headers=None):
    "Put method sends and accepts JSON format."
    logger.info("Putting %s  .......", url)
    data = None
    st_code = None
    if headers:
        headers.update(hdrs)
    else:
        headers = hdrs
    logger.info('PUT: header: %s, url: %s', json.dumps(headers), url)
    if url: #Do something only valid URL
        putdata = parse.urlencode(mapdata).encode()
        logger.info('PUT: data: %s', putdata)
        urlreq = request.Request(url, data=putdata, headers=headers,
                                 method='PUT')
        try:
            urlresp = request.urlopen(urlreq)
            respdata = urlresp.read()
            logger.info("PUT status: %d, response: %s", urlresp.status, respdata)
            st_code = urlresp.status
            check_and_add_error(st_code, "Put Status: %d" % st_code)
            if isinstance(respdata, bytes):
                respdata = respdata.decode()
            data = load_json_input(respdata)
        except:
            pass # Can we do anything here, not anything i can think of immediately
    else:
        pass # Do nothing.
    return st_code, data


def http_post_request(url, mapdata, headers=None, json_type=False):
    "Post method sends and accepts JSON format"
    logger.info("Posting %s  .......", url)
    data = None
    st_code = None
    if not headers:
        headers = hdrs
    logger.info('POST: header: %s, url: %s', json.dumps(headers), url)
    if url: #Do something only valid URL
        try:
            if json_type:
                postdata = str.encode(json.dumps(mapdata))
            else:
                postdata = parse.urlencode(mapdata).encode()
            logger.debug('POST: data: %s', postdata)
            urlreq = request.Request(url, data=postdata, headers=headers,
                                     method='POST')
            urlresp = request.urlopen(urlreq)
            respdata = urlresp.read()
            logger.debug("POST status: %d, response: %s", urlresp.status, respdata)
            st_code = urlresp.status
            check_and_add_error(st_code, "POST status: %d" % st_code)
            if isinstance(respdata, bytes):
                respdata = respdata.decode()
            data = load_json_input(respdata)
        except HTTPError as ex:
            st_code = ex.code
            data = ex.msg
            logger.info("POST status: %d, response: %s", st_code, data)
    else:
        pass # Do nothing.
    return st_code, data
