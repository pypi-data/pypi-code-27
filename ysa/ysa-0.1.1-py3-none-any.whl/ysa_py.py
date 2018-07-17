import requests


class Api:

    __group = 'default'

    def __init__(self, api_url, refreh_token, **kwargs):

        self.__api_url = api_url
        self.__refreh_token = refreh_token

        if 'group' in kwargs:
            self.__group = kwargs['group']

    def __requests(self, method, endpoint, authorization=None):

        return requests.request(
            method,
            self.__api_url+endpoint,
            headers={'Authorization': f'Bearer {authorization}'}
        ).json()

    def __empty(self, *args, **kwargs):
        pass

    def __enabled(self, feature):
        result = self.__requests(
            method='GET',
            endpoint=f'features/{self.__group}/{feature}',
        ).get('data')

        if result:
            return result[0].get('status', False)

        return False

    def feature(self, feature):

        def wrap(f):

            def final_feature(*args, **kwargs):

                if self.__enabled(feature):
                    return f(*args, **kwargs)

                else:
                    return self.__empty(*args, **kwargs)

            return final_feature

        return wrap
