import abc
from typing import Dict

from clean.auth.perm_inspector import PermissionInspector
from clean.entities.token import UserToken
from clean.exceptions import AuthException


class DecodeToken(metaclass=abc.ABCMeta):

    class Meta:
        PERM_VERIFIER_CLASS = PermissionInspector
        ERROR_FUNC = None

    def __init__(self, raw_token: str,
                 kwargs_perm: Dict=None):
        self.raw_token = raw_token
        self.user_token = UserToken(username='', email='', photo_url='').to_dict()
        self.kwargs_perm = {} if kwargs_perm is None else kwargs_perm

    @abc.abstractmethod
    def verify(self, token: str) -> Dict:
        """"""

    def is_valid(self) -> Dict:
        self.decode()
        self.verify_permissions()
        return self.user_token

    def decode(self):
        token = self.raw_token
        if token is None:
            raise AuthException('token not found')
        self.user_token = self.verify(token=token)

    def verify_permissions(self):
        perm = self.Meta.PERM_VERIFIER_CLASS(**self.kwargs_perm)
        if perm.verify(self.user_token) is False:
            raise AuthException('user has not permission')

    def create_resp_err(self, error_msg: str):
        if callable(self.Meta.ERROR_FUNC):
            return self.Meta.ERROR_FUNC(error_msg)
        else:
            return {'error': error_msg}
