# -*- coding:utf-8 -*- 
'''
Created on 21/07/2018
@author: Jimmy
@Group: Tushare
'''

import requests
# from .authorize import Authorize
from ubindex.vars import *
from ubindex import base
import pandas as pd

session = requests.Session()

class DataAPI():
# class DataAPI(Authorize):
    def __init__(self, username='', password='', token=''):
        pass
#         Authorize.__init__(self, username, password, token, session)
        ### Authorize
#         self._authorize()
# 
#         if self._isvalid:
#             ### Do smt.
#             pass

    def get_weight(self, date='', index_name='UB10'):
        """
        Get ubindex list
        """
        df = pd.read_excel(URL%(SERVER, WEIGHT_COMPS))
        df['weight'] = df['weight'].map(FORMAT)
        if date is not None and date != '':
            df = df[df.date == date]
        return df
        
        
    

        
def int2time(timestamp):
    import time
    value = time.localtime(timestamp)
    dt = time.strftime('%Y-%m-%d %H:%M:%S', value)
    return dt

