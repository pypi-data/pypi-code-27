import pandas as pd
from IPython.display import Markdown
from ._error_msg import Error as error


class ResponseMktDataInstruments:
    def __init__(self,
                 raw_data=None):
        assert isinstance(raw_data, dict), error.Msg(0)
        self.dic_res = raw_data
        assert 'instruments' in self.dic_res.keys(), 'instruments should be a dic of JSON response. Response: {}'.format(
            self.dic_res)
        self.df_res = self.build_df_res()

    def build_df_res(self):
        res = [i['alias'] for i in self.dic_res['instruments']]
        return pd.DataFrame([res], index=['instruments']).T


    def info(self):
        md="""**ResponseMktDataInstruments** contains one dataframe:
- **df_res** contains all the Instruments found with respect to constraints 
        """
        return Markdown(md)
