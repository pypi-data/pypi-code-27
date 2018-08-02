import pandas as pd
from IPython.display import Markdown

from ._error_msg import Error as error


class ResponseMktDataFieldsValues:
    def __init__(self,
                 raw_data=None):
        assert isinstance(raw_data, dict), error.Msg(0)
        self.dic_res = raw_data
        assert 'values' in self.dic_res.keys(), 'values should be a key in JSON response. Response: {}'.format(
            self.dic_res)
        self.df_res = self.build_df_res()

    def build_df_res(self):
        value = [dic['value'] for dic in self.dic_res['values']]
        instruments = [dic['instrumentCount'] for dic in self.dic_res['values']]
        return pd.DataFrame([value, instruments], index=['value', 'number_of_instruments']).T


    def info(self):
       md="""**ResponseMktDataFieldsValues** contains one dataframe df_res:
- **df_res** contains all the possible value for a given product & field
        """
       return Markdown(md)
