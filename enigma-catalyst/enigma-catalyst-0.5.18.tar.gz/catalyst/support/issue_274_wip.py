import pytz
from datetime import datetime
from catalyst.api import symbol
from catalyst.utils.run_algo import run_algorithm

coin = 'btc'
quote_currency = 'usd'


def initialize(context):
    context.symbol = symbol('%s_%s' % (coin, quote_currency))


def handle_data_polo_partial_candles(context, data):

    print('NOW: {}\n'.format(data.current_dt))

    history = data.history(symbol('btc_usdt'), ['close', 'volume'],
                           bar_count=2,
                           frequency='1D')

    current = data.current(symbol('btc_usdt'), ['close', 'volume'])

    print('CURRENT:')
    print("{}\n".format(current))
    print('HISTORY (2 BARS):')
    print("{}\n".format(history))

    if not hasattr(context, 'i'):
        context.i = 0
    context.i += 1
    if context.i > 5:
        raise Exception('stop')



""""
    history = data.history(sample_symbol_stock, ['close', 'volume'],
                           bar_count=3,
                           frequency='1d')

    current = data.current(sample_symbol_stock, ['close', 'volume'])

    print ('CURRENT: {}'.format(current))
    print ('HISTORY: {}'.format(history))

    if not hasattr(context, 'i'):
        context.i = 0
    context.i += 1
    if context.i > 5:
        raise Exception('stop')
"""


run_algorithm(initialize=lambda ctx: True,
              handle_data=handle_data_polo_partial_candles,
              exchange_name='poloniex',
              quote_currency='usdt',
              algo_namespace='ns',
              live=False,
              data_frequency='daily',
              capital_base=3000,
              start=datetime(2018, 2, 2, 0, 0, 0, 0, pytz.utc),
              end=datetime(2018, 2, 20, 0, 0, 0, 0, pytz.utc))
