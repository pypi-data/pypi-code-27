import requests
import pandas as pd
import json
import multiprocessing
import random

def get_alphavantage_finance_intraday(ticker, period='15'):
    """
    Retrieve intraday stock data from alphavantage
    Parameters
    ----------
    ticker : str
        Company ticker symbol

    period : str
        Interval between stock values
    
    Returns
    -------
    stock_data : dictionary
        dictionary containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """
    periods = {'1':1, '5':5, '10':10,'15':15, '20':20, '30':30, '60':60}
    
    apikeys = ['X21DKRBIQOJNI83I','ZUPB8P1G4I2N9YGM','5OJXCK8FHCI3492T', 'IB5K70W3YJ95EYDY']
    apikey = random.choice(apikeys)
    
    uri = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY' \
        '&symbol={ticker}&interval={period}min&outputsize=full&apikey={apikey}'.format(ticker=ticker,
                                                                                  period=periods[period],
                                                                                apikey = apikey)
    

    r = requests.get(uri)
    stock_json = r.json()

    df = pd.DataFrame(data = stock_json['Time Series (15min)']).T
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df.index = pd.DatetimeIndex(df.index).strftime('%y-%m-%d %H:%M:%S').tolist()

    stock_json = df.to_json(orient='split')
    stock_data = json.loads(stock_json)
    stock_data['ticker'] = ticker
    
    return stock_data

def alphavantage_intraday_api(tickers, period):
    """Retrieve intraday stock data from alphavantage
    Parameters
    ----------
    tickera : list | str
        Company ticker symbol

    period : str
        Interval between stock values
        option: '1', '5', '10','15', '20', '30', '60'
    Returns
    -------
    stock_data : dictionary
        dictionary containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """
    
    tasks_args = [(ticker,period) for ticker in tickers]
    stocks_data = {}
    cores = multiprocessing.cpu_count() 
    pool = multiprocessing.Pool(processes=cores)
    
    for data in pool.imap(run_get_alphavantage_finance_intraday, tasks_args):
        try:
            stocks_data[data['ticker']] = data
        except Exception as e:
            print (e)

    pool.close()
    del pool

    return stocks_data

def run_get_alphavantage_finance_intraday(args):
    ticker, period = args
    return get_alphavantage_finance_intraday(ticker, period)

