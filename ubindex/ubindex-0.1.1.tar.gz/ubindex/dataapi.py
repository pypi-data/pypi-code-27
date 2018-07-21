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

    def get_weight(self, index_name=''):
        """
        Get ubindex list
        """
        df = pd.read_excel(URL%(SERVER, GET_COMPS))
        df['weight'] = df['weight'].map(FORMAT)
        return df
        
        
    

        
def int2time(timestamp):
    import time
    value = time.localtime(timestamp)
    dt = time.strftime('%Y-%m-%d %H:%M:%S', value)
    return dt

