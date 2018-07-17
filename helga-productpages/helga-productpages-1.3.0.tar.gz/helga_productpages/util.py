import re
from twisted.internet import defer
from helga import log
from helga_productpages.task import ReleaseTask
from txproductpages.exceptions import ProductPagesException
from helga import settings


logger = log.getLogger(__name__)


def match_release_phrase(message, phrase):
    """
    Match a release task in this message.

    "helga: rhcs 3.0 beta date"
    "helga: rhcs 3.0 schedule"

    :returns: a ReleaseTask if we matched, or None if no release task.
    """
    botnick = settings.NICK
    pattern = re.compile('%s[,:]? (.+) %s\??$' % (botnick, phrase))
    m = re.match(pattern, message)
    if not m:
        return
    maybe_release = m.group(1)
    result = ReleaseTask.from_text(maybe_release)
    return result


@defer.inlineCallbacks
def release_not_found(pp, release_task, nick):
    """
    Return a deferred that when fired returns a message about this missing
    release.

    :param pp: txproductpages.Connection object
    :param release_task: ReleaseTask object
    :param nick: str, user who asked about this release_task.
    """
    template = '{nick}, I could not find release {release} in {pp} .'
    try:
        # Note: upcoming_releases() does not capture releases without a GA date
        # set (ie. early in the cycle), or releases in the maintenance phase
        # (z-streams). It's not perfect, but at least it's something.
        upcoming = yield pp.upcoming_releases(release_task.product)
    except ProductPagesException:
        upcoming = ()
    if len(upcoming) == 1:
        suggestion = release_to_text(upcoming[0])
        template += ' Maybe you meant "%s"?' % suggestion
    if len(upcoming) > 1:
        template += ' Upcoming %s releases:' % release_task.product
        for release in upcoming:
            template += ' "%s"' % release_to_text(release)
    product_url = pp.product_url(release_task.product)
    message = template.format(nick=nick,
                              release=release_task.shortname,
                              pp=product_url)
    defer.returnValue(message)


def release_to_text(release):
    """
    Translate this Release object into a text string that would trigger this
    plugin's matcher.

    In other words, translate the release into something that could match
    ReleaseTask.from_text().

    :param release: txproductpages.release.Release object
    :returns: str, like "ceph 3.0"
    """
    shortname = release.shortname
    (product, version) = shortname.split('-', 1)
    version = version.replace('-', '.')
    return '%s %s' % (product, version)
