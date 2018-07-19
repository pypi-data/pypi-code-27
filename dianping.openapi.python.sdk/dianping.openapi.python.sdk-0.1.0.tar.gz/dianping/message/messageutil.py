#! coding:utf-8

import uuid
import time
import dianping.sign
import urllib


def create_client_id():
    return uuid.uuid1()


def build_handle_snake_param(app, wsAdress, clientId):
    params = {
        'app_key': app.get_appKey(),
        'v': '1.0.0',
        'clientId': clientId,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
    }
    signstr = dianping.sign.sign(params, app.get_appSecret(), 'MD5')
    params['sign'] = signstr

    connectaddress = str(wsAdress) + '?'
    encode_params = urllib.urlencode(params)

    connectaddress = connectaddress + encode_params

    return connectaddress
