from timeit import default_timer as timer
from IPython.display import Markdown

from ._util import Util
from .response_market_data_instruments import ResponseMktDataInstruments


class RequestMktDataInstruments:
    def __init__(self,
                 response_obj=ResponseMktDataInstruments):

        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/data',
                   'endpoint': '/v2/instruments'}

        self.constraints = None
        self.url = Util.build_url(dic_url)
        self.response_obj = response_obj
        self.page = 0
        self.pageSize = 0
        self.dic_api={}

    def build_dic_api(self):
        self.dic_api = {'filter': {'constraints': self.constraints}, 'page': self.page, 'pageSize': self.pageSize}

    def expand(self):
        if self.constraints is None:
            self.constraints = {}

        self.build_dic_api()

    def call_api(self, api, debug=False):
        """        See HTTPS://analytics-api.sgmarkets.com/data/v2/products      """
        t0 = timer()
        print('calling API...')

        raw_response = api.post(self.url, payload=self.dic_api)

        t1 = timer()
        print('Done in {:.2f} s'.format(t1 - t0))
        if debug:
            print('*** START DEBUG ***\n{}\n*** END DEBUG ***'.format(raw_response))
        response = ResponseMktDataInstruments(raw_response)
        return response

    def info(self):
        md=""" **RequestMktDataInstruments** takes only one attribute (**constraints**):
+ **Constraints**:  
    Constraints should be a list of dictionaries. Each dictionary has to have at least a property key and a value key. Each dic could also have an operator key.
            
    **Properties are**:
- product 
- Any descriptive field (see the v2_products_fields endpoint)
- Any indicators field (see the v2_products_fields endpoint)

    **Values are**:
- Any product name (asset class) (see v2_products endpoint)
- Any values for numeric data if combined with an operator (by default Equal)
- Any values in the value list for each fields (see the v2_fields_values endpoint)

    **Operator are**:
- Lower 
- LowerOrEqual
- Equal
- GreaterOrEqual 
- Greater.
        """
        return Markdown(md)
