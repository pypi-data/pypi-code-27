# coding=utf-8
import decimal
import json
import logging
import urllib
import urllib2
import urlparse
from datetime import datetime, date, time
from httplib import HTTPException, UNAUTHORIZED, FORBIDDEN, NOT_FOUND
from socket import error

import dateutil.parser
from tornado.options import options

import model
from providers.base import ACTIVE_DIRECTORY_USER_ID
from components.service import SyncUtils


class JSONEncoder(json.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, o):
        if hasattr(o, '__json__'):
            return o.__json__()
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, date):
            return o.strftime(JSONEncoder.DATE_FORMAT)
        elif isinstance(o, time):
            return o.strftime(JSONEncoder.TIME_FORMAT)
        elif isinstance(o, decimal.Decimal) or repr(type(o)) == repr(decimal.Decimal):
            # the second part added as a work around for google app engine sdk bug
            # https://groups.google.com/forum/#!topic/google-appengine-stackoverflow/7-tRlyt31Ic
            return float(o)
        else:
            return super(JSONEncoder, self).default(o)

    def encode(self, o):
        return super(JSONEncoder, self).encode(o)


class JSON(object):
    @staticmethod
    def custom_decoder(o):
        if type(o) is not dict:
            return o
        new = {}
        for key, val in o.iteritems():
            if key.endswith('_dt') or key.endswith('_dttm'):
                try:
                    val = dateutil.parser.parse(val)
                except:
                    pass
            new[key] = val
        return new

    @staticmethod
    def encode(obj, **kwargs):
        kwargs.setdefault('cls', JSONEncoder)
        kwargs.setdefault('indent', None)
        kwargs.setdefault('separators', (',', ':'))
        return json.dumps(obj, **kwargs)

    @staticmethod
    def decode(text, **kwargs):
        try:
            kwargs.setdefault('parse_float', decimal.Decimal)
            kwargs.setdefault('object_hook', JSON.custom_decoder)
            obj = json.loads(text, **kwargs)
        except Exception as e:
            logging.warning("Failed to decode text as JSON: '%s'", text)
            raise e
        else:
            return obj


def join_urls(root_url, part_url):
    if root_url.endswith('/') and part_url.startswith('/'):
        return '{}{}'.format(root_url[:-1], part_url)
    elif root_url.endswith('/') or part_url.startswith('/'):
        return '{}{}'.format(root_url, part_url)
    else:
        return '{}/{}'.format(root_url, part_url)


def make_request(root_url, part_url, data=None, headers={}, method=None, json_type=True, json_response=True,
                 user_id=None):
    url = join_urls(root_url, part_url)
    if json_type:
        data = JSON.encode(data)
        headers['Content-Type'] = 'application/json'
    else:
        if data:
            if isinstance(data, dict):
                for k, v in data.iteritems():
                    if isinstance(v, basestring):
                        data[k] = v.encode('utf-8') if isinstance(v, unicode) else v
            data = urllib.urlencode(data)
    # body and result variables have the same names
    # can't copy unsupported type
    log = {"data_3": "Body: " + SyncUtils.strigify(data)}
    http = urllib2.Request(url, data, headers)
    if method:
        http.get_method = lambda: method
    try:
        response = urllib2.urlopen(http, timeout=60)
    except urllib2.HTTPError as e:  # if HTTP status is not 200
        response = e.read()
        if e.code in [UNAUTHORIZED, FORBIDDEN]:
            raise ValueError('You are not authorised to access this page %s' % response)
        elif e.code == NOT_FOUND:
            raise ValueError('Resource not found: %s' % response)
        else:
            raise ValueError('Invalid OAuth2 response: %s' % response)
    except error:
        hostname = urlparse.urlparse(url)
        raise ValueError('Cannot access %s' % hostname.netloc)
    except (HTTPException, error) as e:
        raise ValueError('Invalid OAuth2 response: %s' % e.message)
    data = response.read()
    if data and json_response:
        try:
            data = json.loads(data)
        except ValueError:
            raise ValueError('Invalid OAuth2 response: %s' % data)
    if options.log_slack_requests:
        log.update({"operation": "slack request",
                    ACTIVE_DIRECTORY_USER_ID: user_id,
                    "success": True,
                    "message": "Request to slack was sent",
                    "data_1": "Url: " + url,
                    "data_2": "Headers: " + SyncUtils.strigify(headers),
                    "data_4": "Response: " + SyncUtils.strigify(data)})
        model.Log.add_log(**log)
    return data

