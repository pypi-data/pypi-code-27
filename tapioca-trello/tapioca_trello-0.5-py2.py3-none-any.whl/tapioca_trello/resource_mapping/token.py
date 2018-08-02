# -*- coding: utf-8 -*-

TOKEN_MAPPING = {
    'token_retrieve': {
        'resource': '/tokens/{token}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#tokenstoken'
        ),
        'methods': ['GET'],
    },
    'token_owner_retrieve': {
        'resource': '/tokens/{token}/member',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#tokenstokenmember'
        ),
        'methods': ['GET'],
    },
    'token_webhook_list': {
        'resource': '/tokens/{token}/webhooks',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#tokenstokenwebhooks'
        ),
        'methods': ['GET'],
    },
    'token_webhook_created_retrieve': {
        'resource': '/tokens/{token}/webhooks/{idWebhook}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#tokenstokenwebhooksidwebhook'
        ),
        'methods': ['GET'],
    },
    'token_webhook_create': {
        'resource': '/tokens/{token}/webhooks',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#tokenstokenwebhooks-2'
        ),
        'methods': ['POST'],
    },
    'token_webhook_update': {
        'resource': '/tokens/{token}/webhooks/{webhookId}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#tokenstokenwebhooks-1'
        ),
        'methods': ['PUT'],
    },
    'token_delete': {
        'resource': '/tokens/{token}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#tokenstoken-1'
        ),
        'methods': ['DELETE'],
    },
    'token_webhook_delete': {
        'resource': '/tokens/{token}/webhooks/{idWebhook}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#tokenstokenwebhooksidwebhook-1'
        ),
        'methods': ['DELETE'],
    },
}
