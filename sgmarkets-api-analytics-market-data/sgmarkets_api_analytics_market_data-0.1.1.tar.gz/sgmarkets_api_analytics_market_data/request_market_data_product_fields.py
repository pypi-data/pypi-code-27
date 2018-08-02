from timeit import default_timer as timer
from IPython.display import Markdown

from ._util import Util
from .response_market_data_product_fields import ResponseMktDataProductFields


class RequestMktDataProductFields:
    def __init__(self,
                 dic_url=None,
                 response_obj=ResponseMktDataProductFields):
        self.product = None
        self.url = None
        self.response_obj = response_obj
        self.dic_api = {}

    def build_dic_url(self):
        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/data',
                   'endpoint': '/v2/products/' + self.product + '/fields'}
        self.url = Util.build_url(dic_url)

    def expand(self):
        self.build_dic_url()

    def call_api(self, api, debug=False):
        """        See https://analytics-api.sgmarkets.com/data/swagger/ui/index#/Explorer/v2/quotas       """
        t0 = timer()
        print('calling API...')

        raw_response = api.get(self.url, payload=self.dic_api)

        t1 = timer()
        print('Done in {:.2f} s'.format(t1 - t0))
        if debug:
            print('*** START DEBUG ***\n{}\n*** END DEBUG ***'.format(raw_response))
        response = ResponseMktDataProductFields(raw_response)
        return response

    def info(self):
        md="""**RequestMktDataProductFields** is a get method. You only need to set a product (asset class).
        """
        return Markdown(md)