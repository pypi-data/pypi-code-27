#!/usr/bin/python
#coding=utf-8

import redis

class ThinkRedisPool(object):
    def __init__(self):
        pass

    @staticmethod
    def get_connection_pool(host = '127.0.0.1'
                            , password = None
                            , port = 6379
                            , db = 0
                            , max_connections = 64
                            ):
        kwargs = {
            'host': host,
            'port': port,
            'db': db,
            'max_connections': max_connections,
            'password': password,
        }
        _connection_pool = redis.ConnectionPool(**kwargs)

        return _connection_pool

# g_redis_pool = ThinkRedisPool.get_connection_pool(host=g_config.get("redis", "host")
#                                                   , password=g_config.get("redis", "password")
#                                                   , port=g_config.get("redis", "port")
#                                                   , db=g_config.get("redis", "db"))