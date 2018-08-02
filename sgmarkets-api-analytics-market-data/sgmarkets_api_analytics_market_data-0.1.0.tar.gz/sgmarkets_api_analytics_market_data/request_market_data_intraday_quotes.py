from timeit import default_timer as timer
from IPython.display import Markdown

from ._util import Util
from .response_market_data_intraday_quotes import ResponseMktDataIntradayQuotes


class RequestMktDataIntradayQuotes:
    def __init__(self,
                 response_obj=ResponseMktDataIntradayQuotes):

        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/data',
                   'endpoint': '/v2/intraday-quotes'}

        self.isins = None
        self.fields = None
        self.type = 'mid'
        self.startDate = None
        self.endDate = None
        self.barLength = 1
        self.isEmpty = True
        self.time_zone_res = None
        self.time_zone_req = 'utc'
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

        if self.time_zone_res is None:
            self.time_zone_res=self.time_zone_req

        self.fields = [f.upper() for f in self.fields]

        assert self.check_type(), "type could only be Mid, Ask, Bid or Undefined string"
        assert isinstance(self.startDate, str), "startDate should be of type string"
        assert isinstance(self.endDate, str), "endDate should be of type string"
        assert isinstance(self.isEmpty, bool), "isEmpty should be a boolean"
        assert isinstance(self.barLength,
                          int), "barLength should be of type int. barLength is the tick interval in minutes"
        assert self.format_response in ['dic_isins_as_keys', 'dic_fields_as_keys', 'multiindex_isins_fields',
                                        'multiindex_fields_isins'], \
            "format_response should be one of {}".format(
                ['dic_isins_as_keys', 'dic_fields_as_keys', 'multiindex_isins_fields', 'multiindex_fields_isins'])
        assert self.time_zone_res.lower() in ['london','paris','new-york','lon','pa','ny','utc','gmt'], \
            "time_zone_res should be one of {}".format(
                ['london', 'paris', 'new-york', 'lon', 'pa', 'ny', 'utc'])
        assert self.time_zone_req.lower() in ['london','paris','new-york','lon','pa','ny','utc','gmt'], \
            "time_zone_req should be one of {}".format(
                ['london', 'paris', 'new-york', 'lon', 'pa', 'ny', 'utc'])

    def check_type(self):
        t = self.type.lower()
        return t == 'mid' or t == 'ask' or t == 'bid' or t == 'undefined'

    def time_converter(self):
        t=self.time_zone_req.lower()
        if t == 'utc':
            return '.000Z'
        elif t == 'london' or t == 'lon':
            return '+0100'
        elif t == 'paris' or t == 'pa':
            return '+0200'
        elif t == 'new_york' or t == 'ny':
            return '-0500'
        else:
            return ''

    def build_dic_api(self):

        self.dic_api = {'instruments': self.isins,
                        'fields': self.fields,
                        'type': self.type,
                        'startDate': self.startDate + self.time_converter(),
                        'endDate': self.endDate + self.time_converter(),
                        'barLength': self.barLength,
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
        response = ResponseMktDataIntradayQuotes(raw_response, self.format_response, self.time_zone_res)
        return response

    def info(self):
        md="""**RequestMktDataIntradayQuotes** takes seven arguments:
- isins (str or list of str)
- fields (str or list of str)
- type (str)
- startDate (str)
- endDate (str)
- time_zone (str)
- barLength (int)


**isins** could be either a list of string or a string.

**fields** could be either a list of string or a string.

**type** could only take three values:
- mid (default)
- bid
- ask

**startDate** should be a string in ISO 8601 format:
    - yyyy-mm-ddThh:mm:ss.SSSz (2018-07-24T12:30:26.983Z) UTC format
    - yyyy-mm-ddThh:mm:ss+hhmm (executed UTC/GMT + time+hhmm) 
    - yyyy-mm-ddThh:mm:ss (executed as UTC/GMT or local time with respect to time_zone_req parameter)
    
**endDate** should be a string as well.

**time_zone_req** set the time zone for the request, could be one of:
- utc
- london, lon = UTC+0100
- paris, pa = UTC+0200
- new-york, ny = UTC-0500 

**time_zone_res** set the time zone for the response, could be one of:
- utc, gmt
- london, lon = UTC+0100
- paris, pa = UTC+0200
- new-york, ny = UTC-0500 

**By default time_zone_res equal time_zone_req**


**barLength** should be an int representing the frequency in minutes (default 1)

**format_response** could take only four values:
- dic_isins_as_keys (default)
  The response will be a dic of df with isins as keys
- dic_fields_as_keys
- multiindex_isins_fields
    level(0) of columns name will be isins, level(1) keys
- multiindex_fields_isins
"""
        return Markdown(md)
