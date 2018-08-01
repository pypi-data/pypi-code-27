# -*- coding: utf-8 -*-

CHECKLIST_MAPPING = {
    'checklist_retrieve': {
        'resource': '/checklists/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsid'
        ),
        'methods': ['GET'],
    },
    'checklist_field_retrieve': {
        'resource': '/checklists/{id}/{field}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsidfield'
        ),
        'methods': ['GET'],
    },
    'checklist_board_retrieve': {
        'resource': '/checklists/{id}/board',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsidboard'
        ),
        'methods': ['GET'],
    },
    'checklist_card_retrieve': {
        'resource': '/checklists/{id}/cards',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsidcards'
        ),
        'methods': ['GET'],
    },
    'checklist_item_list': {
        'resource': '/checklists/{id}/checkItems',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsidcardscheckitems'
        ),
        'methods': ['GET'],
    },
    'checklist_item_retrieve': {
        'resource': '/checklists/{id}/checkItems/{idCheckItem}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsidcardscheckitemscheckitemid'
        ),
        'methods': ['GET'],
    },
    'checklist_update': {
        'resource': '/checklists/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsid-1'
        ),
        'methods': ['PUT'],
    },
    'checklist_item_update': {
        'resource': '/checklists/{id}/checkItems/{idCheckItem}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsidcheckitemsidcheckitem'
        ),
        'methods': ['PUT'],
    },
    'checklist_name_update': {
        'resource': '/checklists/{id}/name',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsidname'
        ),
        'methods': ['PUT'],
    },
    'checklist_create': {
        'resource': '/checklists',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklists'
        ),
        'methods': ['POST'],
    },
    'checklist_item_create': {
        'resource': '/checklists/{id}/checkItems',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsidcheckitems'
        ),
        'methods': ['POST'],
    },
    'checklist_delete': {
        'resource': '/checklists/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsid-2'
        ),
        'methods': ['DELETE'],
    },
    'checklist_item_delete': {
        'resource': '/checklists/{id}/checkItems/{idCheckItem}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#checklistsidcheckitemsid'
        ),
        'methods': ['DELETE'],
    },
}
