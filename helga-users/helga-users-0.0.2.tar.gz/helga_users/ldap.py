from twisted.internet import reactor, defer
from ldaptor.protocols.ldap import ldapclient, ldapsyntax, ldapconnector
from helga import settings
from helga_users.user import User


class NoUsersFoundError(Exception):
    """ Found no users in LDAP for this query """
    pass


class MultipleUsersFoundError(Exception):
    """ Found no multiple users in LDAP that matched this query """
    pass


@defer.inlineCallbacks
def connection():
    """
    Connect to our LDAP server

    :returns: a deferred that when fired returns a
              ldaptor.protocols.ldap.ldapclient.LDAPClient
    """
    if not hasattr(settings, 'LDAP'):
        raise RuntimeError('please configure my LDAP settings')
    host = settings.LDAP['host']  # ldap.corp.example.com
    basedn = settings.LDAP['basedn']  # dc=example,dc=com
    c = ldapconnector.LDAPClientCreator(reactor, ldapclient.LDAPClient)
    overrides = {basedn: (host, 389)}
    client = yield c.connect(basedn, overrides=overrides)
    yield client.startTLS()
    yield client.bind()
    defer.returnValue(client)


@defer.inlineCallbacks
def search(client, query, basedn=None):
    """
    Search for "query" at "basedn"

    :param client: LDAPClient
    :param query: string to search, like "(uid=kdreyer)"
    :param basedn: string, or None to use the default Helga LDAP basedn
    :returns: a deferred that when fired returns a list of LDAPEntryWithClient
    """
    if basedn is None:
        basedn = settings.LDAP['basedn']  # dc=example,dc=com
    o = ldapsyntax.LDAPEntry(client, basedn)
    results = yield o.search(filterText=query)
    # for entry in results:
    #     print(entry)
    defer.returnValue(results)


@defer.inlineCallbacks
def user_from_uid(client, uid):
    """
    Find a User from this uid string.

    :param client: LDAPClient
    :param uid: str eg "kdreyer"
    :returns: a deferred that when fired returns a User
    """
    query = '(uid=%s)' % uid
    results = yield search(client, query)
    result = _one_result(results, query)
    user = _to_user(result)
    defer.returnValue(user)


@defer.inlineCallbacks
def user_from_email(client, email):
    """
    Find a User who owns this email address string.

    Note: this does not currently work on RH's LDAP, because accessing this OU
    requires authentication, which we cannot trivially do with ldaptor.

    :param client: LDAPClient
    :param email: str eg "kdreyer@redhat.com"
    :returns: a deferred that when fired returns a User
    """
    key = email.split('@')[0]
    query = '(sendmailMTAKey=%s)' % key
    basedn = settings.LDAP['maildn']  # 'ou=mx,dc=example,dc=com'
    results = yield search(client, query, basedn)
    result = _one_result(results, query)

    values = list(result['sendmailMTAAliasValue'])
    value = values[0]
    uid = value.split('@')[0]  # "kdreyer"
    user = user_from_uid(uid)
    defer.returnValue(user)


@defer.inlineCallbacks
def user_from_nick(client, nick):
    """
    Find a User from this nick string.

    This method queries LDAP for a "rhatNickName" attribute, or whatever we
    have configured in Helga's LDAP settings for "nickattr".

    :param client: LDAPClient
    :param email: str eg "ktdreyer"
    :returns: a deferred that when fired returns a User
    """
    nickattr = settings.LDAP.get('nickattr', 'rhatNickName')
    query = '(%s=%s)' % (nickattr, nick)
    results = yield search(client, query)
    result = _one_result(results, query)
    user = _to_user(result)
    user.nick = nick
    defer.returnValue(user)


def _one_result(results, query):
    """
    Ensure there is exactly one result for this query, and return it.
    """
    if results is None:
        raise NoUsersFoundError(query)
    if len(results) == 0:
        raise NoUsersFoundError(query)
    elif len(results) > 1:
        raise MultipleUsersFoundError(query)
    return results[0]


def _to_user(result):
    """
    Convert a ldaptor LDAPEntryWithClient to User.

    We set all the attributes in the LDAPEntryWithClient to be attributes on
    the User class we return here.

    :param result: LDAPEntryWithClient
    :return: helga_users.User
    """
    uid = list(result['uid'])[0]
    user = User(uid, client=result.client)
    # Set location, if available.
    locattr = settings.LDAP.get('locattr', 'rhatLocation')
    try:
        location = list(result[locattr])[0]
        setattr(user, 'location', location)
    except KeyError:
        pass
    # Assign all raw attributes from LDAP to our User class
    for entry in result.items():
        key, values = entry
        if len(values) > 1:
            setattr(user, key, values)
        else:
            setattr(user, key, values[0])
    return user
