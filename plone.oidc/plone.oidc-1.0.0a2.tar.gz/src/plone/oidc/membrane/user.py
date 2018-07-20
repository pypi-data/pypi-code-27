# -*- coding: utf-8 -*-
# @Date    : 2018-07-20 09:37:03
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from dexterity.membrane.content.member import IEmail
from plone import schema
from plone.oidc import _


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


class IBaseUser(IEmail):
    """"Membrane based based user Class."""
    first_name = schema.TextLine(
        title=_('First Name'),
    )
    last_name = schema.TextLine(
        title=_('Last name')
        )
    mfa = schema.Choice(
        title=_('Multi-factor authentication (MFA)'),
        required=False,
        vocabulary='mfa_types'
        )
    oidc_enabled = schema.Bool(
        title=_('Is OpenID Connect enabled'),
        required=False,
        )
