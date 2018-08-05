from collections import namedtuple


# TOR settings.
TOR_PASSWORD = ''
TOR_PORT = 9051

# Proxy settings.
LOCAL_HTTP_PROXY = '127.0.0.1:8118'

# IP obtaining settings.
NEW_IP_MAX_ATTEMPTS = 10


# Config = namedtuple(
#     'Config',
#     'tor_password tor_port local_http_proxy new_ip_max_attempts'
# )


# def configure(
#     tor_password=TOR_PASSWORD,
#     tor_port=TOR_PORT,
#     local_http_proxy=LOCAL_HTTP_PROXY,
#     new_ip_max_attempts=NEW_IP_MAX_ATTEMPTS
# ):
#     config = Config(
#         tor_password, tor_port, local_http_proxy, new_ip_max_attempts
#     )
#
#     return config
#
#
# class Config(object):
