# -*- coding: utf-8 -*-
'''
Manage dingtalk tokens, for example access token.
'''
import time
import threading
from ..util.api import client
from ..util.data_store import DictStore


class TokenManager(object):
    def __init__(self, corp_id, corp_secret, agent_id=None,
                 token_store=None, token_lock=None):
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.agent_id = agent_id
        self.token_store = DictStore() if not token_store else token_store
        self.token_lock = threading.Lock() if not token_lock else token_lock

    def get_access_token(self):
        access_token = self.token_store.get('access_token') or {}
        if not access_token or access_token['expires'] <= time.time():
            resp = client.call('GET', '/gettoken', params={'corpid': self.corp_id,
                                                           'corpsecret': self.corp_secret})
            ret = resp.json()
            if ret['errcode'] == 0:
                access_token = {'value': ret['access_token'], 'expires': int(time.time()) + 7100}
            else:
                access_token = {}
            self.token_store.set('access_token', access_token)
        return access_token.get('value')

    def set_access_token(self, token):
        data = {'value': token,
                'expires': int(time.time()) + 3600}
        self.token_store.set('access_token', data)
