# -*- coding: utf-8 -*-

ACTION_MAPPING = {
    'action_retrieve': {
        'resource': '/actions/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsactionid'
        ),
        'methods': ['GET'],
    },
    'action_field_retrieve': {
        'resource': '/actions/{id}/{field}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsidfield'
        ),
        'methods': ['GET'],
    },
    'action_board_retrieve': {
        'resource': '/actions/{id}/board',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsidboard'
        ),
        'methods': ['GET'],
    },
    'action_card_retrieve': {
        'resource': '/actions/{id}/card',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsidcard'
        ),
        'methods': ['GET'],
    },
    'action_display_retrieve': {
        'resource': '/actions/{id}/display',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsiddisplay'
        ),
        'methods': ['GET'],
    },
    'action_lane_retrieve': {
        'resource': '/actions/{id}/list',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsidlist'
        ),
        'methods': ['GET'],
    },
    'action_member_retrieve': {
        'resource': '/actions/{id}/member',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsidmember'
        ),
        'methods': ['GET'],
    },
    'action_member_creator_retrieve': {
        'resource': '/actions/{id}/memberCreator',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsidmembercreator'
        ),
        'methods': ['GET'],
    },
    'action_organization_retrieve': {
        'resource': '/actions/{id}/organization',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsidorganization'
        ),
        'methods': ['GET'],
    },
    'action_update': {
        'resource': '/actions/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsid'
        ),
        'methods': ['PUT'],
    },
    'action_comment_update': {
        'resource': '/actions/{id}/text',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsidtext'
        ),
        'methods': ['PUT'],
    },
    'action_delete': {
        'resource': '/actions/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#actionsid-1'
        ),
        'methods': ['DELETE'],
    },
}
