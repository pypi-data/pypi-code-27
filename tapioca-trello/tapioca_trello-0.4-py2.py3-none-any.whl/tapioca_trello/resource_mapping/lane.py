# -*- coding: utf-8 -*-

LANE_MAPPING = {
    'lane_retrieve': {
        'resource': '/lists/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsid'
        ),
        'methods': ['GET'],
    },
    'lane_field_retrieve': {
        'resource': '/lists/{id}/{field}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsidfield'
        ),
        'methods': ['GET'],
    },
    'lane_action_retrieve': {
        'resource': '/lists/{id}/actions',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsidactions'
        ),
        'methods': ['GET'],
    },
    'lane_board_retrieve': {
        'resource': '/lists/{id}/board',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsidboard'
        ),
        'methods': ['GET'],
    },
    'lane_card_retrieve': {
        'resource': '/lists/{id}/cards',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsidcards'
        ),
        'methods': ['GET'],
    },
    'lane_update': {
        'resource': '/lists/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsid-1'
        ),
        'methods': ['PUT'],
    },
    'lane_archive': {
        'resource': '/lists/{id}/closed',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsidclosed'
        ),
        'methods': ['PUT'],
    },
    'lane_board_move': {
        'resource': '/lists/{id}/idBoard',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsididboard'
        ),
        'methods': ['PUT'],
    },
    'lane_rename': {
        'resource': '/lists/{id}/name',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsidname'
        ),
        'methods': ['PUT'],
    },
    'lane_position_change': {
        'resource': '/lists/{id}/pos',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            'listsidpos'
        ),
        'methods': ['PUT'],
    },
    'lane_subscribe': {
        'resource': '/lists/{id}/subscribed',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsidsubscribed'
        ),
        'methods': ['PUT'],
    },
    'lane_create': {
        'resource': '/lists',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#lists-1'
        ),
        'methods': ['POST'],
    },
    'lane_card_archive': {
        'resource': '/lists/{id}/archiveAllCards',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsidarchiveallcards'
        ),
        'methods': ['POST'],
    },
    'lane_card_move': {
        'resource': '/lists/{id}/moveAllCards',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#listsidmoveallcards'
        ),
        'methods': ['POST'],
    },
}
