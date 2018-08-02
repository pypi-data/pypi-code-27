from ._obj_from_dict import ObjFromDict
from .request_market_data_fields_values import RequestMktDataFieldsValues
from .request_market_data_instruments import RequestMktDataInstruments
from .request_market_data_intraday_quotes import RequestMktDataIntradayQuotes
from .request_market_data_last_quotes import RequestMktDataLastQuotes
from .request_market_data_live_quotes import RequestMktDataLiveQuotes
from .request_market_data_product import RequestMktDataProduct
from .request_market_data_product_fields import RequestMktDataProductFields
from .request_market_data_quota import RequestMktDataQuota
from .request_market_data_quotes import RequestMktDataQuotes
from .request_market_data_snapshot_quotes import RequestMktDataSnapshotQuotes
from .response_market_data_fields_values import ResponseMktDataFieldsValues
from .response_market_data_instruments import ResponseMktDataInstruments
from .response_market_data_intraday_quotes import ResponseMktDataIntradayQuotes
from .response_market_data_last_quotes import ResponseMktDataLastQuotes
from .response_market_data_live_quotes import ResponseMktDataLiveQuotes
from .response_market_data_product import ResponseMktDataProduct
from .response_market_data_product_fields import ResponseMktDataProductFields
from .response_market_data_quota import ResponseMktDataQuota
from .response_market_data_quotes import ResponseMktDataQuotes
from .response_market_data_snapshot_quotes import ResponseMktDataSnapshotQuotes
from .endpoint_info import Info

dic_endpoints = {
    'v2_quotas': {
        'request': RequestMktDataQuota,
        'response': ResponseMktDataQuota,
        'info': Info('quotas'),
    },
    'v2_products_fields': {
        'request': RequestMktDataProductFields,
        'response': ResponseMktDataProductFields,
        'info': Info('products_fields'),
    },
    'v2_products': {
        'request': RequestMktDataProduct,
        'response': ResponseMktDataProduct,
        'info': Info('products'),
    },
    'v2_instruments': {
        'request': RequestMktDataInstruments,
        'response': ResponseMktDataInstruments,
        'info': Info('instruments'),

    },
    'v2_fields_values': {
        'request': RequestMktDataFieldsValues,
        'response': ResponseMktDataFieldsValues,
        'info': Info('fields_values'),
    },
    'v2_quotes': {
        'request': RequestMktDataQuotes,
        'response': ResponseMktDataQuotes,
        'info': Info('quotes'),
    },
    'v2_last_quotes': {
        'request': RequestMktDataLastQuotes,
        'response': ResponseMktDataLastQuotes,
        'info': Info('last_quotes'),
    },
    'v2_snapshot_quotes': {
        'request': RequestMktDataSnapshotQuotes,
        'response': ResponseMktDataSnapshotQuotes,
        'info': Info('snapshot_quotes'),
    },
    'v2_live_quotes': {
        'request': RequestMktDataLiveQuotes,
        'response': ResponseMktDataLiveQuotes,
        'info': Info('live_quotes'),
    },
    'v2_intraday_quotes': {
        'request': RequestMktDataIntradayQuotes,
        'response': ResponseMktDataIntradayQuotes,
        'info': Info('intraday_quotes'),
    },
}
endpoint = ObjFromDict(dic_endpoints)
