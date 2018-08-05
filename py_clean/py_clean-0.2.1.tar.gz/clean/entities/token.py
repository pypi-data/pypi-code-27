from typing import Dict


class UserToken:

    def __init__(self, username: str,
                 email: str,
                 photo_url: str= '',
                 admin: bool=False,
                 staff: bool =False,
                 special: str='',
                 app_meta: Dict=None,
                 user_meta: Dict=None,
                 scopes: Dict=None):
        self.username = username
        self.email = email
        self.photo_url = photo_url
        self.admin = admin
        self.staff = staff
        self.special = special
        self.app_meta = {} if app_meta is None else app_meta
        self.user_meta = {} if user_meta is None else user_meta
        self.scopes = {} if scopes is None else scopes

    @classmethod
    def from_dict(cls, raw: Dict):
        return cls(username=raw['username'],
                   email=raw['email'],
                   photo_url=raw.get('photo_url'),
                   admin=raw.get('admin', False),
                   staff=raw.get('staff', False),
                   special=raw.get('special', 0),
                   app_meta=raw.get('app_meta', {}),
                   user_meta=raw.get('user_meta', {}),
                   scopes=raw.get('scopes', {}))

    def to_dict(self):
        return self.__dict__

    def __eq__(self, other):
        return self.username == other.username and self.email == self.email

    def __repr__(self):
        msg = 'user'
        if self.admin:
            msg = 'admin'
        elif self.staff:
            msg = 'staff'
        elif self.special:
            msg = self.special
        return "I'am {} and have {} permissions.".format(self.username, msg)
