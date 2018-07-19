# coding: utf-8
# 'ascii'
from dianping.client import Client
from dianping.request.session import OauthSessionQueryRequest
from dianping.request.session import CustomerKeyShopScopeRequest


def oauth_session_query_test():
    request = OauthSessionQueryRequest("cecb5bd6ae79e7e1", "acd63c7071198db36e91ffd316e7cf4ad990d350",
                                       "6dff08d50b1b2bbc51f932d97d2796db40690f0b")
    client = Client(request)
    response = client.invoke()
    print(response)
    assert (response is not None)


def customer_key_shopscope_query_test():
    request = CustomerKeyShopScopeRequest("cecb5bd6ae79e7e1", "acd63c7071198db36e91ffd316e7cf4ad990d350",
                                          "6dff08d50b1b2bbc51f932d97d2796db40690f0b",
                                          "cece13e2b14b8fd111ee04674d824d19")
    client = Client(request)
    response = client.invoke()
    print(response)
    assert (response is not None)


if __name__ == '__main__':
    #oauth_session_query_test()
    customer_key_shopscope_query_test()
