import abc

from directory_forms_api_client.client import forms_api_client


class AbstractBackend(abc.ABC):

    def __init__(self, client=forms_api_client, *args, **kwargs):
        self.client = client
        super().__init__(*args, **kwargs)

    @abc.abstractmethod
    def serialize_data(self, data):
        return {}

    def save(self, data):
        serialized_data = self.serialize_data(data)
        return self.client.submit_generic(serialized_data)


class EmailBackend(AbstractBackend):

    BACKEND_NAME = 'email'

    def __init__(self, recipients, *args, **kwargs):
        self.recipients = recipients
        super().__init__(*args, **kwargs)

    def serialize_data(self, data):
        return {
            'data': data,
            'meta': {
                'backend_name': self.BACKEND_NAME,
                'recipients': self.recipients
            }
        }


class ZendeskBackend(AbstractBackend):

    BACKEND_NAME = 'zendesk'

    def serialize_data(self, data):
        return {
            'data': data,
            'meta': {
                'backend_name': self.BACKEND_NAME,
            }
        }
