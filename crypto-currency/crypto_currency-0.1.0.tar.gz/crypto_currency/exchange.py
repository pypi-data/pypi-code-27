# Code By Vaayne
# It's for ccxt(https://github.com/ccxt/ccxt/wiki/Manua)
import logging

import ccxt
import pandas as pd


def get_exchange(exchange, api_key=None, secret_key=None):
    if not api_key or not secret_key:
        logging.warning("No API_KEY or SECRET_KEY, could not access to Private data")
    exchange = getattr(ccxt, exchange)({
        'apiKey': api_key,
        'secret': secret_key
    })
    return exchange


class Exchange(object):

    def __init__(self, exchange, api_key=None, secret_key=None):
        self.cli = get_exchange(exchange, api_key, secret_key)

    def get_latest_price(self, symbol):
        ticker = self.cli.fetch_ticker(symbol)
        return ticker.get('last')

    def get_kline_data(self, symbol, period='1d', since=None, limit=None):
        """
        Get kline data, return data frame
        """
        kline_data = self.cli.fetch_ohlcv(symbol, period, since, limit)
        columns = ['time', 'open', 'close', 'low', 'high', 'volumn']
        df = pd.DataFrame(kline_data, columns=columns)
        df.time = pd.to_datetime(df.time, unit='ms')
        df = df.set_index('time')
        return df
