import sys
import os
import requests
from urllib import parse
from http import HTTPStatus
import base64
import json
from pprint import pprint

HOST = 'api.epsonconnect.com'
ACCEPT = 'application/json;charset=utf-8'

def send_request(uri, data, headers, method):
    try:
        if method == 'POST':
            response = requests.post(uri, data=data, headers=headers)
        elif method == 'GET':
            response = requests.get(uri, headers=headers)
        elif method == 'PUT':
            response = requests.put(uri, data=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(uri, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")
        response.raise_for_status()
        return response, response.text, ''
    except requests.exceptions.HTTPError as err:
        return None, None, str(err.response.status_code) + ':' + err.response.reason + ':' + err.response.text
    except requests.exceptions.RequestException as err:
        return None, None, str(err)

AUTH_URI = 'https://' + HOST + '/api/1/printing/oauth2/auth/token?subject=printer'
CLIENT_ID = '0a3f010746cd4ddba09f82c83d571d9f'
SECRET = 'hvs8QQSLwFfzXWF6xhQjxcW2NAHe5kl8FwLImyRI1s5DoEdeBBCaEDzIbn3374lC'
#DEVICE = 'HACKSONIC_EW-M752T@print.epsonconnect.com'    # EW-M752T（Ｌ判～Ａ４）
DEVICE = 'HACKSONIC_EW-M973A3T@print.epsonconnect.com'  # EW-M973A3T（カード～Ａ３ノビ）
#DEVICE = 'HACKSONIC_PF-71@print.epsonconnect.com'       # PF-71（カード～Ａ５）


def print(filename):
    auth = base64.b64encode((CLIENT_ID + ':' + SECRET).encode()).decode()

    query_param = {
        'grant_type': 'password',
        'username': DEVICE,
        'password': ''
    }
    query_string = parse.urlencode(query_param)

    headers = {
        'Authorization': 'Basic ' + auth,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
    }
    res, body, err_str = send_request(AUTH_URI, query_string, headers, 'POST')
    pprint('1. Authentication: ---------------------------------')
    pprint(AUTH_URI)
    pprint(query_string)
    if res is None:
        pprint(err_str)
    else:
        pprint(str(res.status_code) + ':' + res.reason)
        pprint(json.loads(body))

    if err_str != '' or res.status_code != HTTPStatus.OK:
        sys.exit(1)

    # 2. Create print job

    subject_id = json.loads(body).get('subject_id')
    access_token = json.loads(body).get('access_token')

    job_uri = 'https://' + HOST + '/api/1/printing/printers/' + subject_id + '/jobs'

    data_param = {
        'job_name': 'SampleJob1',
        #'print_mode': 'document'
        'print_mode': 'photo',
        'print_setting': { 
            "media_size": "ms_l",
            "media_type": "mt_photopaper", 
            "borderless": False, 
            "print_quality": "high", 
            "source": "front1",             #########
            "color_mode": "color", 
            "2_sided": "none", 
            "reverse_order": False, 
            "copies": 1, 
            "collate": False 
        }
    }
    data = json.dumps(data_param)

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json;charset=utf-8'
    }

    res, body, err_str = send_request(job_uri, data, headers, 'POST')

    pprint('2. Create print job: -------------------------------')
    pprint(job_uri)
    pprint(data)
    if res is None:
        pprint(err_str)
    else:
        pprint(str(res.status_code) + ':' + res.reason)
        pprint(json.loads(body))

    if err_str != '' or res.status_code != HTTPStatus.CREATED:
        sys.exit(1)

    # 3. Upload print file

    job_id = json.loads(body).get('id')
    base_uri = json.loads(body).get('upload_uri')

    #local_file_path = './SampleDoc.pdf'
    local_file_path = filename

    _, ext = os.path.splitext(local_file_path)
    file_name = '1' + ext
    upload_uri = base_uri + '&File=' + file_name

    headers = {
        'Content-Length': str(os.path.getsize(local_file_path)),
        'Content-Type': 'application/octet-stream'
    }

    try:
        with open(local_file_path, 'rb') as f:
            res = requests.post(upload_uri, data=f, headers=headers)
            res.raise_for_status()
            body = res.text
    except requests.exceptions.HTTPError as err:
        err_str = str(err.response.status_code) + ':' + err.response.reason + ':' + err.response.text
    except requests.exceptions.RequestException as err:
        err_str = str(err)

    pprint('3. Upload print file: ------------------------------')
    pprint(base_uri)
    if res is None:
        pprint(err_str)
    else:
        pprint(str(res.status_code) + ':' + res.reason)

    if err_str != '' or res.status_code != HTTPStatus.OK:
        sys.exit(1)

    # 4. Execute print

    print_uri = 'https://' + HOST + '/api/1/printing/printers/' + subject_id + '/jobs/' + job_id + '/print'
    data=''

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json; charset=utf-8'
    }

    res, body, err_str = send_request(print_uri, data, headers, 'POST')

    pprint('4. Execute print: ----------------------------------')
    pprint(print_uri)
    if res is None:
        pprint(err_str)
    else:
        pprint(str(res.status_code) + ':' + res.reason)
        pprint(json.loads(body))

if __name__ == '__main__':
    #filename = './SampleDoc.pdf'
    #filename = 'uploads/e3bf3ea4-415b-48c9-a52e-36604e5800be.jpg'
    filename = 'uploads/fb531baf-a0b6-41a8-a59a-afc7905ea942.jpg'
    print(filename)
