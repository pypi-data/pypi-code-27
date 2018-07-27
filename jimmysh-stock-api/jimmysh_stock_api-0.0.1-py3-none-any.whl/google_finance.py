#!/usr/bin/env python 
"""
Retrieve intraday stock data from Google Finance.
"""
import warnings
warnings.filterwarnings("ignore")

import os
import sys
import csv
import datetime
import re
import codecs

import multiprocessing
import pandas as pd
import requests




    
def get_google_finance_intraday(ticker, exchange, period='60', days=1):
    """
    Retrieve intraday stock data from Google Finance.
    Parameters
    ----------
    ticker : str
        Company ticker symbol
    exchange : str
        Exchange of ticker
    period : str
        Interval between stock values in seconds.
    days : int
        Number of days of data to retrieve.
    Returns
    -------
    stock_data : dictionary
        dictionary file containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """
    periods = {'1':1*60, '5':5*60, '10':10*60,'15':15*60, '20':20*60, '30':30*60, '60':60*60}
    
    
    uri = 'https://www.google.com/finance/getprices' \
          '?i={period}&p={days}d&f=d,o,h,l,c,v&q={ticker}&x={exchange}'.format(ticker=ticker,
                                                                          period=periods[period],
                                                                          days=days,
                                                                          exchange=exchange)

    page = requests.get(uri)
    reader = csv.reader(codecs.iterdecode(page.content.splitlines(), "utf-8"))

    columns = ['Close', 'High', 'Low', 'Open', 'Volume']
    rows = []
    times = []
    for row in reader:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+datetime.timedelta(seconds=periods[period]*int(row[0])))
            rows.append(row[1:])
            
    stock_data = {}
    stock_data['ticker'] = ticker
    stock_data['data'] = rows
    stock_data['index'] = pd.DatetimeIndex(times).strftime('%y-%m-%d %H:%M:%S').tolist()
    stock_data['columns'] = columns
    
    return stock_data


def google_intraday_api(tickers, exchanges, period, days):
    """get intraday stocks data
    """
    
    tasks_args = [(ticker,exchage, period, days) for (ticker,exchage) in zip(tickers, exchanges)]
    stocks_data = {}
    cores = multiprocessing.cpu_count() 
    pool = multiprocessing.Pool(processes=cores)
    
    for data in pool.imap(run_get_google_finance_intraday, tasks_args):
        try:
            stocks_data[data['ticker']] = data
        except Exception as e:
            print (e)

    pool.close()
    del pool

    return stocks_data

def run_get_google_finance_intraday(args):
    ticker, exchange, period, days = args
    return get_google_finance_intraday(ticker, exchange, period, days)
