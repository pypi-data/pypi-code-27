import numpy as np
import pandas as pd
from IPython.display import Markdown
from ._error_msg import Error as error


class ResponseMktDataSnapshotQuotes:
    def __init__(self,
                 raw_data=None, format_response='dic_isins_as_keys'):

        assert isinstance(raw_data, dict), error.Msg(0)
        assert 'quotes' in raw_data.keys(), 'quotes should be a key of JSON response. Response: {}'.format(raw_data)
        self.dic_raw = raw_data
        self.format_response = format_response
        self.res = self.build_df_res()

    def build_df_res(self):
        res_ = {d['date']: self.concat_instruments_df(d) for d in self.dic_raw['quotes']}
        if self.format_response.lower() == 'dic_dates_as_keys':
            return res_
        if self.format_response.lower() == 'dic_isins_as_keys':
            return self.make_classic_res(res_)
        if self.format_response.lower() == 'multiindex_isin_fields':
            return pd.concat(self.make_classic_res(res_), axis=1)
        if self.format_response.lower() == 'dic_fields_as_keys' or self.format_response.lower() == 'multiindex_fields_isins':
            a = []
            res_dic = {}
            fields_list = self.longest_list_of_fields(self.dic_raw['quotes'])
            res_ = self.make_classic_res(res_)
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

    def make_classic_res(self, res_):
        result = {}
        for isin in self.list_of_isins(res_):
            df = pd.DataFrame()
            for k, v in res_.items():
                if isin in v.index:
                    tmp = pd.DataFrame([v.loc[isin]], index=[k])
                    df = pd.concat([df, tmp], axis=0)
                else:
                    tmp = pd.DataFrame(np.nan, index=[k], columns=v.columns)
                    df = pd.concat([df, tmp], axis=0)
            result[isin] = df
        return result

    def list_of_isins(self, res_):
        tmp = 0
        for v in res_.values():
            ind = list(v.index)
            if len(ind) > tmp:
                res = ind
                tmp = len(ind)
        return res

    def unpack_values(self, v_list, ind):
        isin = [dic['instrument'] for dic in v_list]
        value = [dic['value'] for dic in v_list]
        return pd.DataFrame(value, index=isin, columns=[ind])

    def concat_instruments_df(self, dic):
        df = [self.unpack_values(d['values'], d['name']) for d in dic['fields']['indicators']]
        return pd.concat(df, axis=1,sort=True)

    def longest_list_of_fields(self, list_quotes):
        indic = []
        for l in list_quotes:
            indic.append([n['name'] for n in l['fields']['indicators']])
        tmp = 0
        for l in indic:
            if len(l) > tmp:
                max = l
            tmp = len(l)
        return max


    def info(self):

        md = """**ResponseMktDataSnapshotQuotes** contains only one attributes .res.
- **res** could be a df or a dic depending on the format_response selected.
                """
        return Markdown(md)
