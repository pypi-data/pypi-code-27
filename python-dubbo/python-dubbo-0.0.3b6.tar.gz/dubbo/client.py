# -*- coding: utf-8 -*-
import logging
import threading
import time
from random import randint
from urllib import quote

from kazoo.client import KazooClient

from dubbo.common.constants import DUBBO_ZK_PROVIDERS, DUBBO_ZK_CONFIGURATORS, DUBBO_ZK_CONSUMERS
from dubbo.common.exceptions import RegisterException
from dubbo.common.util import parse_url, get_pid, get_ip
from connection.connections import connection_pool

logger = logging.getLogger('dubbo')


class DubboClient(object):
    """
    用于实现dubbo调用的客户端
    """

    def __init__(self, interface, version='1.0.0', dubbo_version='2.4.10', zk_register=None, host=None):
        """
        :param interface: 接口名，例如：com.qianmi.pc.es.api.EsProductQueryProvider
        :param version: 接口的版本号，例如：1.0.0，默认为1.0.0
        :param dubbo_version: dubbo的版本号，默认为2.4.10
        :param zk_register: zookeeper注册中心管理端，参见类：ZkRegister
        :param host: 远程主机地址，用于绕过zookeeper进行直连，例如：172.21.4.98:20882
        """
        if not zk_register and not host:
            raise RegisterException('zk_register和host至少需要填入一个')

        self.__interface = interface
        self.__version = version
        self.__dubbo_version = dubbo_version

        self.__zk_register = zk_register
        self.__host = host

    def call(self, method, args=(), timeout=None):
        """
        执行远程调用
        :param method: 远程调用的方法名
        :param args: 方法参数
                    1. 对于没有参数的方法，此参数不填；
                    2. 对于只有一个参数的方法，直接填入该参数；
                    3. 对于有多个参数的方法，传入一个包含了所有参数的列表；
                    4. 当前方法参数支持以下类型：
                        * bool
                        * int
                        * long
                        * float
                        * double
                        * java.lang.String
                        * java.lang.Object
        :param timeout: 请求超时时间（秒），不设置则不会超时。默认不设置，如无特殊需求不建议设置
                    * 不设置超时时间在某些极限情况下可能导致此连接一直阻塞；
                    * 设置超时时间会增加远程调用的时间；
        :return:
        """
        if not isinstance(args, (list, tuple)):
            args = [args]

        if self.__zk_register:  # 优先从zk中获取provider的host
            host = self.__zk_register.get_provider_host(self.__interface)
        else:
            host = self.__host
        # logger.debug('get host {}'.format(host))

        request_param = {
            'dubbo_version': self.__dubbo_version,
            'version': self.__version,
            'path': self.__interface,
            'method': method,
            'arguments': args
        }
        # logger.debug(request_param)
        result = connection_pool.get(host, request_param, timeout)
        return result


class ZkRegister(object):
    """
    ZkRegister的主要作用：
    1. 根据特定的interface从zk中取出与之相关的所有provider的host并且监听
       provider的变化，当发生变化时更新最新的hosts到本地缓存；
    2. 当从zk中获取指定的interface的provider的时候，把当前进程作为此interface
       的一个consumer注册到zk中，并设置此节点的状态为ephemeral；
    """

    def __init__(self, hosts, application_name='search_platform'):
        """
        :param hosts: Zookeeper的地址
        :param application_name: 当前客户端的名称
        """
        zk = KazooClient(hosts=hosts)
        zk.start()

        self.zk = zk
        self.hosts = {}
        self.weights = {}
        self.application_name = application_name
        self.lock = threading.Lock()

    def get_provider_host(self, interface):
        """
        从zk中可以根据接口名称获取到此接口某个provider的host
        :param interface:
        :return:
        """
        if interface not in self.hosts:
            self.lock.acquire()
            if interface not in self.hosts:
                path = DUBBO_ZK_PROVIDERS.format(interface)
                if self.zk.exists(path):
                    providers = self.zk.get_children(path, watch=self._watch_children)
                    providers = filter(lambda provider: provider['scheme'] == 'dubbo', map(parse_url, providers))
                    if len(providers) == 0:
                        raise RegisterException('no providers for interface {}'.format(interface))
                    self._register_consumer(providers)
                    self.hosts[interface] = map(lambda provider: provider['host'], providers)

                    # 试图从配置中取出权重相关的信息
                    configurators = self.zk.get_children(DUBBO_ZK_CONFIGURATORS.format(interface),
                                                         watch=self._watch_configurators)
                    if configurators:
                        configurators = map(parse_url, configurators)
                        conf = {}
                        for configurator in configurators:
                            conf[configurator['host']] = configurator['fields'].get('weight', 100)  # 默认100
                        self.weights[interface] = conf
                else:
                    raise RegisterException('can\'t providers for interface {0}'.format(interface))
            self.lock.release()
        return self._routing_with_wight(interface)

    def _routing_with_wight(self, interface):
        """
        根据接口名称以及配置好的权重信息获取一个host
        :param interface:
        :return:
        """
        hosts = self.hosts[interface]
        # 此接口没有权重设置，使用朴素的路由算法
        if not self.weights.get(interface):
            return hosts[randint(0, len(hosts) - 1)]

        weights = self.weights[interface]
        hosts_weight = []
        for host in hosts:
            hosts_weight.append(int(weights.get(host, '100')))

        hit = randint(0, sum(hosts_weight) - 1)
        for i in xrange(len(hosts)):
            if hit <= sum(hosts_weight[:i + 1]):
                return hosts[i]

        raise RegisterException('error for finding [{}] host with weight.'.format(interface))

    def _watch_children(self, event):
        """
        对某个provider下的子节点进行监听，一旦provider发生了变化则对本地缓存进行更新
        :param event:
        :return:
        """
        path = event.path
        interface = path.split('/')[2]

        providers = self.zk.get_children(path, watch=self._watch_children)
        logger.debug('{} providers: {}'.format(interface, providers))
        providers = filter(lambda provider: provider['scheme'] == 'dubbo', map(parse_url, providers))
        if len(providers) == 0:
            logger.debug('no providers for interface {}'.format(interface))
            del self.hosts[interface]
            return
        self.hosts[interface] = map(lambda provider: provider['host'], providers)

    def _watch_configurators(self, event):
        """
        监测某个interface中provider的权重的变化信息
        :param event:
        :return:
        """
        path = event.path
        interface = path.split('/')[2]

        # 试图从配置中取出权重相关的信息
        configurators = self.zk.get_children(DUBBO_ZK_CONFIGURATORS.format(interface),
                                             watch=self._watch_configurators)
        if configurators:
            configurators = map(parse_url, configurators)
            conf = {}
            for configurator in configurators:
                conf[configurator['host']] = configurator['fields'].get('weight', 100)
            self.weights[interface] = conf
        else:
            # 没有权重配置则意味着此配置可以被删除
            del self.weights[interface]

    def _register_consumer(self, providers):
        """
        把本机注册到对应的interface的consumer上去
        :param providers:
        :return:
        """
        provider = providers[0]
        provider_fields = provider['fields']

        consumer = 'consumer://' + get_ip() + provider['path'] + '?'
        fields = {
            'application': self.application_name,
            'category': 'consumers',
            'check': 'false',
            'connected': 'true',
            'dubbo': provider_fields['dubbo'],
            'interface': provider_fields['interface'],
            'methods': provider_fields['methods'],
            'pid': get_pid(),
            'revision': provider_fields['revision'],
            'side': 'consumer',
            'timestamp': int(time.time() * 1000),
            'version': provider_fields['version'],
        }

        keys = fields.keys()
        keys.sort()
        for key in keys:
            value = fields[key]
            consumer += '{0}={1}&'.format(key, value)
        consumer = consumer[:-1]  # 干掉最后一个&

        consumer_path = DUBBO_ZK_CONSUMERS.format(fields['interface'])
        self.zk.ensure_path(consumer_path)
        self.zk.create_async(consumer_path + '/' + quote(consumer, safe=''), ephemeral=True)

    def close(self):
        self.zk.stop()


if __name__ == '__main__':
    pass
