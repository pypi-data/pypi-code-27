# -*- coding:utf-8 -*- 

SERVER = 'tushare.org'
URL = 'http://file.%s/tsdata/ubindex/%s'

GET_COMPS = 'ub_weight.xlsx'
WEIGHT_COMPS = 'ubindex.xlsx'
COLS = ['comps', 'weight', 'date']

FORMAT = lambda x: '%.4f' % x

