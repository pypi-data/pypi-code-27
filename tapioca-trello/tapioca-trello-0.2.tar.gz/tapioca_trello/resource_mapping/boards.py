# -*- coding: utf-8 -*-

BOARDS_MAPPING = {
    'board_retrieve': {
        'resource': '/boards/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardid-1'
        ),
        'methods': ['GET'],
    },
    'board_field_retrieve': {
        'resource': '/boards/{id}/{field}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boards-nested-resources'
        ),
        'methods': ['GET'],
    },
    'board_action_list': {
        'resource': '/boards/{id}/actions',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardidactions'
        ),
        'methods': ['GET'],
    },
    'board_plugin_list': {
        'resource': '/boards/{id}/boardPlugins',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidboardplugins'
        ),
        'methods': ['GET'],
    },
    'board_star_list': {
        'resource': '/boards/{id}/boardStars',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardidactions-2'
        ),
        'methods': ['GET'],
    },
    'board_card_list': {
        'resource': '/boards/{id}/cards',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardidtest'
        ),
        'methods': ['GET'],
    },
    'board_card_list_filter': {
        'resource': '/boards/{id}/cards/{filter}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardidcardsfilter'
        ),
        'methods': ['GET'],
    },
    'board_card_retrieve': {
        'resource': '/boards/{id}/cards/{cardId}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardidactions-1'
        ),
        'methods': ['GET'],
    },
    'board_checklist_list': {
        'resource': '/boards/{id}/checklists',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardidactions-3'
        ),
        'methods': ['GET'],
    },
    'board_custom_field_list': {
        'resource': '/boards/{id}/customFields',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidcustomfields'
        ),
        'methods': ['GET'],
    },
    'board_tag_list': {
        'resource': '/boards/{id}/tags',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardididtags'
        ),
        'methods': ['GET'],
    },
    'board_label_list': {
        'resource': '/boards/{id}/labels',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardidlabels'
        ),
        'methods': ['GET'],
    },
    'board_lane_list': {
        'resource': '/boards/{id}/lists',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardidlists'
        ),
        'methods': ['GET'],
    },
    'board_lane_list_filter': {
        'resource': '/boards/{id}/lists/{filter}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardidlistsfilter'
        ),
        'methods': ['GET'],
    },
    'board_member_list': {
        'resource': '/boards/{id}/members',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsboardidmembers'
        ),
        'methods': ['GET'],
    },
    'board_membership_list': {
        'resource': '/boards/{id}/memberships',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidmemberships'
        ),
        'methods': ['GET'],
    },
    'board_power_up_list': {
        'resource': '/boards/{id}/plugins',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidplugins'
        ),
        'methods': ['GET'],
    },
    'board_update': {
        'resource': '/boards/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#idnext'
        ),
        'methods': ['put'],
    },
    'board_member_update': {
        'resource': '/boards/{id}/members',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidlabelnamesmembers'
        ),
        'methods': ['PUT'],
    },
    'board_member_add': {
        'resource': '/boards/{id}/members/{idMember}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidlabelnamesmembersidmember'
        ),
        'methods': ['PUT'],
    },
    'board_membership_add': {
        'resource': '/boards/{id}/memberships/{idMembership}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidlabelnamesmembershipsidmembership'
        ),
        'methods': ['PUT'],
    },
    'board_email_position_update': {
        'resource': '/boards/{id}/myPrefs/emailPosition',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidmyprefsemailposition'
        ),
        'methods': ['PUT'],
    },
    'board_email_list_update': {
        'resource': '/boards/{id}/myPrefs/idEmailList',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidmyprefsidemaillist'
        ),
        'methods': ['PUT'],
    },
    'board_list_guide_update': {
        'resource': '/boards/{id}/myPrefs/showListGuide',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidmyprefsshowlistguide'
        ),
        'methods': ['PUT'],
    },
    'board_sidebar_update': {
        'resource': '/boards/{id}/myPrefs/showSidebar',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidmyprefsshowsidebae'
        ),
        'methods': ['PUT'],
    },
    'board_sidebar_activity_update': {
        'resource': '/boards/{id}/myPrefs/showSidebarActivity',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidmyprefsshowsidebaractivity'
        ),
        'methods': ['PUT'],
    },
    'board_sidebar_action_update': {
        'resource': '/boards/{id}/myPrefs/showSidebarBoardActions',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidmyprefsshowsidebarboardactions'
        ),
        'methods': ['PUT'],
    },
    'board_sidebar_member_update': {
        'resource': '/boards/{id}/myPrefs/showSidebarMembers',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidmyprefsshowsidebarmembers'
        ),
        'methods': ['PUT'],
    },
    'board_create': {
        'resource': '/boards/',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsid'
        ),
        'methods': ['POST'],
    },
    'board_plugin_create': {
        'resource': '/boards/{id}/boardPlugins',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidboardplugins-1'
        ),
        'methods': ['POST'],
    },
    'board_calendar_key_create': {
        'resource': '/boards/{id}/calendarKey/generate',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidcalendarkeygenerate'
        ),
        'methods': ['POST'],
    },
    'board_checklist_create': {
        'resource': '/boards/{id}/checklists',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidchecklists'
        ),
        'methods': ['POST'],
    },
    'board_email_key_create': {
        'resource': '/boards/{id}/emailKey/generate',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidemailkeygenerate'
        ),
        'methods': ['POST'],
    },
    'board_tag_create': {
        'resource': '/boards/{id}/idTags',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsididtags'
        ),
        'methods': ['POST'],
    },
    'board_label_create': {
        'resource': '/boards/{id}/labels',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidlabels'
        ),
        'methods': ['POST'],
    },
    'board_lane_create': {
        'resource': '/boards/{id}/lists',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidlists'
        ),
        'methods': ['POST'],
    },
    'board_mark_as_viewed': {
        'resource': '/boards/{id}/markedAsViewed',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidmarkedasviewed'
        ),
        'methods': ['POST'],
    },
    'board_power_up_create': {
        'resource': '/boards/{id}/powerUps',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidpowerups'
        ),
        'methods': ['POST'],
    },
    'board_delete': {
        'resource': '/boards/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsid-1'
        ),
        'methods': ['DELETE'],
    },
    'board_plugin_delete': {
        'resource': '/boards/{id}/boardPlugins/{idPlugin}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidboardplugins-2'
        ),
        'methods': ['DELETE'],
    },
    'board_member_delete': {
        'resource': '/boards/{id}/members/{idMember}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidmembersidmember'
        ),
        'methods': ['DELETE'],
    },
    'board_power_up_delete': {
        'resource': '/boards/{id}/powerUps/{powerUp}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#boardsidpowerupspowerup'
        ),
        'methods': ['DELETE'],
    },
}
