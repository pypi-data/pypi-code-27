from datetime import datetime as dt
from IPython.display import Markdown

import numpy as np
import pandas as pd
from ._error_msg import Error as error


class ResponseMktDataLiveQuotes:
    def __init__(self,
                 raw_data=None, format_response='dic_isins_as_keys', time=dt.now()):

        assert isinstance(raw_data, dict), error.Msg(0)
        self.time = time

        self.dic_raw = raw_data
        assert 'liveQuotes' in self.dic_raw.keys(), 'liveQuotes should be a key of JSON response. Response: {}'.format(
            self.dic_raw)
        self.format_response = format_response
        self.res = self.build_df_res()

    def build_df_res(self):
        res_ = {d['instrument']: self.concat_fields_df(d) for d in self.dic_raw['liveQuotes']}
        if self.format_response.lower() == 'dic_isins_as_keys':
            return res_
        if self.format_response.lower() == 'multiindex_isins_fields':
            return pd.concat(res_, axis=1)
        if self.format_response.lower() == 'dic_fields_as_keys' or self.format_response.lower() == 'multiindex_fields_isins':
            a = []
            res_dic = {}
            fields_list = self.longest_list_of_fields(self.dic_raw['liveQuotes'])
            for f in fields_list:
                res = pd.DataFrame()
                for k, v in res_.items():
                    if f in v.columns:
                        tmp = pd.DataFrame(v[f])
                        tmp.columns = [k]
                        res = pd.concat([res, tmp], axis=1)
                    else:
                        tmp = pd.DataFrame(np.nan, index=res.index, columns=[k])
                        res = pd.concat([res, tmp], axis=1)
                res_dic[f] = res
            if self.format_response.lower() == 'dic_fields_as_keys':
                return res_dic
            else:
                return pd.concat(res_dic, axis=1)

    def unpack_values(self, v_list, ind):
        date = [self.time]
        value = [v_list['value']]
        return pd.DataFrame(value, index=date, columns=[ind])

    def concat_fields_df(self, dic):
        df = [self.unpack_values(d, d['field']) for d in dic['indicators']]
        return pd.concat(df, axis=1)

    def longest_list_of_fields(self, list_quotes):
        indic = []
        for l in list_quotes:
            indic.append([n['field'] for n in l['indicators']])
        tmp = 0
        for l in indic:
            if len(l) > tmp:
                max = l
                tmp += len(l)
        return max


    def info(self):

        md = """**ResponseMktDataLiveQuotes** contains only one attributes .res.
- **res** could be a df or a dic depending on the format_response selected.
                """
        return Markdown(md)

