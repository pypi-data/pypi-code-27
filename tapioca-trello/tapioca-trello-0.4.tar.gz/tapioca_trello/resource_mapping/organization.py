# -*- coding: utf-8 -*-

ORGANIZATION_MAPPING = {
    'organization_retrieve': {
        'resource': '/organizations/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsid'
        ),
        'methods': ['GET'],
    },
    'organization_field_retrieve': {
        'resource': '/organizations/{id}/{field}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidfield'
        ),
        'methods': ['GET'],
    },
    'organization_action_list': {
        'resource': '/organizations/{id}/actions',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidactions'
        ),
        'methods': ['GET'],
    },
    'organization_board_list': {
        'resource': '/organizations/{id}/boards',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidboards'
        ),
        'methods': ['GET'],
    },
    'organization_member_list': {
        'resource': '/organizations/{id}/members',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidmembers'
        ),
        'methods': ['GET'],
    },
    'organization_member_filter': {
        'resource': '/organizations/{id}/members/{filter}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidmembersfilter'
        ),
        'methods': ['GET'],
    },
    'organization_invited_member_list': {
        'resource': '/organizations/{id}/membersInvited',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidmembersinvited'
        ),
        'methods': ['GET'],
    },
    'organization_membership_list': {
        'resource': '/organizations/{id}/memberships',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidmemberships'
        ),
        'methods': ['GET'],
    },
    'organization_membership_retrieve': {
        'resource': '/organizations/{id}/memberships/{idMembership}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidmembershipsidmembership'
        ),
        'methods': ['GET'],
    },
    'organization_plugindata_retrieve': {
        'resource': '/organizations/{id}/pluginData',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidplugindata'
        ),
        'methods': ['GET'],
    },
    # Experimental resource, as advised in the documentation.
    'organization_tag_list': {
        'resource': '/organizations/{id}/tags',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidtags'
        ),
        'methods': ['GET'],
    },
    'organization_update': {
        'resource': '/organizations/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsid-1'
        ),
        'methods': ['PUT'],
    },
    'organization_membership_update': {
        'resource': '/organizations/{id}/members',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidmembers-1'
        ),
        'methods': ['PUT'],
    },
    'organization_member_type_update': {
        'resource': '/organizations/{id}/members/{idMember}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidmembersidmember'
        ),
        'methods': ['PUT'],
    },
    'organization_member_status_update': {
        'resource': '/organizations/{id}/members/{idMember}/deactivated',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidmembersidmemberdeactivated'
        ),
        'methods': ['PUT'],
    },
    'organization_create': {
        'resource': '/organizations',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizations-1'
        ),
        'methods': ['POST'],
    },
    'organization_logo_set': {
        'resource': '/organizations/{id}/logo',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidlogo'
        ),
        'methods': ['POST'],
    },
    # Experimental resource, as advised in the documentation.
    'organization_tag_create': {
        'resource': '/organizations/{id}/tags',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidtags-1'
        ),
        'methods': ['POST'],
    },
    'organization_remove': {
        'resource': '/organizations/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsid-2'
        ),
        'methods': ['DELETE'],
    },
    'organization_logo_remove': {
        'resource': '/organizations/{id}/logo',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidlogo-1'
        ),
        'methods': ['DELETE'],
    },
    'organization_member_remove': {
        'resource': '/organizations/{id}/members/{idMember}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidmembersidmember-1'
        ),
        'methods': ['DELETE'],
    },
    'organization_member_board_all_remove': {
        'resource': '/organizations/{id}/members/{idMember}/all',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidmembersidmemberall'
        ),
        'methods': ['DELETE'],
    },
    'organization_associated_domain_remove': {
        'resource': '/organizations/{id}/prefs/associatedDomain',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidprefsassociateddomain'
        ),
        'methods': ['DELETE'],
    },
    'organization_domain_restriction_remove': {
        'resource': '/organizations/{id}/prefs/orgInviteRestrict',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidprefsassociateddomain'
        ),
        'methods': ['DELETE'],
    },
    # Experimental resource, as advised in the documentation.
    'organization_tag_remove': {
        'resource': '/organizations/{id}/tags/{idTag}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#organizationsidtagsidtag'
        ),
        'methods': ['DELETE'],
    },
}
