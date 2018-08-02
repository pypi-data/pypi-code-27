import pandas as pd


class Util:
    @staticmethod
    def build_url(dic_url):

        return '{}{}{}'.format(dic_url['base_url'], dic_url['service'], dic_url['endpoint'])

    @staticmethod
    def unpack_ref_sets(dic_list):
        source = []
        place = []
        time = []
        for l in dic_list:
            source.append(l['source'])
            place.append(l['place'])
            time.append(l['time'])
        return pd.DataFrame([[source, place, time]], columns=['source', 'place', 'time'])

    def dict2obj(d):
        if isinstance(d, list):
            d = [Util.dict2obj(x) for x in d]
        if not isinstance(d, dict):
            return d
        o = C()
        for k in d:
            o.__dict__[k] = Util.dict2obj(d[k])
        return o


class C(object):
    pass
