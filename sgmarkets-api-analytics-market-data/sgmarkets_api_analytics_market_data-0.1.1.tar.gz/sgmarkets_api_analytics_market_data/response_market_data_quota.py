import pandas as pd
from IPython.display import Markdown
from ._error_msg import Error as error


class ResponseMktDataQuota:
    def __init__(self,
                 raw_data=None):
        assert isinstance(raw_data, dict), error.Msg(0)
        self.dic_res = raw_data
        self.df_res = self.build_df_res()

    def build_df_res(self):
        df = pd.DataFrame.from_dict(self.dic_res, orient='index')
        df.columns = ['Number of requests']
        return df

    def info(self):
        md=""" **ResponseMktDataQuota** contains one dataframe, df_res:
        """
        return Markdown(md)
