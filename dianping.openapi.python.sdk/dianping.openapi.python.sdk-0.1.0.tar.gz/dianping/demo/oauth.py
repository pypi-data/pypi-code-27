from dianping.client import Client
from dianping.request.oauth import AuthorizePlatformRequest
from dianping.request.oauth import RefreshTokenRequest
from dianping.request.oauth import DynamicTokenRequest


def platformauthtest():
    authorize_request = AuthorizePlatformRequest('1000069', '6862bd6012020b0fd385652905db18d4c9eaa835')
    client = Client(authorize_request)
    response = client.invoke()
    print(response)
    assert (response is not None)


def refreshtokentest():
    refreshreq = RefreshTokenRequest('17', '6A23F2D41F73902EFCC9B6B3F076D74B',
                                     '172e69a5b9e5d8245d012e66665ccb08cfbe116d')
    client = Client(refreshreq)
    response = client.invoke()
    print(response)
    assert (response is not None)


def dynamicTokenRequest():
    dynamicTokenRequest = DynamicTokenRequest('f9e039e3da9ea9ec', '6c8ac87e6f81a7c8249b12fd7efee4cf4dd7a787',
                                              '19bbc883eb621a2604018805f7fb18b6f6c88340', 'cn.bing.com')
    client = Client(dynamicTokenRequest)
    response = client.invoke()
    print(response)
    assert (response is not None)


if __name__ == '__main__':
    platformauthtest()
    refreshtokentest()
    dynamicTokenRequest()
