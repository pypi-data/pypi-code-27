# coding: utf-8
# 'ascii'
from dianping.client import Client
from dianping.request.poimaintain import POIMaintainQueryFlowStatusRequest

#根据流程id查询流程状态
def poimaintainqueryflowsatustest():
    poimaintainqueryflowsatusrequest = POIMaintainQueryFlowStatusRequest('92ac75f6c6d2b9bf', '6132f8f4a0af2697bdd7c1acaa9739f9fc8b8d05',
                                                                         'b5f6f2ae6b6a773f41c717f75b575de1d2896e6c', 0, 191748933)
    client = Client(poimaintainqueryflowsatusrequest)
    response = client.invoke()
    print(response)
    assert (response is not None)


if __name__ == '__main__':
   poimaintainqueryflowsatustest()