# -*- coding: utf-8 -*-

MEMBER_MAPPING = {
    'member_retrieve': {
        'resource': '/members/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersid'
        ),
        'methods': ['GET'],
    },
    'member_field_retrieve': {
        'resource': '/members/{id}/{field}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidfield'
        ),
        'methods': ['GET'],
    },
    'member_action_list': {
        'resource': '/members/{id}/actions',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidactions'
        ),
        'methods': ['GET'],
    },
    'member_board_list': {
        'resource': '/members/{id}/boards',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboards'
        ),
        'methods': ['GET'],
    },
    'member_board_background_list': {
        'resource': '/members/{id}/boardBackgrounds',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboardbackgrounds'
        ),
        'methods': ['GET'],
    },
    'member_board_background_retrieve': {
        'resource': '/members/{id}/boardBackgrounds/{idBackground}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboardbackgroundsidbackground'
        ),
        'methods': ['GET'],
    },
    'member_board_star_list': {
        'resource': '/members/{id}/boardStars',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboardbackgroundsidbackground'
        ),
        'methods': ['GET'],
    },
    'member_board_star_retrieve': {
        'resource': '/members/{id}/boardStars/{idStar}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboardstarsidstar'
        ),
        'methods': ['GET'],
    },
    'member_invited_board_list': {
        'resource': '/members/{id}/boardsInvited',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboardsinvited'
        ),
        'methods': ['GET'],
    },
    'member_card_list': {
        'resource': '/members/{id}/cards',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcards'
        ),
        'methods': ['GET'],
    },
    'member_custom_board_background_list': {
        'resource': '/members/{id}/customBoardBackgrounds',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcustomboardbackgrounds'
        ),
        'methods': ['GET'],
    },
    'member_custom_board_background_retrieve': {
        'resource': '/members/{id}/customBoardBackgrounds/{idBackground}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcustomboardbackgroundsidbackground'
        ),
        'methods': ['GET'],
    },
    'member_custom_emoji_list': {
        'resource': '/members/{id}/customEmoji',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcustomemoji'
        ),
        'methods': ['GET'],
    },
    'member_custom_emoji_retrieve': {
        'resource': '/members/{id}/customEmoji/{idEmoji}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcustomemojiidemoji'
        ),
        'methods': ['GET'],
    },
    'member_custom_sticker_list': {
        'resource': '/members/{id}/customStickers',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcustomstickers'
        ),
        'methods': ['GET'],
    },
    'member_custom_sticker_retrieve': {
        'resource': '/members/{id}/customStickers/{idSticker}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcustomstickersidsticker'
        ),
        'methods': ['GET'],
    },
    'member_enterprise_list': {
        'resource': '/members/{id}/enterprises/',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidenterprises'
        ),
        'methods': ['GET'],
    },
    'member_notification_list': {
        'resource': '/members/{id}/notifications',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidnotifications'
        ),
        'methods': ['GET'],
    },
    'member_organization_list': {
        'resource': '/members/{id}/organizations',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidorganizations'
        ),
        'methods': ['GET'],
    },
    'member_invited_organization_list': {
        'resource': '/members/{id}/organizationsInvited',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidorganizationsinvited'
        ),
        'methods': ['GET'],
    },
    'member_saved_search_list': {
        'resource': '/members/{id}/savedSearches',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidsavedsearches'
        ),
        'methods': ['GET'],
    },
    'member_saved_search_retrieve': {
        'resource': '/members/{id}/savedSearches/{idSearch}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidsavedsearchesidsearch'
        ),
        'methods': ['GET'],
    },
    'member_token_list': {
        'resource': '/members/{id}/tokens',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidtokens'
        ),
        'methods': ['GET'],
    },
    'member_update': {
        'resource': '/members/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersid-1'
        ),
        'methods': ['PUT'],
    },
    'member_board_background_update': {
        'resource': '/members/{id}/boardBackgrounds/{idBackground}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboardbackgroundsidbackground-1'
        ),
        'methods': ['PUT'],
    },
    'member_board_star_update': {
        'resource': '/members/{id}/boardStars/{idStar}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboardstarsidstar-1'
        ),
        'methods': ['PUT'],
    },
    'member_custom_board_background_update': {
        'resource': '/members/{id}/customBoardBackgrounds/{idBackground}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#put-membersidcustomboardbackgroundsidbackground'
        ),
        'methods': ['PUT'],
    },
    'member_saved_search_update': {
        'resource': '/members/{id}/savedSearches/{idSearch}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidsavedsearchesidsearch-1'
        ),
        'methods': ['PUT'],
    },
    'member_avatar_create': {
        'resource': '/members/{id}/avatar',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidavatar'
        ),
        'methods': ['CREATE'],
    },
    'member_board_background_create': {
        'resource': '/members/{id}/boardBackgrounds',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboardbackgrounds-1'
        ),
        'methods': ['CREATE'],
    },
    'member_board_star_create': {
        'resource': '/members/{id}/boardStars',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboardstars-1'
        ),
        'methods': ['CREATE'],
    },
    'member_custom_board_background_create': {
        'resource': '/members/{id}/customBoardBackgrounds',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcustomboardbackgrounds-1'
        ),
        'methods': ['CREATE'],
    },
    'member_custom_emoji_create': {
        'resource': '/members/{id}/customEmoji',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcustomemoji-1'
        ),
        'methods': ['CREATE'],
    },
    'member_custom_sticker_create': {
        'resource': '/members/{id}/customStickers',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcustomstickers-1'
        ),
        'methods': ['CREATE'],
    },
    'member_message_dismiss': {
        'resource': '/members/{id}/oneTimeMessagesDismissed',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidonetimemessagesdismissed'
        ),
        'methods': ['CREATE'],
    },
    'member_saved_search_create': {
        'resource': '/members/{id}/savedSearches',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidsavedsearches-1'
        ),
        'methods': ['CREATE'],
    },
    'member_board_background_delete': {
        'resource': '/members/{id}/boardBackgrounds/{idBackground}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboardbackgroundsidbackground-2'
        ),
        'methods': ['DELETE'],
    },
    'member_board_star_delete': {
        'resource': '/members/{id}/boardStars/{idStar}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidboardstarsidstar-2'
        ),
        'methods': ['DELETE'],
    },
    'member_custom_board_background_delete': {
        'resource': '/members/{id}/customBoardBackgrounds/{idBackground}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcustomboardbackgroundsidbackground-1'
        ),
        'methods': ['DELETE'],
    },
    'member_custom_sticker_delete': {
        'resource': '/members/{id}/customStickers/{idSticker}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidcustomstickersidsticker-1'
        ),
        'methods': ['DELETE'],
    },
    'member_saved_search_delete': {
        'resource': '/members/{id}/savedSearches/{idSearch}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#membersidsavedsearchesidsearch-2'
        ),
        'methods': ['DELETE'],
    },
}
