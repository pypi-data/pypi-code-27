import pandas as pd
from IPython.display import Markdown
from ._error_msg import Error as error


class ResponseMktDataProductFields:
    def __init__(self,
                 raw_data=None):
        assert isinstance(raw_data, dict), error.Msg(0)
        assert 'fields' in raw_data.keys(), 'fields should be a key of JSON response'.format(raw_data)
        self.dic_res = raw_data
        self.df_description, self.df_indicators = self.build_df_res()

    def build_df_res(self):
        res = self.dic_res['fields']
        df_description = pd.DataFrame(res['descriptions'])
        df_description.columns = ['descriptions']
        df_indicators = pd.DataFrame(res['indicators'])
        df_indicators.columns = ['indicators']
        return df_description, df_indicators

    def info(self):
        md="""**ResponseMktDataProductFields** contains two dataframes:
- **df_description** containing all the descriptive fields applicable to the product
- **df_indicators** containing all tje indicators fields applicable to the product
        """
        return Markdown(md)
