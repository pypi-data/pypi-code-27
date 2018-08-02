import pandas as pd
from ._error_msg import Error as error
from ._util import Util
from IPython.display import Markdown

class ResponseMktDataProduct:
    def __init__(self,
                 raw_data=None):

        assert isinstance(raw_data, dict), error.Msg(0)
        self.products = []
        self.dic_raw = raw_data
        assert 'products' in self.dic_raw.keys(), 'products should be a key of JSON response, Response: {}'.format(
            self.dic_raw)
        self.build_obj()

    def build_obj(self):
        for dic in self.dic_raw['products']:
            nme = dic['name'].replace(' ', '_')
            self.products.append(nme)
            setattr(self, nme, Util.dict2obj(self.build_dic(dic)))

    def build_dic(self, dic):
        dic_res = {'indicators': pd.DataFrame(dic['fields']['indicators'],
                                              columns=['indicators']),
                   'descriptions': pd.DataFrame(dic['fields']['descriptions'],
                                                columns=['descriptions']),
                   'features': pd.DataFrame.from_dict(dic['features'], orient='index'),
                   'instrumentCount': dic['instrumentCount'], 'dbSource': dic['dbSource'],
                   'refSets': self.build_refset_df(dic['refSets'])}
        return dic_res

    @staticmethod
    def build_refset_df(dic_list):
        source = []
        place = []
        time = []
        for l in dic_list:
            source.append(l['source'])
            place.append(l['place'])
            time.append(l['time'])
        return pd.DataFrame([source, place, time], index=['source', 'place', 'time']).T

    def info(self):

        md="""**ResponseMktDataProduct** is a tree object and an independent list:
- **products** is a list of all the products name. Spaces in product names are replace by _. 
        
**Tree**:
- 1st node is the name of the product. E.g: ResponseMktDataProduct.BOND
- 2nd node are indicators, descriptions, features, instrumentCount, dbSource and refSets. 
        """
        return Markdown(md)
