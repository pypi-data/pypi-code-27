# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import hmac
import time
import hashlib
import os
import json
import logging

logger = logging.getLogger('adpushup_adstxt.utils')

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

revert = {"%21": "!", "%2A": "*", "%27": "'", "%28": "(", "%29": ")"}


def strtr(strng, replace):
    buffer = []
    i, n = 0, len(strng)
    while i < n:
        match = False
        for s, r in replace.items():
            if strng[i : len(s) + i] == s:
                buffer.append(r)
                i = i + len(s)
                match = True
                break
        if not match:
            buffer.append(strng[i])
            i = i + 1
    return "".join(buffer)


def encode_uri_component(value):
    return strtr(quote(value), revert)


def authenticate(req_hash, req_time, user_id, key):

    if int(time.time()) - int(req_time) > 5:
        return False

    hash_params = "email={}&ts={}".format(
        encode_uri_component(user_id.encode("UTF-8")), req_time)

    return req_hash == hmac.new(key, hash_params, hashlib.sha256).hexdigest()


def get_ads_txt(root_dir):

    try:
        data = open(os.path.join(root_dir, "ads.txt"), b"r").read()
        return 200, json.dumps(dict(status=1, data=data))
    except IOError:
        return 404, json.dumps(dict(status=0, status_message="No Ads.txt File"))


def set_ads_txt(root_dir, data):

    data = strtr(data, {"<": "", ">": "", "?": ""})
    file_name = os.path.join(root_dir, "ads.txt")
    try:
        with open(file_name, b"w") as f:
            f.write(data)
        logger.debug("% file written", file_name)

        return 200, json.dumps(dict(status=1, status_message="Ads.txt Updated"))
    except IOError as e:
        logger.exception('Could not write %s', file_name)
        return 500, json.dumps(dict(status=0, status_message="IOError"))
