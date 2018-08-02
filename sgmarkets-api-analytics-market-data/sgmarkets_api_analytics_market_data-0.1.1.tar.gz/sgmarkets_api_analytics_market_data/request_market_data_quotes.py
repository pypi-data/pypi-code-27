from timeit import default_timer as timer
from IPython.display import Markdown

from ._util import Util
from .response_market_data_quotes import ResponseMktDataQuotes


class RequestMktDataQuotes:
    def __init__(self,
                 response_obj=ResponseMktDataQuotes):

        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/data',
                   'endpoint': '/v2/quotes'}

        self.isins = None
        self.fields = None
        self.type = 'mid'
        self.startDate = None
        self.endDate = None
        self.source = 'SG'
        self.time = 'Close'
        self.place = 'Europe'
        self.refSet = None
        self.frequency = 'undefined'
        self.fillEmptyQuotes = True
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

        assert self.check_type(), "type could only be Mid, Ask, Bid or Undefined string"
        assert isinstance(self.startDate, str), "startDate should be of type string"
        assert isinstance(self.endDate, str), "endDate should be of type string"
        assert isinstance(self.refSet, dict), "refSet should be a dic containing source, place and time keys"
        assert set(self.refSet.keys()) == {'source', 'place', 'time'}, "refSet keys should be source, place and time"
        assert self.frequency in ['undefined', 'daily', 'weekly', 'monthly', 'quaterly',
                                  'annually'], "frequency should be one of ['undefined','daily','weekly','monthly','quaterly','annually'] "
        assert isinstance(self.fillEmptyQuotes, bool), "fillemptyQuotes should be a boolean"
        assert isinstance(self.isEmpty, bool), "isEmpty should be a boolean"
        assert self.format_response in ['dic_isins_as_keys', 'dic_fields_as_keys', 'multiindex_isins_fields',
                                        'multiindex_fields_isins'], \
            "format_response should be one of {}".format(
                ['dic_isins_as_keys', 'dic_fields_as_keys', 'multiindex_isins_fields', 'multiindex_fields_isins'])

    def check_type(self):
        t = self.type.lower()
        return t == 'mid' or t == 'ask' or t == 'bid' or t == 'undefined'

    def build_refSet(self):
        if self.refSet is None:
            self.refSet = {
                'source': self.source,
                'place': self.place,
                'time': self.time,
            }

    def build_dic_api(self):

        self.dic_api = {'instruments': self.isins,
                        'fields': self.fields,
                        'type': self.type,
                        'startDate': self.startDate,
                        'endDate': self.endDate,
                        'refSet': self.refSet,
                        'frequency': self.frequency,
                        'crossInstrumentsFormulas': self.crossIntrumentsFormulas,
                        'fillEmptyQuotes': self.fillEmptyQuotes,
                        'isEmpty': self.isEmpty}

    def expand(self):
        self.build_refSet()
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
        response = ResponseMktDataQuotes(raw_response, self.format_response)
        return response

    def info(self):
        md="""**RequestMktDataQuotes** takes seven arguments:
- isins (str or list of str)
- fields (str or list of str)
- type (str)
- startDate (str)
- endDate (str)
- source (str)
- time (str)
- place (str)
- refSet (dic)
- fillEmptyQuotes (bool)
- format_response (str)


**isins** could be either a list of string or a string.([str,str],'str,str')

**fields** could be either a list of string or a string.([str,str],'str,str')

**type** could only take three values:
- mid (default)
- bid
- ask

**startDate** should be a string, with format:
- yyyy-mm-dd (2018-07-24)
    
**endDate** should be a string as well.

**source** could take multiples values:
- SG (default)
- MARKIT
- ICAP
- ...

For more details see v2_products enpdoint

**time** could take multiple values:
- Close (default)
- Open
- "18H30"
- ...

For more details see v2_products enpdoint

**place** could take three values:
- Europe (default)
- US
- Asia

**refSet** is a dic with three keys:
- source
- time
- place

You can so either set the refSet dic or set each element separetly.

**fillEmptyQuotes** boolean, if True (default) fill missing point with previous data

**frequency** could take five values:
- daily (default)
- weekly
- monthly
- quaterly
- annualy

**format_response** could take only four values:
- dic_isins_as_keys (default)
  The response will be a dic of df with isins as keys
- dic_fields_as_keys
- multiindex_isins_fields
    level(0) of columns name will be isins, level(1) keys
- multiindex_fields_isins

"""
        return Markdown(md)
