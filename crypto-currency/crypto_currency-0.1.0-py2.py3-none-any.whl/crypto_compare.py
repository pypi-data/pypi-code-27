"""
It is API for CryptoCompare
API Docs: https://min-api.cryptocompare.com
"""

from urllib.parse import urljoin

from crypto_currency.utils import fetch_data


class CryptoCompareBase(object):

    def _get(self, url_path, **kwargs):
        url = urljoin('https://min-api.cryptocompare.com', url_path)
        return fetch_data(url, **kwargs)

    def _valid_params(self, keys, kwargs):
        for key in keys:
            if key not in kwargs:
                raise ValueError(f"This function must have `{key}` as a param")

    def _fetch_data(self, url_path, valid_keys=None, **kwargs):
        if valid_keys:
            self._valid_params(valid_keys, kwargs)
        return self._get(url_path, **kwargs)


class Price(CryptoCompareBase):

    def price_single_symbol(self, **kwargs):
        """
        Get the current price of any crypto currency in any other currency that you need.
        If the crypto does not trade directly into the toSymbol requested, BTC will be used for conversion.
        If the opposite pair trades we invert it (eg.: BTC-XMR)

        Args:
            fsym(str): The crypto currency symbol of interest [Max character length: 10]
            tsyms(str): Comma separated crypto currency symbols list to convert into [Max character length: 500]

        Returns:
            dict: dict of target symbols
        """
        url_path = '/data/price'
        valid_keys = ['fsym', 'tsyms']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def price_multi_symbols(self, **kwargs):
        """
        Get the current price of any crypto currency in any other currency that you need.
        If the crypto does not trade directly into the toSymbol requested, BTC will be used for conversion.
        If the opposite pair trades we invert it (eg.: BTC-XMR)

        Args:
            fsyms(str): The crypto currency symbol of interest [Max character length: 10]
            tsyms(str): Comma separated crypto currency symbols list to convert into [Max character length: 500]

        Returns:
            dict: dict of target symbols
        """
        url_path = '/data/pricemulti'
        valid_keys = ['fsyms', 'tsyms']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def price_multi_symbols_full_data(self, **kwargs):
        """
        Get all the current trading info (price, vol, open, high, low etc)
        of any list of crypto currencies in any other currency that you need.

        If the crypto does not trade directly into the toSymbol requested, BTC will be used for conversion.
        This API also returns Display values for all the fields.
        If the opposite pair trades we invert it (eg.: BTC-XMR)
        """
        url_path = '/data/pricemultifull'
        valid_keys = ['fsyms', 'tsyms']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def price_custom_average(self, **kwargs):
        """
        Compute the current trading info (price, vol, open, high, low etc)
        of the requested pair as a volume weighted average based on the exchanges requested.
        """
        url_path = '/data/pricemultifull'
        valid_keys = ['fsym', 'tsym', 'e']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)


class HistoryDate(CryptoCompareBase):

    def historical_daily(self, **kwargs):
        """
        Get open, high, low, close, volume from and volume to from the daily historical data.
        The values are based on 00:00 GMT time.
        It uses BTC conversion if data is not available because the coin is not trading in the specified currency.
        """
        url_path = '/data/histoday'
        valid_keys = ['fsym', 'tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def historical_hourly(self, **kwargs):
        """
        Get open, high, low, close, volume from and volume to from the hourly historical data.
        The values are based on 00:00 GMT time.
        It uses BTC conversion if data is not available because the coin is not trading in the specified currency.
        """
        url_path = '/data/histohour'
        valid_keys = ['fsym', 'tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def historical_minute(self, **kwargs):
        """
        Get open, high, low, close, volume from and volume to from the minute historical data.
        The values are based on 00:00 GMT time.
        It uses BTC conversion if data is not available because the coin is not trading in the specified currency.
        """
        url_path = '/data/histohour'
        valid_keys = ['fsym', 'tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def historical_daily_timestamp(self, **kwargs):
        """
        Get the price of any crypto currency in any other currency that you need at a given timestamp.
        The price comes from the daily info - so it would be the price
        at the end of the day GMT based on the requested TS.

        If the crypto does not trade directly into the toSymbol requested, BTC will be used for conversion.
        Tries to get direct trading pair data, if there is none or it is more than 10 days before the ts requested,
        it uses BTC conversion. If the opposite pair trades we invert it (eg.: BTC-XMR)

        The calculation types are:

        Close - a Close of the day close price
        MidHighLow - the average between the 24 H high and low
        VolFVolT - the total volume to / the total volume from
        """
        url_path = '/data/pricehistorical'
        valid_keys = ['fsym', 'tsyms']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def historical_daily_average_price(self, **kwargs):
        url_path = '/data/dayAvg'
        valid_keys = ['fsym', 'tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def historical_daily_exchange_volume(self, **kwargs):
        """
        Get total volume from the daily historical exchange data.
        We store the data in BTC and we multiply by the BTC-tsym value
        """
        url_path = '/data/exchange/histoday'
        valid_keys = ['tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def historical_hourly_exchange_volume(self, **kwargs):
        """
        Get total volume from the hourly historical exchange data.
        We store the data in BTC and we multiply by the BTC-tsym value
        """
        url_path = '/data/exchange/histohour'
        valid_keys = ['tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)


class TopList(CryptoCompareBase):

    def top_exchange_volume_data_by_pair(self, **kwargs):
        """
        Get top exchanges by volume for a currency pair.
        The number of exchanges you get is the minimum of the limit
        you set (default 5) and the total number of exchanges available
        """
        url_path = '/data/top/exchanges'
        valid_keys = ['fsym', 'tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def top_exchange_full_data_by_pair(self, **kwargs):
        """
        Get top exchanges by volume for a currency pair plus the full CCCAGG data.
        The number of exchanges you get is the minimum of the limit
        you set (default 5) and the total number of exchanges available
        """
        url_path = '/data/top/exchanges/full'
        valid_keys = ['fsym', 'tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def top_list_by_pair_volume(self, **kwargs):
        """
        Get top coins by volume for the to currency.
        It returns volume24hto and total supply (where available).
        The number of coins you get is the minimum of the limit
        you set (default 50) and the total number of coins available
        """
        url_path = '/data/top/volumes'
        valid_keys = ['tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def top_list_of_trading_pairs(self, **kwargs):
        """
        Get top pairs by volume for a currency (always uses our aggregated data).
        The number of pairs you get is the minimum of the limit
        you set (default 5) and the total number of pairs available
        """
        url_path = '/data/top/pairs'
        valid_keys = ['fsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def top_list_by_total_volume(self, **kwargs):
        """
        Get a number of top coins by their total volume across all markets in the last 24 hours.
        Default value is first page (0) and the top 10 coins.
        """
        url_path = '/data/top/totalvol'
        valid_keys = ['tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)


class Streaming(CryptoCompareBase):

    def subs_watchlist(self, **kwargs):
        """
        Get combinations of subs and pricing info in order to know
        what needs to be streamed and how to connect to the streamers.
        The possible responses for Conversion are: not_needed, direct,
        invert, multiply, divide, invert_multiply, invert_divide

        - For not_needed - it means you asked for one symbol to the same symbol.
          You should just use the value you have, no need for streaming or conversion.
        - For direct - SubBase + Market + ~ + CurrencyFrom + ~ + CurrencyTo
        - For invert - 1 / SubBase + Market + ~ + CurrencyTo + ~ + CurrencyFrom
        - For multiply - SubBase + Market + ~ + CurrencyFrom + ~ + ConversionSymbol * \
          SubBase + Market + ~ + ConversionSymbol + ~ + CurrencyTo
        - For divide - SubBase + Market + ~ + CurrencyFrom + ~ + ConversionSymbol / SubBase + \
          Market + ~ + CurrencyTo + ~ + ConversionSymbol
        - For invert_multiply - 1 / (SubBase + Market + ~ + CurrencyFrom + ~ + ConversionSymbol * \
          SubBase + Market + ~ + ConversionSymbol + ~ + CurrencyTo)
        - For invert_divide - SubBase + Market + ~ + ConversionSymbol + ~ + CurrencyTo / SubBase + \
          Market + ~ + ConversionSymbol + ~ + CurrencyFrom
        """
        url_path = '/data/coin/subsWatchlist'
        valid_keys = ['fsyms', 'tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def coins_general_info(self, **kwargs):
        """
        Get combinations of subs and pricing info in order to know
        what needs to be streamed and how to connect to the streamers.
        The possible responses for Conversion are: not_needed, direct,
        invert, multiply, divide, invert_multiply, invert_divide

        - For not_needed - it means you asked for one symbol to the same symbol.
          You should just use the value you have, no need for streaming or conversion.
        - For direct - SubBase + Market + ~ + CurrencyFrom + ~ + CurrencyTo
        - For invert - 1 / SubBase + Market + ~ + CurrencyTo + ~ + CurrencyFrom
        - For multiply - SubBase + Market + ~ + CurrencyFrom + ~ + ConversionSymbol * \
          SubBase + Market + ~ + ConversionSymbol + ~ + CurrencyTo
        - For divide - SubBase + Market + ~ + CurrencyFrom + ~ + ConversionSymbol / SubBase + \
          Market + ~ + CurrencyTo + ~ + ConversionSymbol
        - For invert_muliply - 1 / (SubBase + Market + ~ + CurrencyFrom + ~ + ConversionSymbol * \
          SubBase + Market + ~ + ConversionSymbol + ~ + CurrencyTo)
        - For invert_divide - SubBase + Market + ~ + ConversionSymbol + ~ + CurrencyTo / SubBase + \
          Market + ~ + ConversionSymbol + ~ + CurrencyFrom
        """
        url_path = '/data/coin/generalinfo'
        valid_keys = ['fsyms', 'tsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)

    def subs_by_pair(self, **kwargs):
        """
        Get all the available streamer subscription channels for the requested pairs.
        """
        url_path = '/data/subs'
        valid_keys = ['fsym']
        return self._fetch_data(url_path, valid_keys=valid_keys, **kwargs)


class News(CryptoCompareBase):

    def latest_news_articles(self, **kwargs):
        """
        Returns news articles from the providers that CryptoCompare has integrated with.
        """
        url_path = '/data/v2/news'
        return self._fetch_data(url_path, **kwargs)

    def list_news_feeds(self, **kwargs):
        """
        Returns all the news feeds (providers) that CryptoCompare has integrated with.
        """
        url_path = '/data/news/feeds'
        return self._fetch_data(url_path, **kwargs)

    def news_article_categories(self, **kwargs):
        """
        Returns news articles categories, you can use them to filter news.
        """
        url_path = '/data/news/categories'
        return self._fetch_data(url_path, **kwargs)

    def list_news_feeds_and_categories(self, **kwargs):
        """
        Returns all the news feeds (providers) that CryptoCompare has integrated with and the full list of categories.
        """
        url_path = '/data/news/feedsandcategories'
        return self._fetch_data(url_path, **kwargs)


class Info(CryptoCompareBase):

    def all_exchanges_and_trading_pairs(self, **kwargs):
        """
        Returns all the exchanges that CryptoCompare has integrated with.
        """
        url_path = '/data/all/exchanges'
        return self._fetch_data(url_path, **kwargs)

    def cccagg_constituent_exchanges(self, **kwargs):
        """
        Returns all the exchanges that CryptoCompare has integrated with and their status,
        including whether or not they are excluded from pricing and volumes.
        """
        url_path = '/data/all/cccaggexchanges'
        return self._fetch_data(url_path, **kwargs)

    def coin_list(self, **kwargs):
        """
        Returns all the coins that CryptoCompare has added to the website.
        This is not the full list of coins we have in the system,
        it is just the list of coins we have done some research on.
        """
        url_path = '/data/all/coinlist'
        return self._fetch_data(url_path, **kwargs)

    def rate_limits(self, **kwargs):
        """
        Get the rate limits left for you on the history,
        price and news paths in the current hour, minute and second.
        """
        url_path = '/stats/rate/limit'
        return self._fetch_data(url_path, **kwargs)


class CryptoCompare(Price, HistoryDate, TopList, Streaming, News, Info, CryptoCompareBase):
    pass
