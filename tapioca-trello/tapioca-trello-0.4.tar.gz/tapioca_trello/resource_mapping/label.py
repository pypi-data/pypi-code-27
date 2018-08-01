# -*- coding: utf-8 -*-

LABEL_MAPPING = {
    'label_retrieve': {
        'resource': '/labels/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#id'
        ),
        'methods': ['GET'],
    },
    'label_update': {
        'resource': '/labels/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#id-1'
        ),
        'methods': ['PUT'],
    },
    'label_color_update': {
        'resource': '/labels/{id}/color',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#idcolor'
        ),
        'metods': ['PUT'],
    },
    'label_name_update': {
        'resource': '/labels/{id}/name',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#idname'
        ),
        'methods': ['PUT'],
    },
    'label_create': {
        'resource': '/labels',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#page-1'
        ),
        'methods': ['POST'],
    },
    'label_delete': {
        'resource': '/labels',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#id-2'
        ),
        'methods': ['DELETE'],
    },
}
