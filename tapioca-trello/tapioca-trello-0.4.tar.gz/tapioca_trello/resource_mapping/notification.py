# -*- coding: utf-8 -*-

NOTIFICATION_MAPPING = {
    'notification_retrieve': {
        'resource': '/notifications/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#notificationsid'
        ),
        'methods': ['GET'],
    },
    'notification_field_retrieve': {
        'resource': '/notifications/{id}/{field}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#notificationsidfield'
        ),
        'methods': ['GET'],
    },
    'notification_board_retrieve': {
        'resource': '/notifications/{id}/board',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#notificationsidboard'
        ),
        'methods': ['GET'],
    },
    'notification_card_retrieve': {
        'resource': '/notifications/{id}/card',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#notificationsidcard'
        ),
        'methods': ['GET'],
    },
    'notification_lane_retrieve': {
        'resource': '/notifications/{id}/list',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#notificationsidlist'
        ),
        'methods': ['GET'],
    },
    'notification_member_retrieve': {
        'resource': '/notifications/{id}/member',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#notificationsidmember'
        ),
        'methods': ['GET'],
    },
    'notification_member_creator_retrieve': {
        'resource': '/notifications/{id}/memberCreator',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#notificationsidmembercreator'
        ),
        'methods': ['GET'],
    },
    'notification_organization_retrieve': {
        'resource': '/notifications/{id}/organization',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#notificationsidorganization'
        ),
        'methods': ['GET'],
    },
    'notification_read_status_update': {
        'resource': '/notifications/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#notificationsid-1'
        ),
        'methods': ['PUT'],
    },
    # Possible duplicate endpoint
    'notification_unread_status_update': {
        'resource': '/notifications/{id}/unread',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#notificationsidunread'
        ),
        'methods': ['PUT'],
    },
    'notification_all_read_mark': {
        'resource': '/notifications/all/read',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#notificationsallread'
        ),
        'methods': ['POST'],
    },
}
