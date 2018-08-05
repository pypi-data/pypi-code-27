import requests
import pandas as pd
import numpy as np
from .util import ascii, retry

ROBINHOOD_EARNING_URL = 'https://api.robinhood.com/marketdata/earnings/'


def __get_earnings(symbol):

    def get_path(d, parent, child, default=None):
        if parent in d and d[parent] is not None and child in d[parent]:
            return d[parent][child]
        else:
            return default

    def parse_result(d):
        period = '%sQ%s' % (d['year'], d['quarter'])
        timing = 'BMO' if get_path(d, 'report', 'timing', '') == 'am' else 'AMC'
        verified = get_path(d, 'report', 'verified', False)
        estimate_eps = ascii(get_path(d, 'eps', 'estimate'))
        actual_eps = ascii(get_path(d, 'eps', 'actual'))
        estimate_eps = float(estimate_eps) if estimate_eps is not None else np.nan
        actual_eps = float(actual_eps) if actual_eps is not None else np.nan

        return {'period': period,
                'timing': timing,
                'verified': verified,
                'estimate_eps': estimate_eps,
                'actual_eps': actual_eps}

    r = requests.get(ROBINHOOD_EARNING_URL, {'symbol': symbol})
    res = r.json()

    data = []
    index = []
    for e in res['results']:
        if 'report' in e and e['report'] is not None and 'date' in e['report']:
            data += [parse_result(e)]
            index += [pd.to_datetime(e['report']['date'])]

    return pd.DataFrame(data=data, index=index)


def get_earnings(symbol):
    return retry(__get_earnings)(symbol)
