# -*- coding: utf-8 -*-
# :Project:   SoL -- The User entity
# :Created:   mar 10 lug 2018 07:42:14 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Lele Gaifax
#

from datetime import datetime
import logging

from nacl import pwhash
from nacl.exceptions import InvalidkeyError

from sqlalchemy import (
    Column,
    Sequence,
    func,
    select,
    )
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import object_session
from sqlalchemy.orm.exc import NoResultFound

from ..i18n import translatable_string as N_, gettext as _, ngettext
from . import Base
from .domains import (
    boolean_t,
    email_t,
    flag_t,
    intid_t,
    language_t,
    name_t,
    password_t,
    timestamp_t,
    )
from .errors import OperationAborted
from .utils import normalize


logger = logging.getLogger(__name__)


class User(Base):
    """A single user of the system."""

    __tablename__ = 'users'
    "Related table."

    ## Columns

    iduser = Column(
        intid_t, Sequence('gen_iduser', optional=True),
        primary_key=True,
        nullable=False,
        info=dict(label=N_('User ID'),
                  hint=N_('Unique ID of the user.')))
    """Primary key."""

    created = Column(
        timestamp_t,
        nullable=False,
        default=datetime.utcnow,
        info=dict(label=N_('Created'),
                  hint=N_('Timestamp of record creation.'),
                  type='date', timestamp=True))
    """Timestamp of record creation."""

    email = Column(
        email_t,
        nullable=False,
        unique=True,
        info=dict(label=N_('Email'),
                  hint=N_('Email address of the user.')))
    """Email address of the user."""

    firstname = Column(
        name_t,
        nullable=False,
        info=dict(label=N_('First name'),
                  hint=N_('First name of the user.')))
    """User's first name."""

    lastname = Column(
        name_t,
        nullable=False,
        info=dict(label=N_('Last name'),
                  hint=N_('Last name of the user.')))
    """User's last name."""

    _password = Column(
        password_t,
        name='password',
        nullable=False,
        default='*',
        info=dict(label=N_('Password'),
                  hint=N_('Login password of the user.')))
    """Crypted password."""

    language = Column(
        language_t,
        info=dict(label=N_('Language'),
                  hint=N_('The code of the preferred language by the user.')))
    """The `ISO code <http://en.wikipedia.org/wiki/ISO_639-1>`_ of the preferred
       language of the user."""

    ownersadmin = Column(
        boolean_t,
        nullable=False,
        default=False,
        info=dict(label=N_('Owners Admin'),
                  hint=N_('Whether the user can change ownership of other items.')))
    """Whether the user can change ownership of other items."""

    state = Column(
        flag_t,
        nullable=False,
        default='R',
        info=dict(label=N_('Status'),
                  hint=N_('The status of the user.'),
                  dictionary=dict(R=N_('Registered'),
                                  C=N_('Confirmed'))))
    """The status of the user: ``R`` means *registered*, ``C`` means *confirmed*."""

    lastlogin = Column(
        timestamp_t,
        info=dict(label=N_('Last login'),
                  hint=N_('Timestamp of the last successful login.'),
                  type='date', timestamp=True))

    @classmethod
    def check_insert(klass, session, fields):
        "Prevent duplicated user."

        from pyramid.threadlocal import get_current_registry

        try:
            lname = normalize(fields['lastname'])
            fname = normalize(fields['firstname'])
            email = fields['email']
            if email:
                email = email.strip()
            password = fields['password']
            if password:
                password = password.strip()
        except KeyError:
            raise OperationAborted(_('For a new user "firstname", "lastname", "email" and'
                                     ' "password" fields are mandatory'))
        if not lname or not fname or not email or not password:
            raise OperationAborted(_('For a new user "firstname", "lastname", "email" and'
                                     ' "password" fields are mandatory'))

        settings = get_current_registry().settings
        if settings is None:  # unittests
            settings = {'sol.admin.user': 'admin', 'sol.guest.user': 'guest'}
        if email == settings['sol.admin.user'] or email == settings['sol.guest.user']:
            raise OperationAborted(_('“$email” is reserved, please use a different email',
                                     mapping=dict(email=email)))

        try:
            session.query(User).filter(User.email == email, User.password != '*').one()
        except NoResultFound:
            pass
        else:
            raise OperationAborted(
                _('The user “$email” already exists, please use a different email',
                  mapping=dict(email=email)))

        if len(password) < 6:
            raise OperationAborted(
                _('Password is too weak, use a longer one'))

    def check_update(self, fields):
        "Perform any check before updating the instance."

        from pyramid.threadlocal import get_current_registry

        if 'lastname' in fields:
            lname = normalize(fields['lastname'])
            if not lname:
                raise OperationAborted(_('The "lastname" field of a user cannot be empty'))

        if 'firstname' in fields:
            fname = normalize(fields['firstname'])
            if not fname:
                raise OperationAborted(_('The "firstname" field of a user cannot be empty'))

        if 'password' in fields:
            password = fields['password']
            if password:
                password = password.strip()
                if password != '*' and len(password) < 6:
                    raise OperationAborted(
                        _('Password is too weak, use a longer one'))
            else:
                raise OperationAborted(
                    _('Please provide a valid "password"'))

        if 'email' in fields:
            email = fields['email']
            if email:
                email = email.strip()
                if not email:
                    raise OperationAborted(
                        _('Please provide a valid "email" address'))
            else:
                raise OperationAborted(
                    _('Please provide a valid "email" address'))

            settings = get_current_registry().settings
            if settings is None:  # unittests
                settings = {'sol.admin.user': 'admin', 'sol.guest.user': 'guest'}
            reservedemails = (settings.get('sol.admin.user'), settings.get('sol.guest.user'))
            if email in reservedemails:
                raise OperationAborted(_('“$email” is reserved, please use a different email',
                                         mapping=dict(email=email)))

            session = object_session(self)

            try:
                session.query(User).filter(User.email == email,
                                           User.password != '*',
                                           User.iduser != self.iduser).one()
            except NoResultFound:
                pass
            else:
                raise OperationAborted(
                    _('The user “$email” already exists, please use a different email',
                      mapping=dict(email=email)))

    def delete(self):
        "Prevent deletion if this user owns something."

        from . import Championship, Club, Player, Rating, Tourney

        sess = object_session(self)

        count = sess.execute(select([func.count()],
                                    Tourney.__table__.c.idowner == self.iduser)).scalar()
        if count > 0:
            raise OperationAborted(ngettext(
                'Deletion not allowed: $user owns $count tourney!',
                'Deletion not allowed: $user owns $count tourneys!',
                count, mapping=dict(user=self.caption(html=False), count=count)))

        count = sess.execute(select([func.count()],
                                    Player.__table__.c.idowner == self.iduser)).scalar()
        if count > 0:
            raise OperationAborted(ngettext(
                'Deletion not allowed: $user owns $count player!',
                'Deletion not allowed: $user owns $count players!',
                count, mapping=dict(user=self.caption(html=False), count=count)))

        count = sess.execute(select([func.count()],
                                    Championship.__table__.c.idowner == self.iduser)).scalar()
        if count > 0:
            raise OperationAborted(ngettext(
                'Deletion not allowed: $user owns $count championship!',
                'Deletion not allowed: $user owns $count championships!',
                count, mapping=dict(user=self.caption(html=False), count=count)))

        count = sess.execute(select([func.count()],
                                    Club.__table__.c.idowner == self.iduser)).scalar()
        if count > 0:
            raise OperationAborted(ngettext(
                'Deletion not allowed: $user owns $count club!',
                'Deletion not allowed: $user owns $count clubs!',
                count, mapping=dict(user=self.caption(html=False), count=count)))

        count = sess.execute(select([func.count()],
                                    Rating.__table__.c.idowner == self.iduser)).scalar()
        if count > 0:
            raise OperationAborted(ngettext(
                'Deletion not allowed: $user owns $count rating!',
                'Deletion not allowed: $user owns $count ratings!',
                count, mapping=dict(user=self.caption(html=False), count=count)))

        super().delete()

    @hybrid_property
    def password(self):
        """Return the hashed password of the user."""

        password = self._password
        if password == '*':
            password = None
        return password

    @password.setter
    def password(self, raw_password):
        """Change the password of the user.

        :param raw_password: the raw password, in clear
        """

        if raw_password and raw_password.strip():
            raw_password = raw_password.strip()
            if raw_password != '*':
                self._password = pwhash.str(raw_password.encode('utf-8'))
            else:
                self._password = '*'
        else:
            self._password = '*'

    def check_password(self, raw_password):
        """Check the password.

        :param raw_password: the raw password, in clear
        :rtype: boolean

        Return ``True`` if the `raw_password` matches the user's
        password, ``False`` otherwise.
        """

        if self.state != 'C':
            return False

        if raw_password:
            raw_password = raw_password.strip().encode('utf-8')
            password = self.password
            if password is not None:
                try:
                    return pwhash.verify(password, raw_password)
                except InvalidkeyError:
                    return False

    def caption(self, html=None, localized=True, css_class=None):
        "Description of the user, made up concatenating his names."

        if html is None or html:
            format = N_('<b>$lastname</b> $firstname')
        else:
            format = N_('$lastname $firstname')
        result = _(format, just_subst=not localized, mapping=dict(
            lastname=self.lastname,
            firstname=self.firstname))
        if (html is None or html) and css_class:
            result = '<span class="%s">%s</span>' % (css_class, result)
        return result

    description = property(caption)

    def serialize(self, serializer):
        """Reduce a single user to a simple dictionary.

        :param serializer: a :py:class:`.Serializer` instance
        :rtype: dict
        :returns: a plain dictionary containing a flatified view of this user
        """

        simple = {}
        simple['created'] = self.created
        simple['email'] = self.email
        simple['firstname'] = self.firstname
        simple['lastname'] = self.lastname
        simple['ownersadmin'] = self.ownersadmin
        simple['state'] = self.state
        if self.language:
            simple['language'] = self.language
        if self.lastlogin:
            simple['lastlogin'] = self.lastlogin

        return simple
