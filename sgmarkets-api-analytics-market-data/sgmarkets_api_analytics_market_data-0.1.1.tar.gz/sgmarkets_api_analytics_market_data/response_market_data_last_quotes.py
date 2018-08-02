import numpy as np
import pandas as pd
from IPython.display import Markdown

class ResponseMktDataLastQuotes:
    def __init__(self,
                 raw_data=None, format_response='df_isins_as_columns'):

        assert isinstance(raw_data, list), """ raw data must be a list"""
        self.dic_raw = raw_data
        self.format_response = format_response
        self.res = self.build_df_res()

    def build_df_res(self):
        res_ = {d['instrument']: self.concat_fields_df(d) for d in self.dic_raw}
        if self.format_response.lower() == 'dic_isins_as_keys':
            return res_
        elif self.format_response.lower() == 'df_isins_as_columns' or self.format_response.lower() == 'df_fields_as_columns':
            res_ = {d['instrument']: self.concat_fields_df(d).T for d in self.dic_raw}
            tmp = pd.concat(res_, axis=1, sort=True)
            tmp.columns = tmp.columns.droplevel(1)
            if self.format_response.lower == 'df_isins_as_columns':
                return tmp.T
            else:
                return tmp
        elif self.format_response.lower() == 'multiindex_isins_fields':
            return pd.concat(res_, axis=1,sort=True)
        elif self.format_response.lower() == 'dic_fields_as_keys' or self.format_response.lower() == 'multiindex_fields_isins':
            a = []
            res_dic = {}
            fields_list = self.longest_list_of_fields(self.dic_raw)
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
        value = [dic['value'] for dic in v_list]
        date=['last']*len(value)
        return pd.DataFrame(value, index=date, columns=[ind])

    def concat_fields_df(self, dic):
        assert 'fields' in dic.keys(), 'fields should be a key of JSON response. Response: {}'.format(dic)
        df = [self.unpack_values(d['values'], d['name']) for k,d_f in dic['fields'].items() for d in d_f if d_f]
        return pd.concat(df, axis=1,sort=True)

    def longest_list_of_fields(self, list_quotes):
        indic = []
        for l in list_quotes:
            indic.append([n['name'] for k,nn in l['fields'].items() for n in nn if nn])
        tmp = 0
        for l in indic:
            if len(l) > tmp:
                max = l
                tmp += len(l)
        return max


    def info(self):

        md="""**ResponseMktDataLastQuotes** contains only one attributes .res.
- **res** could be a df or a dic depending on the format_response selected.
        """
        return Markdown(md)
