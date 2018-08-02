from timeit import default_timer as timer
from IPython.display import Markdown

from ._util import Util
from .response_market_data_live_quotes import ResponseMktDataLiveQuotes


class RequestMktDataLiveQuotes:
    def __init__(self,
                 response_obj=ResponseMktDataLiveQuotes):

        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/data',
                   'endpoint': '/v2/live-quotes'}

        self.isins = None
        self.fields = None
        self.type = 'mid'
        self.crossIntrumentsFormulas = []
        self.isEmpty = True

        self.url = Util.build_url(dic_url)
        self.response_obj = response_obj
        self.format_response = 'dic_isins_as_keys'
        self.dic_api = {}

    def check_params(self):
        if isinstance(self.isins, str):
            self.isins = self.isins.split(',')

        if not isinstance(self.isins, list):
            self.isins = [self.isins]

        if isinstance(self.fields, str):
            self.fields = self.fields.split(',')

        if not isinstance(self.fields, list):
            self.fields = [self.fields]

        self.fields = [f.upper() for f in self.fields]

        assert self.check_type(), "type could only be Mid, Ask, Bid string"
        assert isinstance(self.isEmpty, bool), "isEmpty should be a boolean"
        assert self.format_response in ['dic_isins_as_keys', 'dic_fields_as_keys', 'multiindex_isins_fields',
                                        'multiindex_fields_isins'], \
            "format_response should be one of {}".format(
                ['dic_isins_as_keys', 'dic_fields_as_keys', 'multiindex_isins_fields', 'multiindex_fields_isins'])

    def check_type(self):
        t = self.type.lower()
        return t == 'mid' or t == 'ask' or t == 'bid'

    def build_dic_api(self):

        self.dic_api = {'instruments': self.isins,
                        'fields': self.fields,
                        'type': self.type,
                        'crossInstrumentsFormulas': self.crossIntrumentsFormulas,
                        'isEmpty': self.isEmpty}

    def expand(self):
        self.check_type()
        self.check_params()
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
        response = ResponseMktDataLiveQuotes(raw_response, self.format_response)
        return response

    def info(self):
        md="""**RequestMktDataLiveQuotes** could takes only three arguments:
- isins (str or list of str)
- fields (str or list of str)
- type (str)


**isins** could be either a list of string or a string.

**fields** could be either a list of string or a string.

**type** could only take three values:
- mid (default)
- bid
- ask

**format_response** could take only four values:
- dic_isins_as_keys (default)
  The response will be a dic of df with isins as keys
- dic_fields_as_keys
- multiindex_isins_fields
    level(0) of columns name will be isins, level(1) keys
- multiindex_fields_isins"""

        return Markdown(md)
