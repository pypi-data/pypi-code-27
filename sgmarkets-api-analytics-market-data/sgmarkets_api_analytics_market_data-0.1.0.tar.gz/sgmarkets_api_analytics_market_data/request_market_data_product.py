from timeit import default_timer as timer
from IPython.display import Markdown

from ._util import Util
from .response_market_data_product import ResponseMktDataProduct


class RequestMktDataProduct:
    def __init__(self,
                 dic_url=None,
                 response_obj=ResponseMktDataProduct):
        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/data',
                   'endpoint': '/v2/products'}
        self.url = Util.build_url(dic_url)
        self.response_obj = response_obj
        self.dic_api = {}

    def call_api(self, api, debug=False):
        """        See HTTPS://analytics-api.sgmarkets.com/data/v2/products      """
        t0 = timer()
        print('calling API...')

        raw_response = api.get(self.url, payload=self.dic_api)

        t1 = timer()
        print('Done in {:.2f} s'.format(t1 - t0))
        if debug:
            print('*** START DEBUG ***\n{}\n*** END DEBUG ***'.format(raw_response))
        response = ResponseMktDataProduct(raw_response)
        return response

    def info(self):
        md="""**RequestMktDataProduct** is a get method. You don't need to set anything.
        """
        return Markdown(md)
