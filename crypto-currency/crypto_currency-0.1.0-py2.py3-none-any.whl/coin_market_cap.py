# Code By Vaayne

import pandas as pd

from crypto_currency.utils import fetch_data


class CoinMarketCapBase(object):

    @classmethod
    def _get(cls, path, **kwargs):
        if not path[0] == '/':
            path = '/' + path
        url = 'https://api.coinmarketcap.com/v2' + path
        return fetch_data(url, **kwargs)

    @classmethod
    def get_listings(cls):
        """
        This endpoint displays all active crypto currency listings in one call.
        Use the "id" field on the Ticker endpoint to query more information on a specific crypto currency.
        Returns:
            {
                "data": [
                    {
                        "id": 1,
                        "name": "Bitcoin",
                        "symbol": "BTC",
                        "website_slug": "bitcoin"
                    },
                    {
                        "id": 2,
                        "name": "Litecoin",
                        "symbol": "LTC",
                        "website_slug": "litecoin"
                    },
                    ...
                },
                "metadata": {
                    "timestamp": 1525137187,
                    "num_cryptocurrencies": 1602,
                    "error": null
                }
            ]
        """
        path = '/listings/'
        res = cls._get(path)
        return res

    @classmethod
    def get_ticker(cls, start=1, limit=100, structure='array', sort='rank', convert=None):
        """
        Description:
            This endpoint displays crypto currency ticker data in order of rank.
            The maximum number of results per call is 100.
            Pagination is possible by using the start and limit parameters.
        Optional parameters:
            (int) start - return results starting from the specified number (default is 1)
            (int) limit - return a maximum of [limit] results (default is 100; max is 100)
            (string) sort - return results sorted by [sort] . Possible values are id, rank,
                            volume_24h, and percent_change_24h (default is rank).
            Note: It is strongly recommended to use id to sort if paginating through all available
                  results since id is the only sort option guaranteed to return in a consistent order.
            (string) structure - specify the structure for the main data field.
                     Possible values are dictionary and array (default is dictionary).
            (string) convert - return pricing info in terms of another currency.
            Valid fiat currency values are: "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK",
                                            "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",
                                            "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN",
                                            "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"
            Valid cryptocurrency values are: "BTC", "ETH" "XRP", "LTC", and "BCH"
        Returns:
            {
                "data": {
                    "1": {
                        "id": 1,
                        "name": "Bitcoin",
                        "symbol": "BTC",
                        "website_slug": "bitcoin",
                        "rank": 1,
                        "circulating_supply": 17008162.0,
                        "total_supply": 17008162.0,
                        "max_supply": 21000000.0,
                        "quotes": {
                            "USD": {
                                "price": 9024.09,
                                "volume_24h": 8765400000.0,
                                "market_cap": 153483184623.0,
                                "percent_change_1h": -2.31,
                                "percent_change_24h": -4.18,
                                "percent_change_7d": -0.47
                            }
                        },
                        "last_updated": 1525137271
                    },
                    "1027": {
                        "id": 1027,
                        "name": "Ethereum",
                        "symbol": "ETH",
                        "website_slug": "ethereum",
                        "rank": 2,
                        "circulating_supply": 99151888.0,
                        "total_supply": 99151888.0,
                        "max_supply": null,
                        "quotes": {
                            "USD": {
                                "price": 642.399,
                                "volume_24h": 2871290000.0,
                                "market_cap": 63695073558.0,
                                "percent_change_1h": -3.75,
                                "percent_change_24h": -7.01,
                                "percent_change_7d": -2.32
                            }
                        },
                        "last_updated": 1525137260
                    }
                    ...
                },
                "metadata": {
                    "timestamp": 1525137187,
                    "num_cryptocurrencies": 1602,
                    "error": null
                }
            ]
        """
        path = '/ticker/'
        params = {
            'start': start,
            'limit': limit,
            'structure': structure,
            'sort': sort,
            'convert': convert
        }

        res = cls._get(path, params=params)
        return res

    @classmethod
    def get_global(cls, convert=None):
        """
        This endpoint displays the global data found at the top of coinmarketcap.com.
        Args:
            convert(str): return pricing info in terms of another currency.
            Valid fiat currency values are: "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK",
                                                           "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",
                                                           "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN",
                                                           "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"
            Valid crypto currency values are: "BTC", "ETH" "XRP", "LTC", and "BCH"
        Returns:
        {
            "data": {
                "active_cryptocurrencies": 1594,
                "active_markets": 10526,
                "bitcoin_percentage_of_market_cap": 37.65,
                "quotes": {
                    "USD": {
                        "total_market_cap": 407690157494.0,
                        "total_volume_24h": 30969801118.0
                    }
                },
                "last_updated": 1525137271
            },
            "metadata": {
                "timestamp": 1525237332,
                "error": null
            }
        }
        """
        path = '/global/'
        params = {
            'convert': convert
        }
        res = cls._get(path, params=params)
        return res

    @classmethod
    def get_ticker_by_id(cls, id, structure='array', convert=None):
        """
        This endpoint displays ticker data for a specific crypto currency.
        Use the "id" field from the Listings endpoint in the URL.
        Args:
            id(int): coin id
            structure(str): specify the structure for the main data field.
                            Possible values are dictionary and array (default is dictionary).
            convert(str):  return pricing info in terms of another currency.
                           Valid fiat currency values are: "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK",
                                                           "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",
                                                           "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN",
                                                           "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"
                           Valid crypto currency values are: "BTC", "ETH" "XRP", "LTC", and "BCH"

        Returns:
            {
                "data": {
                    "id": 1,
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "website_slug": "bitcoin",
                    "rank": 1,
                    "circulating_supply": 17008162.0,
                    "total_supply": 17008162.0,
                    "max_supply": 21000000.0,
                    "quotes": {
                        "USD": {
                            "price": 9024.09,
                            "volume_24h": 8765400000.0,
                            "market_cap": 153483184623.0,
                            "percent_change_1h": -2.31,
                            "percent_change_24h": -4.18,
                            "percent_change_7d": -0.47
                        }
                    },
                    "last_updated": 1525137271
                },
                "metadata": {
                    "timestamp": 1525237332,
                    "error": null
                }
        }
        """
        path = f' /ticker/{id}/'
        params = {
            'structure': structure,
            'convert': convert
        }
        res = cls._get(path, params=params)
        return res


class CoinMarketCap(CoinMarketCapBase):

    def __init__(self):
        self._coins = self._coin_list()

    def _coin_list(self):
        coins = self.get_listings()
        coins = pd.DataFrame(coins['data'])
        coins = coins.set_index('symbol')
        return coins

    @property
    def coins(self):
        return self._coins

    def get_symbol_info(self, symbol, info_name):
        if info_name in ['id', 'name', 'website_slug']:
            return self.coins.loc[symbol, info_name]
        else:
            raise ValueError('Only support id, name and website_slug info')

    def cal_metric(self, df):
        df['Volume_MA'] = df.Volume.rolling(7).mean()
        df['Change'] = df['Close'] / df['Open'] - 1
        df['Amplitude'] = df['High'] / df['Low'] - 1
        df['Volume_Per'] = df['Volume'] / df['Volume_MA']
        return df

    def history_data(self, symbol, start, end):
        """
        Get history data from CoinMarketCap
        Args:
            symbol(str): BTC/ETH/...
            start(str): 20180101
            end(str): 20181230

        Returns:
            pd.DataFrame: DataFrame of data
        """
        slug = self.get_symbol_info(symbol, 'website_slug')
        url = f'https://coinmarketcap.com/currencies/{slug}/historical-data/?start={start}&end={end}'
        df = pd.read_html(url)[0]
        df.columns = df.columns.str.replace('*', '')
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        df = df.sort_index(ascending=True)
        return df
