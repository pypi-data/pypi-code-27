from elampclient.api_methods import BaseAPIMethods

BASE_URL = 'compose/v1/skills'


class SkillAPIMethods(BaseAPIMethods):

    def list(self, skill=None):
        if skill:
            return self.client.api_call('{}?parent={}'.format(BASE_URL, skill), http_method='get')
        else:
            return self.client.api_call('{}'.format(BASE_URL), http_method='get')

    def list_recents(self):
        return self.client.api_call('{}/recents'.format(BASE_URL), http_method='get')

    def search(self, query):
        return self.client.api_call('{}/search?q={}'.format(BASE_URL, query), http_method='get')

    def get(self, identifier):
        return self.client.api_call('{}/{}'.format(BASE_URL, identifier), http_method='get')

    def create(self, data):
        return self.client.api_call('{}'.format(BASE_URL), http_method='post', post_data=data)

    def update(self, identifier, data):
        return self.client.api_call('{}/{}'.format(BASE_URL, identifier), http_method='patch', post_data=data)

    def delete(self, identifier):
        return self.client.api_call('{}/{}'.format(BASE_URL, identifier), http_method='delete')

    def list_qualifiers(self, identifier):
        return self.client.api_call('{}/{}/qualifiers'.format(BASE_URL, identifier), http_method='get')