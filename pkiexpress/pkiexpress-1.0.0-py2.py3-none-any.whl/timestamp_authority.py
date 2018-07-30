class TimestampAuthority(object):
    __url = None
    __token = None
    __ssl_thumbprint = None
    __basic_auth = None
    __auth_type = None

    NONE = 0
    BASIC_AUTH = 1
    SSL = 2
    OAUTH_TOKEN = 3

    def __init__(self, url):
        self.__url = url
        self.__auth_type = TimestampAuthority.NONE

    def set_oauth_token_authentication(self, token):
        self.__token = token
        self.__auth_type = TimestampAuthority.OAUTH_TOKEN

    def set_basic_authentication(self, username, password):
        self.__basic_auth = "%s:%s" % (username, password)
        self.__auth_type = TimestampAuthority.BASIC_AUTH

    def set_ssl_authentication(self, ssl_thumbprint):
        self.__ssl_thumbprint = ssl_thumbprint
        self.__auth_type = TimestampAuthority.SSL

    @property
    def url(self):
        return self.__url

    @property
    def token(self):
        return self.__token

    @property
    def ssl_thumbprint(self):
        return self.__ssl_thumbprint

    @property
    def basic_auth(self):
        return self.__basic_auth

    def add_cmd_arguments(self, args):
        args.append('--tsa-url')
        args.append(self.__url)

        # User choice SSL authentication.
        if self.__auth_type is TimestampAuthority.NONE:
            pass
        elif self.__auth_type is TimestampAuthority.BASIC_AUTH:
            args.append('--tsa-basic-auth')
            args.append(self.__basic_auth)
        elif self.__auth_type is TimestampAuthority.SSL:
            args.append('--tsa-ssl-thumbprint')
            args.append(self.__ssl_thumbprint)
        elif self.__auth_type is TimestampAuthority.OAUTH_TOKEN:
            args.append('--tsa-token')
            args.append(self.__token)
        else:
            raise Exception('Unknown authentication type of the timestamp'
                            'authority')


__all__ = ['TimestampAuthority']
