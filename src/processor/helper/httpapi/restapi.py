"""all the base functions for making REST API calls"""
import json
import logging
import requests

logger = logging.getLogger(__name__)


jsonhdr = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def json_delete_request(url, deldata=None, headers=None, log=False):
    "Delete method sends and accepts JSON format without basic authenication"
    if log: print("Deleting %s  ......." % url)
    data = None
    st_code = None
    if headers:
        headers.update(jsonhdr)
    else:
        headers = jsonhdr
    if url: #Do something only valid URL
        if deldata:
            resp = requests.delete(url, data=json.dumps(deldata), headers=headers, timeout=30)
        else:
            resp = requests.delete(url, headers=headers, timeout=30)
        if log: print("Get response: %s" % resp)
        st_code = resp.status_code
        try:
            data = resp.json()
        except Exception as e:
            logger.warning("Error parsing JSON response from DELETE %s: %s", url, str(e))
    else:
        pass # Do nothing.
    return st_code, data


def json_get_request(url, headers=None, log=False):
    "Get method sends and accepts JSON format without basic authenication"
    if log: print("Getting %s  ......." % url)
    data = None
    st_code = None
    if headers:
        headers.update(jsonhdr)
    else:
        headers = jsonhdr
    if url: #Do something only valid URL
        resp = requests.get(url, headers=headers, timeout=30)
        if log: print("Get response: %s" % resp)
        st_code = resp.status_code
        try:
            data = resp.json()
        except Exception as e:
            logger.warning("Error parsing JSON response from GET %s: %s", url, str(e))
    else:
        pass # Do nothing.
    return st_code, data


def json_put_request(url, mapdata, headers=None, log=False):
    "Put method sends and accepts JSON format without basic authenication"
    if log: print("Putting %s  ......." % url)
    data = None
    st_code = None
    if headers:
        headers.update(jsonhdr)
    else:
        headers = jsonhdr
    if url: #Do something only valid URL
        resp = requests.put(url, data=json.dumps(mapdata), headers=headers, timeout=30)
        if log: print("Get response: %s" % resp)
        st_code = resp.status_code
        try:
            data = resp.json()
        except Exception as e:
            logger.warning("Error parsing JSON response from PUT %s: %s", url, str(e))
    else:
        pass # Do nothing.
    return st_code, data


def json_post_request(url, mapdata, headers=None, log=False):
    "Post method sends and accepts JSON format without basic authenication"
    if log: print("Posting %s  ......." % url)
    data = None
    st_code = None
    if headers:
        headers.update(jsonhdr)
    else:
        headers = jsonhdr
    if url: #Do something only valid URL
        resp = requests.post(url, data=json.dumps(mapdata), headers=headers, timeout=30)
        if log: print("Get response: %s" % resp)
        st_code = resp.status_code
        try:
            data = resp.json()
        except Exception as e:
            logger.warning("Error parsing JSON response from POST %s: %s", url, str(e))
    else:
        pass # Do nothing.
    return st_code, data
