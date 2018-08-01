# -*- coding: utf-8 -*-

from tapioca import (JSONAdapterMixin, TapiocaAdapter,
                     generate_wrapper_from_adapter)


from .resource_mapping import RESOURCE_MAPPING


class TrelloClientAdapter(JSONAdapterMixin, TapiocaAdapter):

    api_root = 'https://api.trello.com/1/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(TrelloClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs
        )

        auth = {
            'key': api_params.get('key'),
            'token': api_params.get('token'),
        }

        if 'params' in params:
            params['params'].update(auth)
        else:
            params['params'] = auth

        return params

    def get_iterator_list(self, response_data):
        return response_data

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs,
                                         response_data, response):
        pass


Trello = generate_wrapper_from_adapter(TrelloClientAdapter)
