# -*- coding: utf-8 -*-

CUSTOM_FIELD_MAPPING = {
    'custom_field_retrieve': {
        'resource': '/customFields/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#customfieldsid-3'
        ),
        'methods': ['GET'],
    },
    'custom_field_update': {
        'resource': '/customFields/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#customfieldsid'
        ),
        'methods': ['PUT'],
    },
    'custom_field_create': {
        'resource': '/customFields',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#customfields'
        ),
        'methods': ['POST'],
    },
    'custom_field_delete': {
        'resource': '/customFields/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#customfieldsid-1'
        ),
        'methods': ['DELETE'],
    },
    'custom_field_option_list': {
        'resource': '/customFields/{id}/options',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#customfieldsidoptions-1'
        ),
        'methods': ['GET'],
    },
    'custom_field_option_retrieve': {
        'resource': '/customFields/{id}/options/{idCustomFieldOption}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#customfieldsidoptionsidcustomfieldoption-3'
        ),
        'methods': ['GET'],
    },
    'custom_field_option_create': {
        'resource': '/customFields/{id}/options',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#customfieldsidoptions-2'
        ),
        'methods': ['POST'],
    },
    'custom_field_option_delete': {
        'resource': '/customfields/{id}/options/{idCustomFieldOption}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#customfieldsidoptionsidcustomfieldoption-1'
        ),
        'methods': ['DELETE'],
    },
}
