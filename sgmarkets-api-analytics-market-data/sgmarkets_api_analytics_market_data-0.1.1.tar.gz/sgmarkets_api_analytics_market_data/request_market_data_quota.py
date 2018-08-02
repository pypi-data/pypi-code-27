from timeit import default_timer as timer

from ._util import Util
from .response_market_data_quota import ResponseMktDataQuota


class RequestMktDataQuota:
    def __init__(self,
                 dic_url=None,
                 response_obj=ResponseMktDataQuota):
        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/data',
                   'endpoint': '/v2/quotas'}

        self.response_obj = response_obj
        self.url = Util.build_url(dic_url)

        self.dic_api = {"maxQuotas": 0,
                        "currentQuotasUsage": 0}

    def call_api(self, api, debug=False):
        """        See https://analytics-api.sgmarkets.com/data/swagger/ui/index#/Explorer/v2/quotas       """
        t0 = timer()
        print('calling API...')

        raw_response = api.get(self.url, payload=self.dic_api)

        t1 = timer()
        print('Done in {:.2f} s'.format(t1 - t0))
        if debug:
            print('*** START DEBUG ***\n{}\n*** END DEBUG ***'.format(raw_response))
        response = ResponseMktDataQuota(raw_response)
        return response
