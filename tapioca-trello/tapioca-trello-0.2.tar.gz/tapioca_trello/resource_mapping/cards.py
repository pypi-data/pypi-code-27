# -*- coding: utf-8 -*-

CARDS_MAPPING = {
    'card_retrieve': {
        'resource': '/cards/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsid'
        ),
        'methods': ['GET'],
    },
    'card_field_retrieve': {
        'resource': '/cards/{id}/{field}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidfield'
        ),
        'methods': ['GET'],
    },
    'card_action_list': {
        'resource': '/cards/{id}/actions',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidactions'
        ),
        'methods': ['GET'],
    },
    'card_attachment_list': {
        'resource': '/cards/{id}/attachments',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidattachments'
        ),
        'methods': ['GET'],
    },
    'card_attachment_retrieve': {
        'resource': '/cards/{id}/attachments/{idAttachment}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidattachmentsidattachment'
        ),
        'methods': ['GET'],
    },
    'card_board_retrieve': {
        'resource': '/cards/{id}/board',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidboard'
        ),
        'methods': ['GET'],
    },
    'card_checklist_state_list': {
        'resource': '/cards/{id}/checkItemStates',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidcheckitemstates'
        ),
        'methods': ['GET'],
    },
    'card_checklist_list': {
        'resource': '/cards/{id}/checklists',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidchecklists'
        ),
        'methods': ['GET'],
    },
    'card_checklist_item_retrieve': {
        'resource': '/cards/{id}/checkItem/{idCheckItem}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidcheckitemidcheckitem'
        ),
        'methods': ['GET'],
    },
    'card_custom_field_list': {
        'resource': '/cards/{id}/customFieldItems',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidcustomfielditems'
        ),
        'methods': ['GET'],
    },
    'card_lane_retrieve': {
        'resource': '/cards/{id}/list',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidlist'
        ),
        'methods': ['GET'],
    },
    'card_member_list': {
        'resource': '/cards/{id}/members',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidmembers'
        ),
        'methods': ['GET'],
    },
    'card_member_voted_list': {
        'resource': '/cards/{id}/membersVoted',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidmembersvoted'
        ),
        'methods': ['GET'],
    },
    'card_plugin_data_retrieve': {
        'resource': '/cards/{id}/pluginData',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidplugindata'
        ),
        'methods': ['GET'],
    },
    'card_sticker_list': {
        'resource': '/cards/{id}/stickers',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidstickers'
        ),
        'methods': ['GET'],
    },
    'card_sticker_retrieve': {
        'resource': '/cards/{id}/stickers/{idSticker}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidstickersidsticker'
        ),
        'methods': ['GET'],
    },
    'card_update': {
        'resource': '/cards/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsid-1'
        ),
        'methods': ['PUT'],
    },
    'card_comment_update': {
        'resource': '/cards/{id}/actions/{idAction}/comments',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsid-1'
        ),
        'methods': ['PUT'],
    },
    'card_checklist_item_update': {
        'resource': '/cards/{id}/checkItem/{idCheckItem}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidcheckitemidcheckitem-1'
        ),
        'methods': ['PUT'],
    },
    'card_checklist_item_update2': {
        'resource': (
            '/cards/{idCard}/checklist/{idChecklist}/checkItem/{idCheckItem}'
        ),
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidcardchecklistidchecklistcheckitemidcheckitem'
        ),
        'methods': ['PUT'],
    },
    'card_sticker_update': {
        'resource': '/cards/{id}/stickers/{idSticker}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidstickersidsticker-2'
        ),
        'methods': ['PUT'],
    },
    'card_create': {
        'resource': '/cards',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cards-2'
        ),
        'methods': ['POST'],
    },
    'card_comment_create': {
        'resource': '/cards/{id}/actions/comments',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidactionscomments'
        ),
        'methods': ['POST'],
    },
    'card_attachment_create': {
        'resource': '/cards/{id}/attachments',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidattachments-1'
        ),
        'methods': ['POST'],
    },
    'card_checklist_create': {
        'resource': '/cards/{id}/checklists',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidchecklists-1'
        ),
        'methods': ['POST'],
    },
    'card_label_add': {
        'resource': '/cards/{id}/idLabels',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsididlabels'
        ),
        'methods': ['POST'],
    },
    'card_member_add': {
        'resource': '/cards/{id}/idMembers',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsididmembers'
        ),
        'methods': ['POST'],
    },
    'card_label_create': {
        'resource': '/cards/{id}/labels',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidlabels'
        ),
        'methods': ['POST'],
    },
    'card_mark_as_read': {
        'resource': '/cards/{id}/markAssociatedNotificationsRead',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidmarkassociatednotificationsread'
        ),
        'methods': ['POST'],
    },
    'card_member_vote_add': {
        'resource': '/cards/{id}/membersVoted',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidmembersvoted-1'
        ),
        'methods': ['POST'],
    },
    'card_delete': {
        'resource': '/cards/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#delete-card'
        ),
        'methods': ['DELETE'],
    },
    'card_comment_delete': {
        'resource': '/cards/{id}/actions/{idAction}/comments',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidactionsidactioncomments-1'
        ),
        'methods': ['DELETE'],
    },
    'card_attachment_delete': {
        'resource': '/cards/{id}/attachments/{idAttachment}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidattachmentsidattachment-1'
        ),
        'methods': ['DELETE'],
    },
    'card_checklist_item_delete': {
        'resource': '/cards/{id}/checkItem/{idCheckItem}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidcheckitemidcheckitem-2'
        ),
        'methods': ['DELETE'],
    },
    'card_checklist_delete': {
        'resource': '/cards/{id}/checklists/{idChecklist}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidchecklistsidchecklist'
        ),
        'methods': ['DELETE'],
    },
    'card_label_delete': {
        'resource': '/cards/{id}/idLabels/{idLabel}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsididlabelsidlabel'
        ),
        'methods': ['DELETE'],
    },
    'card_member_delete': {
        'resource': '/cards/{id}/idMembers/{idMember}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsididmembersidmember'
        ),
        'methods': ['DELETE'],
    },
    'card_member_vote_delete': {
        'resource': '/cards/{id}/membersVoted/{idMember}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidmembersvotedidmember'
        ),
        'methods': ['DELETE'],
    },
    'card_sticker_delete': {
        'resource': '/cards/{id}/stickers/{idSticker}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#cardsidstickersidsticker-1'
        ),
        'methods': ['DELETE'],
    },
}
