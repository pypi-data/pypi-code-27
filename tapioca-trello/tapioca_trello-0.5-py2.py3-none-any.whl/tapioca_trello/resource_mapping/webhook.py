# -*- coding: utf-8 -*-

WEBHOOK_MAPPING = {
    'webhook_retrieve': {
        'resource': '/webhooks/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#webhook-object-1'
        ),
        'methods': ['GET'],
    },
    'webhook_field_retrieve': {
        'resource': '/webhooks/{id}/{field}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#webhooksidfield'
        ),
        'methods': ['GET'],
    },
    'webhook_update': {
        'resource': '/webhooks/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#webhooksid'
        ),
        'methods': ['PUT'],
    },
    'webhook_create': {
        'resource': '/webhooks',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#webhooks-2'
        ),
        'methods': ['POST'],
    },
    'webhook_delete': {
        'resource': '/webhooks/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#webhooksid-1'
        ),
        'methods': ['DELETE'],
    },
}
