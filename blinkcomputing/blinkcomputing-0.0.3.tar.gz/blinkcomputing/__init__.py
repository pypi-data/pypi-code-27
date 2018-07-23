# Copyright 2018 Blink Computing Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import time


class Connection:
    def __init__(self, cluster_id, coord_host, user_name, password, session=None,
                 stop_on_close=False, console_url=None):
        assert not stop_on_close or console_url is not None
        self._cluster_id = cluster_id
        self._coord_host = coord_host
        self._user_name = user_name
        self._password = password
        self._session = session
        self._stop_on_close = stop_on_close
        self._console_url = console_url

    #def GetIbisConnection(self):
    def GetDbapiConnection(self):
        import impala.dbapi
        return impala.dbapi.connect(
            host=self._coord_host, use_ssl=True, auth_mechanism='PLAIN', user='admin',
            password='admin')

    def GetIbisConnection(self):
        import ibis.impala
        return ibis.impala.connect(
            host=self._coord_host, port=21050, hdfs_client=None, use_ssl=True,
            auth_mechanism='PLAIN', user='admin', password='admin')

    def Close(self):
        if not self._stop_on_close:
            return
        # stop cluster
        stop_data = {'id':self._cluster_id}
        stop_url = '{}/rpc/StopCluster'.format(self._console_url)
        res = self._session.post(stop_url, data=stop_data,
                                 headers={'X-CSRFToken':self._session.cookies['csrftoken'],
                                          'Referer':stop_url})
        if res.status_code != requests.codes.ok:
            raise Error('stop failed')

class Error(Exception):
    def __init__(self, msg):
        self.msg = msg

def Connect(account=None, user_name=None, password=None, cluster_name=None, test=False):
    assert account is not None
    assert user_name is not None
    assert password is not None
    assert cluster_name is not None

    if test:
        console_url = 'http://localhost:8000'
    else:
        console_url = 'https://prod-console.dev.leodata.io'

    # log in
    session = requests.Session()
    login_data = {'account_name':account, 'user_name':user_name, 'password':password}
    res = session.post('{}/rpc/LogIn'.format(console_url), data=login_data)
    if res.status_code != requests.codes.ok:
        raise Error('login failed')
    csrf_token = session.cookies['csrftoken']

    # get cluster id
    get_data = {'name':cluster_name}
    get_url = '{}/rpc/GetClusters'.format(console_url)
    res = session.post(get_url, data=get_data, headers={'X-CSRFToken':csrf_token, 'Referer':get_url})
    if res.status_code != requests.codes.ok or len(res.json()) == 0:
        raise Error('unknown cluster: {}'.format(cluster_name))
    cluster = res.json()[0]
    if cluster['state'] == 1:
        # it's already running
        return Connection(cluster['id'], cluster['coord_host'], user_name, password,
                          session=session, stop_on_close=False)
    if cluster['state'] != 4:
        # it's something other than stopped, we can't start it
        raise Error('cluster {} is not stopped'.format(cluster_name))

    # start cluster
    start_data = {'id':cluster['id']}
    start_url = '{}/rpc/StartCluster'.format(console_url)
    res = session.post(start_url, data=start_data, headers={'X-CSRFToken':csrf_token, 'Referer':start_url})
    if res.status_code != requests.codes.ok:
        raise Error('start failed')
    cluster = res.json()

    # loop until the cluster is running and coord_host is set
    while cluster['state'] == 0 or cluster['coord_host'] is None:
        time.sleep(10)
        # get cluster state
        res = session.post(get_url, data=get_data, headers={'X-CSRFToken':csrf_token, 'Referer':get_url})
        if res.status_code != requests.codes.ok or len(res.json()) == 0:
            raise Error('error getting cluster state')
        cluster = res.json()[0]
        if cluster['state'] == 1 and cluster['coord_host'] is not None:
            return Connection(cluster['id'], cluster['coord_host'], user_name, password,
                              session=session, stop_on_close=True, console_url=console_url)
