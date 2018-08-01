# -*- coding: utf-8 -*-

ENTERPRISE_MAPPING = {
    'enterprise_retrieve': {
        'resource': '/enterprises/{id}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesid'
        ),
        'methods': ['GET'],
    },
    'enterprise_admin_list': {
        'resource': '/enterprises/{id}/admins',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesidadmins'
        ),
        'methods': ['GET'],
    },
    'enterprise_signup_retrieve': {
        'resource': '/enterprises/{id}/signupUrl',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesidsignupurl'
        ),
        'methods': ['GET'],
    },
    'enterprise_member_list': {
        'resource': '/enterprises/{id}/members',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesidmembers'
        ),
        'methods': ['GET'],
    },
    'enterprise_member_retrieve': {
        'resource': '/enterprises/{id}/members/{idMember}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesidmembersidmember'
        ),
        'methods': ['GET'],
    },
    'enterprise_organization_transfer_retrieve': {
        'resource': (
            '/enterprises/{id}/transferrable/organization/{idOrganization}'
        ),
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesidtransferrableorganizationidorganization'
        ),
        'methods': ['GET'],
    },
    'enterprise_member_activation_update': {
        'resource': '/enterprises/{id}/members/{idMember}/deactivated',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesidmembersidmemberdeactivated-1'
        ),
        'methods': ['PUT'],
    },
    'enterprise_organization_transfer': {
        'resource': '/enterprises/{id}/organizations',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesidadminsidmember'
        ),
        'methods': ['PUT'],
    },
    'enterprise_admin_update': {
        'resource': '/enterprises/{id}/admins/{idMember}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesidadminsidmember-1'
        ),
        'methods': ['PUT'],
    },
    'enterprise_token_create': {
        'resource': '/enterprises/{id}/tokens',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesidtokens'
        ),
        'methods': ['POST'],
    },
    'enterprise_organization_delete': {
        'resource': '/enterprises/{id}/organizations/{idOrganization}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesidorganizationsidorganization'
        ),
        'methods': ['DELETE'],
    },
    'enterprise_admin_delete': {
        'resource': '/enterprises/{id}/admins/{idMember}',
        'docs': (
            'https://developers.trello.com/v1.0/reference'
            '#enterprisesidadminsidmember-2'
        ),
        'methods': ['DELETE'],
    },
}
