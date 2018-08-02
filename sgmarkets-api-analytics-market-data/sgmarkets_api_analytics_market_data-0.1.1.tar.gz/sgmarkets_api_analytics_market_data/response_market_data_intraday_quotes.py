import numpy as np
import pandas as pd
from IPython.display import Markdown
import datetime
import dateutil.parser
from pytz import timezone


class ResponseMktDataIntradayQuotes:
    def __init__(self,
                 raw_data=None,format_response='dic_isins_as_keys', time_zone='utc'):

        assert isinstance(raw_data, list), "raw data should be a list"
        self.dic_raw = raw_data
        self.format_response = format_response
        self.time_zone = time_zone
        self.res = self.build_df_res()

    def build_df_res(self):
        res_ = {d['instrument']: self.concat_fields_df(d) for d in self.dic_raw}
        if self.format_response.lower() == 'dic_isins_as_keys':
            return res_
        if self.format_response.lower() == 'multiindex_isins_fields':
            return pd.concat(res_, axis=1)
        if self.format_response.lower() == 'dic_fields_as_keys' or self.format_response.lower() == 'multiindex_fields_isins':
            a = []
            res_dic = {}
            fields_list = self.longest_list_of_fields(res_)
            for f in fields_list:
                res = pd.DataFrame()
                for k, v in res_.items():
                    col = v.columns.get_level_values('fields')
                    if f in col:
                        tmp = pd.DataFrame(v[f])
                        tmp.columns = pd.MultiIndex.from_product([[k], tmp.columns])
                        res = pd.concat([res, tmp], axis=1)
                    else:
                        tmp = pd.DataFrame(np.nan, index=res.index, columns=[k])
                        res = pd.concat([res, tmp], axis=1)
                res_dic[f] = res
            if self.format_response.lower() == 'dic_fields_as_keys':
                return res_dic
            else:
                return pd.concat(res_dic, axis=1)

    def unpack_values(self, v_list, ind, typ):
        date = [dic['date'] for dic in v_list]
        value = [dic['value'] for dic in v_list]
        date=self.tz_convert(date)
        col = pd.MultiIndex.from_tuples([(ind, typ)], names=['fields', 'type'])
        df = pd.DataFrame(value, index=date, columns=col)
        return df

    def tz_convert(self,date):
        t=self.time_zone.lower()
        if t == 'utc' or t == 'gmt':
            return date
        elif t == 'london' or t == 'lon':
            tz=timezone('Europe/London')
        elif t== 'paris' or t=='pa':
            tz=timezone('Europe/Paris')
        elif t== 'new-york' or t=='ny':
            tz=timezone('US/Eastern')
        return [self.getDateTimeFromISO8601String(d).astimezone(tz) for d in date]

    def concat_fields_df(self, dic):
        assert 'values' in dic.keys(), 'values should be a key of JSON response. Response: {}'.format(dic)
        df = [self.unpack_values(d['values'], d['description']['indicator'], d['description']['analysis']) for d in
              dic['values']]
        return pd.concat(df, axis=1, sort=True)

    def longest_list_of_fields(self, dic_res):
        tmp = 0
        for k, v in dic_res.items():
            l = v.columns.get_level_values('fields')
            if len(l) > tmp:
                max = l
            tmp = len(l)
        return max


    def info(self):

        md="""**ResponseMktDataIntradayQuotes** contains only one attributes .res.
- **res** could be a df or a dic depending on the format_response selected.
        """
        return Markdown(md)

    def getDateTimeFromISO8601String(self, s):
        d = dateutil.parser.parse(s)
        return d