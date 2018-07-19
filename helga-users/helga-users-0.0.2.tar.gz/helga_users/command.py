from helga.plugins import command, ResponseNotReady
from helga_users import ldap
from twisted.internet import defer


@command('user', help='Usage: helga user <pattern>')
def helga_users(client, channel, nick, message, cmd, args):
    if not args:
        return '%s, specify a nick to search' % nick

    d = ldap.connection()
    d.addCallback(search_callback, client, channel, nick, args)
    d.addErrback(send_err, client, channel)
    raise ResponseNotReady


@defer.inlineCallbacks
def search_callback(conn, client, channel, nick, args):
    searchname = args[0]
    user = yield find_user(conn, searchname)
    if not user:
        client.msg(channel, 'I could not find user data for %s' % searchname)
        defer.returnValue(None)

    # Print user's time
    import arrow
    utc = arrow.utcnow()
    time = utc.to(user.preferredTimeZone)
    timestr = time.strftime('%-l:%M%P')
    message = "%s, it's %s for %s" % (nick, timestr, user.uid)

    # Print user's geographic location
    if user.location:
        client.msg(channel, "%s is in %s" % (user.uid, user.location))

    # Add the delta to this user, if we can.
    questioner = yield find_user(conn, nick)
    if questioner:
        questioner_time = utc.to(questioner.preferredTimeZone)
        delta = time.datetime.replace(tzinfo=None) - \
            questioner_time.datetime.replace(tzinfo=None)
        deltastr = describe_delta(delta)
        message += ' (%s your %s timezone)' % \
            (deltastr, questioner.preferredTimeZone)
    client.msg(channel, message)


def describe_delta(delta):
    """
    Describe a timedelta in human-readable terms.

    eg. "2:00 ahead of"
    eg. "1:00 behind"
    eg. "same as"

    :param delta: datetime.timedelta
    :returns: string
    """
    deltasec = int(delta.total_seconds())
    deltahour, remainder = divmod(deltasec, 3600)
    deltamin = remainder // 60
    deltahour = abs(deltahour)
    if deltasec > 0:
        return '%d:%02d ahead of' % (deltahour, deltamin)
    if deltasec < 0:
        return '%d:%02d behind' % (deltahour, deltamin)
    if deltasec == 0:
        return 'same as'


@defer.inlineCallbacks
def find_user(conn, searchname):
    """
    Search LDAP for this user's IRC nick or UID.

    :return: a User for this "name", or None
    """
    user = None
    try:
        user = yield ldap.user_from_nick(conn, searchname)
    except ldap.NoUsersFoundError:
        try:
            user = yield ldap.user_from_uid(conn, searchname)
        except ldap.NoUsersFoundError:
            pass
    defer.returnValue(user)


def send_err(e, client, channel):
    client.msg(channel, '%s: %s' % (e.type.__name__, e.value))
    # Provide the file and line number if this was an an unexpected error.
    tb = e.getBriefTraceback().split()
    client.msg(channel, str(tb[-1]))
