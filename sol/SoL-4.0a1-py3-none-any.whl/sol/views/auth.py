# -*- coding: utf-8 -*-
# :Project:   SoL -- Autentication views
# :Created:   lun 15 apr 2013 16:48:23 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2013, 2014, 2015, 2016, 2018 Lele Gaifax
#

from datetime import datetime
import hashlib
import logging
from collections import OrderedDict
from os.path import isdir
from socket import gethostbyaddr

from sqlalchemy.orm.exc import NoResultFound
import transaction

from itsdangerous import BadData, BadTimeSignature, TimestampSigner
from pyramid.csrf import check_csrf_token
from pyramid.events import NewRequest, subscriber
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound, HTTPGone, HTTPUnauthorized
from pyramid.view import view_config
from pyramid.settings import asbool
from pyramid_mailer.message import Message

from . import get_request_logger
from ..i18n import translatable_string as _, translator
from ..models import DBSession, User, bio


logger = logging.getLogger(__name__)


NO_SUCH_USER = _('No such user!')
INVALID_CREDENTIALS = _('Invalid credentials')
RESERVED_EMAIL = _('Invalid email address')
INVALID_EMAIL = _('Please use a different email address')
MANDATORY_FIELD = _('Mandatory field')
MISSING_FIELDS = _('Missing fields')
FULL_NAME = _('{first_name} {last_name}')
ADMINISTRATOR = _('Administrator')
ANONYMOUS = _('Anonymous')
INVALID_OLD_PASSWORD = _('Invalid old password')
OLD_PASSWORD_DOES_NOT_MATCH = _('Old password does not match')


@subscriber(NewRequest)
def check_authorized_request(event,
                             authorized_paths={'/',
                                               '/auth/login',
                                               '/auth/lostPassword',
                                               '/auth/resetPassword',
                                               '/auth/signin',
                                               '/catalog',
                                               '/extjs-l10n',
                                               '/favicon.ico',
                                               '/robots.txt',
                                               }):
    """Assert the request is authorized.

    This function gets hooked at the Pyramid's ``NewRequest`` event,
    so it will be executed at the start of each new request.

    If the user has been authenticated, or if she is requesting a
    static resource or one of the authentication views, then nothing
    happens. Otherwise an HTTPUnauthorized exception is raised.
    """

    request = event.request

    # Authenticated user?
    session = request.session
    if 'user_id' in session:
        return

    rpath = request.path

    # Anonymous authorized path or static resource?
    sw = rpath.startswith
    if rpath in authorized_paths or sw('/static/') or sw('/desktop/'):
        return
    if request.method == 'GET' and (sw('/bio/')
                                    or sw('/lit/')
                                    or sw('/pdf/')
                                    or sw('/svg/')
                                    or sw('/tourney/countdown')
                                    or sw('/xlsx/')
                                    or rpath == '/lit'):
        return
    if sw('/scripts') and request.registry.settings.get('desktop.debug', False):
        return

    get_request_logger(request, logger).error('Unauthorized access to %s (%s)',
                                              request.path, request.method)

    raise HTTPUnauthorized(_('You must re-authenticate yourself'))


ADMIN_ONLY_MODULES = OrderedDict((
    ("users", dict(
        classname='SoL.module.Users')),
))


MODULES = OrderedDict((
    ("upload", dict(
        classname='SoL.module.Upload')),
    ("clubs", dict(
        classname='SoL.module.Clubs',
        quickstart=dict(
            name=_('Clubs'),
            iconCls='clubs-icon',
            moduleId='clubs-win'))),
    ("championships", dict(
        classname='SoL.module.Championships',
        quickstart=dict(
            name=_('Championships'),
            iconCls='championships-icon',
            moduleId='championships-win'))),
    ("tourneys", dict(
        classname='SoL.module.Tourneys',
        quickstart=dict(
            name=_('Tourneys'),
            iconCls='tourneys-icon',
            moduleId='tourneys-win'))),
    ("tourney", dict(
        classname='SoL.module.Tourney')),
    ("players", dict(
        classname='SoL.module.Players')),
    ("ratings", dict(
        classname='SoL.module.Ratings')),
    ("competitors", dict(
        classname='SoL.module.Competitors')),
    ("ratedplayers", dict(
        classname='SoL.module.RatedPlayers')),
    ("myclubs", dict(
        classname='SoL.module.MyClubs',
        shortcut=dict(
            name=_('My clubs'),
            iconCls='clubs-shortcut-icon',
            moduleId='my-clubs-win'))),
    ("mychampionships", dict(
        classname='SoL.module.MyChampionships',
        shortcut=dict(
            name=_('My championships'),
            iconCls='championships-shortcut-icon',
            moduleId='my-championships-win'))),
    ("mytourneys", dict(
        classname='SoL.module.MyTourneys',
        shortcut=dict(
            name=_('My tourneys'),
            iconCls='tourneys-shortcut-icon',
            moduleId='my-tourneys-win'))),
    ("myplayers", dict(
        classname='SoL.module.MyPlayers',
        shortcut=dict(
            name=_('My players'),
            iconCls='players-shortcut-icon',
            moduleId='my-players-win'))),
    ("myratings", dict(
        classname='SoL.module.MyRatings',
        shortcut=dict(
            name=_('My ratings'),
            iconCls='ratings-shortcut-icon',
            moduleId='my-ratings-win'))),
))


@view_config(route_name='login', renderer='json', request_method='POST')
def auth_user(request):
    from pyramid.i18n import make_localizer
    from pyramid.interfaces import ILocalizer, ITranslationDirectories
    from sol.i18n import available_languages

    t = translator(request)

    data = request.params

    username = data.get('username', None)
    password = data.get('password', None)

    ipaddress = request.client_addr
    try:
        host = gethostbyaddr(ipaddress)
    except Exception:
        hostname = "unknown host"
    else:  # pragma: nocover
        hostname = host[0]

    logger.info('Login attempt by "%s" from %s (%s)', username, hostname, ipaddress)

    if username and password:
        settings = request.registry.settings

        adminuser = settings.get('sol.admin.user')
        adminpwd = settings.get('sol.admin.password')
        guestuser = settings.get('sol.guest.user')
        guestpwd = settings.get('sol.guest.password')

        is_admin = False
        is_ownersadmin = False
        is_guest = False
        user_id = None
        ui_language = None

        if adminuser and username == adminuser:
            if password == adminpwd:
                is_admin = is_ownersadmin = True
                fullname = t(ADMINISTRATOR)
            else:
                return {'success': False,
                        'message': t(NO_SUCH_USER),
                        'errors': {'username': t(INVALID_CREDENTIALS),
                                   'password': t(INVALID_CREDENTIALS)}}
        elif guestuser and username == guestuser:
            if password == guestpwd:
                is_guest = True
                fullname = t(ANONYMOUS)
            else:
                return {'success': False,
                        'message': t(NO_SUCH_USER),
                        'errors': {'username': t(INVALID_CREDENTIALS),
                                   'password': t(INVALID_CREDENTIALS)}}
        else:
            sasess = DBSession()
            user = sasess.query(User).filter(User.email == username,
                                             User.password != '*',
                                             User.state == 'C').one_or_none()
            if user is None or not user.check_password(password):
                return {'success': False,
                        'message': t(NO_SUCH_USER),
                        'errors': {'username': t(INVALID_CREDENTIALS),
                                   'password': t(INVALID_CREDENTIALS)}}
            else:
                user_id = user.iduser
                is_ownersadmin = user.ownersadmin
                first_name = user.firstname
                last_name = user.lastname
                if user.language in available_languages:
                    ui_language = user.language

                if first_name and last_name:
                    fullname = t(FULL_NAME).format(
                        first_name=first_name, last_name=last_name)
                else:  # pragma: nocover
                    fullname = username
                user.lastlogin = datetime.utcnow()

        s = request.session
        s['user_id'] = user_id
        s['user_name'] = username
        s['is_admin'] = is_admin
        s['is_ownersadmin'] = is_ownersadmin
        s['is_guest'] = is_guest
        s['ui_language'] = ui_language

        def translate_name(cfg):
            copy = dict(cfg)
            copy['name'] = t(copy['name'])
            return copy

        if ui_language:
            req_language = request.accept_language.best_match(
                available_languages, 'en')
            reload_l10n = ui_language != req_language

            if reload_l10n:
                # Reset the Pyramid request localizer to use the preferred language
                registry = request.registry
                request._LOCALE_ = ui_language
                localizer = registry.queryUtility(ILocalizer, name=ui_language)

                if localizer is None:
                    tdirs = registry.queryUtility(ITranslationDirectories, default=[])
                    localizer = make_localizer(ui_language, tdirs)
                    registry.registerUtility(localizer, ILocalizer, name=ui_language)

                request.localizer = localizer
        else:
            reload_l10n = False

        modules = [MODULES[m]['classname'] for m in MODULES
                   if not is_guest or m != 'upload']
        if is_admin:
            modules += [ADMIN_ONLY_MODULES[m]['classname'] for m in ADMIN_ONLY_MODULES]
        result = {
            'success': True,
            'fullname': fullname,
            'is_admin': is_admin,
            'is_ownersadmin': is_ownersadmin,
            'user_id': user_id,
            'reload_l10n': reload_l10n,
            'modules': modules,
            'shortcuts': [] if is_guest else [translate_name(sc)
                                              for sc in [MODULES[m]['shortcut']
                                                         for m in MODULES
                                                         if 'shortcut' in MODULES[m]]],
            'quickstart': [translate_name(qs)
                           for qs in [MODULES[m]['quickstart']
                                      for m in MODULES
                                      if 'quickstart' in MODULES[m]]]
        }

        get_request_logger(request, logger).info('New session for %s', fullname)

        return result
    else:  # pragma: no cover
        errors = {}
        if not username:
            errors['username'] = t(MANDATORY_FIELD)
        if not password:
            errors['password'] = t(MANDATORY_FIELD)
        return {'success': False,
                'message': t(MISSING_FIELDS),
                'errors': errors}


@view_config(route_name='logout', renderer='json')
def logout(request):
    s = request.session

    get_request_logger(request, logger).info('Session terminated')

    if s['user_id'] or s['is_admin']:  # not for guest users
        settings = request.registry.settings
        bckdir = settings.get('sol.backups_dir', None)
        if bckdir and isdir(bckdir):
            logger.info('Performing a database backup, just in case...')

            pdir = settings['sol.portraits_dir']
            edir = settings['sol.emblems_dir']

            with transaction.manager:
                bio.backup(DBSession(), pdir, edir, bckdir,
                           serialization_format='json', native_when_possible=True)

    s.invalidate()

    return {'success': True, 'message': 'Goodbye'}


CONFIRM_MESSAGE = _("""\
Hello {firstname},

you received this message because somebody, possibly you, requested a new account on
the SoL instance at {hostname}.

If it was not you, sorry for the inconvenience: just ignore this email, and the request
won't be fulfilled and eventually trashed.

Otherwise, you have two days starting from now to visit the following link to complete the
registration form:

  {confirm_url}

Best regards and happy carromming!
""")


@view_config(route_name='signin', renderer='json', request_method='POST')
def create_new_user(request):
    settings = request.registry.settings

    if not asbool(settings.get('sol.enable_signin')):  # pragma: nocover
        raise HTTPBadRequest()

    check_csrf_token(request)

    t = translator(request)

    data = request.params

    email = data.get('email', None)
    if email:
        email = email.strip()
    firstname = data.get('firstname', None)
    if firstname:
        firstname = firstname.strip()
    lastname = data.get('lastname', None)
    if lastname:
        lastname = lastname.strip()
    password = data.get('password', None)

    ipaddress = request.client_addr
    try:
        host = gethostbyaddr(ipaddress)
    except Exception:
        hostname = "unknown host"
    else:  # pragma: nocover
        hostname = host[0]

    logger.info('Sign in attempt by "%s" from %s (%s)', email, hostname, ipaddress)

    if email and firstname and lastname and password:
        adminuser = settings.get('sol.admin.user')
        guestuser = settings.get('sol.guest.user')

        if (adminuser and email == adminuser) or (guestuser and email == guestuser):
            return {'success': False,
                    'message': t(RESERVED_EMAIL),
                    'errors': {'email': t(INVALID_EMAIL)}}

        sasess = DBSession()
        user = sasess.query(User).filter(User.email == email).one_or_none()

        if user is not None:
            return {'success': False,
                    'message': t(RESERVED_EMAIL),
                    'errors': {'email': t(INVALID_EMAIL)}}

        user = User(email=email, firstname=firstname, lastname=lastname, password=password)
        sasess.add(user)
        sasess.flush()

        sender = settings.get('mail.default_sender')
        s = TimestampSigner(settings['sol.signer_secret_key'])
        signed_id = s.sign(str(user.iduser)).decode('ascii')
        confirm_url = request.route_url('signin', _query={'confirm': signed_id})
        body = t(CONFIRM_MESSAGE).format(firstname=firstname,
                                         hostname=request.route_url('app'),
                                         confirm_url=confirm_url)
        message = Message(subject=t(_('Confirm your SoL account')),
                          sender=sender,
                          recipients=[email],
                          body=body)

        request.mailer.send(message)
        logger.debug('Sent email to %s with the activation link: %s', email, confirm_url)

        return {
            'success': True,
            'message': t(_('Email sent!'))
        }
    else:  # pragma: no cover
        errors = {}
        if not email:
            errors['email'] = t(MANDATORY_FIELD)
        if not firstname:
            errors['firstname'] = t(MANDATORY_FIELD)
        if not lastname:
            errors['lastname'] = t(MANDATORY_FIELD)
        if not password:
            errors['password'] = t(MANDATORY_FIELD)
        return {'success': False,
                'message': t(MISSING_FIELDS),
                'errors': errors}


REGISTRATION_MESSAGE = _("""\
Hello again,

this to confirm that your registration has been successfully completed: you can now access
your own account at {login_url} and start using SoL.

Use this email address as the “username” and provide the same password you specified in the
request.

Best regards and happy carromming!
""")


@view_config(route_name='signin', request_method='GET')
def confirm_new_user(request):
    settings = request.registry.settings

    if not asbool(settings.get('sol.enable_signin')):  # pragma: nocover
        raise HTTPBadRequest()

    signed_id = request.params.get('confirm')
    if signed_id is not None:
        s = TimestampSigner(settings['sol.signer_secret_key'])
        max_age = 60 * 60 * 24 * 2  # in seconds, two days
        try:
            id = s.unsign(signed_id, max_age=max_age)
        except BadTimeSignature as e:
            logger.warning('User token %r expired: %s', signed_id, e)
            raise HTTPGone()
        except BadData:
            raise HTTPBadRequest()
        else:
            id = int(id.decode('ascii'))
    else:
        raise HTTPBadRequest()

    sasess = DBSession()
    user = sasess.query(User).get(id)

    if user is None:
        raise HTTPBadRequest()
    elif user.state != 'R':
        raise HTTPGone()

    user.state = 'C'
    sasess.flush()

    t = translator(request)

    login_url = request.route_url('app')
    body = t(REGISTRATION_MESSAGE).format(login_url=login_url)
    sender = settings.get('mail.default_sender')
    message = Message(subject=t(_('Your new SoL account has been activated')),
                      sender=sender,
                      recipients=[user.email],
                      body=body)

    request.mailer.send(message)
    logger.debug('Sent confirmation email to %s', user.email)

    return HTTPFound(location=login_url)


RESET_MESSAGE = _("""\
Hello {firstname},

you received this message because somebody, possibly you, requested a password reset of
your account on the SoL instance at {hostname}.

If it was not you, sorry for the inconvenience: just ignore this email, and the request
won't be fulfilled and eventually trashed.

Otherwise, you have two days starting from now to visit the following link to complete the
procedure:

  {reset_password_url}

Best regards and happy carromming!
""")


@view_config(route_name='lost_password', renderer='json', request_method='POST')
def lost_password(request):
    settings = request.registry.settings

    if not asbool(settings.get('sol.enable_password_reset')):  # pragma: nocover
        raise HTTPBadRequest()

    check_csrf_token(request)

    t = translator(request)

    data = request.params

    email = data.get('email', None)
    if email:
        email = email.strip()

    ipaddress = request.client_addr
    try:
        host = gethostbyaddr(ipaddress)
    except Exception:
        hostname = "unknown host"
    else:  # pragma: nocover
        hostname = host[0]

    logger.info('Lost password request by "%s" from %s (%s)', email, hostname, ipaddress)

    if email:
        adminuser = settings.get('sol.admin.user')
        guestuser = settings.get('sol.guest.user')

        if (adminuser and email == adminuser) or (guestuser and email == guestuser):
            return {'success': False,
                    'message': t(RESERVED_EMAIL),
                    'errors': {'email': t(INVALID_EMAIL)}}

        sasess = DBSession()
        try:
            user = sasess.query(User).filter(User.email == email).one()
        except NoResultFound:
            return {'success': False,
                    'message': t(NO_SUCH_USER),
                    'errors': {'email': t(INVALID_EMAIL)}}
        else:
            if user.state != 'C':
                return {'success': False,
                        'message': t(NO_SUCH_USER),
                        'errors': {'email': t(INVALID_EMAIL)}}

        sender = settings.get('mail.default_sender')
        s = TimestampSigner(settings['sol.signer_secret_key'])
        token = '%s-%s' % (user.iduser, hashlib.md5(user._password).hexdigest())
        signed_token = s.sign(token).decode('ascii')
        reset_password_url = request.route_url('app', _anchor='reset_password=' + signed_token)
        body = t(RESET_MESSAGE).format(firstname=user.firstname,
                                       hostname=request.route_url('app'),
                                       reset_password_url=reset_password_url)
        message = Message(subject=t(_('Confirm password reset for your SoL account')),
                          sender=sender,
                          recipients=[email],
                          body=body)

        request.mailer.send(message)
        logger.debug('Sent email to %s with the password reset link: %s',
                     email, reset_password_url)

        return {
            'success': True,
            'message': t(_('Email sent!'))
        }
    else:  # pragma: no cover
        return {'success': False,
                'message': t(MISSING_FIELDS),
                'errors': {'email': t(MANDATORY_FIELD)}}


@view_config(route_name='reset_password', renderer='json', request_method='POST')
def reset_password(request):
    settings = request.registry.settings

    if not asbool(settings.get('sol.enable_password_reset')):  # pragma: nocover
        raise HTTPBadRequest()

    signed_token = request.params.get('token')
    password = request.params.get('password')

    if signed_token is not None and password is not None:
        s = TimestampSigner(settings['sol.signer_secret_key'])
        max_age = 60 * 60 * 24 * 2  # in seconds, two days
        try:
            token = s.unsign(signed_token, max_age=max_age)
        except BadTimeSignature as e:
            logger.warning('User token %r expired: %s', signed_token, e)
            raise HTTPGone()
        except BadData:
            raise HTTPBadRequest()
        else:
            id, oldpwhash = token.decode('ascii').split('-', 1)
            id = int(id)
    else:
        raise HTTPBadRequest()

    sasess = DBSession()
    user = sasess.query(User).get(id)

    if user is None or user.state != 'C':
        raise HTTPBadRequest()

    if hashlib.md5(user._password).hexdigest() != oldpwhash:
        raise HTTPGone()

    user.password = password
    sasess.flush()

    return {
        'success': True,
        'location': request.route_url('app')
    }


@view_config(route_name='change_password', renderer='json', request_method='POST')
def change_password(request):
    user_id = request.session.get('user_id')
    oldpassword = request.params.get('oldpassword')
    newpassword = request.params.get('newpassword')

    if user_id is not None and oldpassword is not None and newpassword is not None:
        sasess = DBSession()
        user = sasess.query(User).get(user_id)
        if user.check_password(oldpassword):
            user.password = newpassword
            sasess.flush()

            return {
                'success': True,
            }
        else:
            t = translator(request)
            return {
                'success': False,
                'message': t(INVALID_OLD_PASSWORD),
                'errors': {'oldpassword': t(OLD_PASSWORD_DOES_NOT_MATCH)}
            }
    else:
        raise HTTPBadRequest()
