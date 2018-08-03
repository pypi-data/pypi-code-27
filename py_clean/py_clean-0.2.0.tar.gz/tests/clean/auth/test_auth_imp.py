import pytest

from clean.entities.token import UserToken
from clean.auth.abs import DecodeToken
from clean.exceptions import AuthException

perms = {
    'user': {
        'req': 'user'
    },
    'rule': {
        'path': 'scopes.bar',
        'op': 'eq',
        'value': 'foo'
    }
}


class VerifyTokenAuth(DecodeToken):

    def verify(self, token: str):
        return UserToken('crl', 'admin@admin.com',
                         photo_url='',
                         app_meta={'bar': 'foo'},
                         scopes={'bar': 'foo'}).to_dict()


def test_decode_token():
    vt = VerifyTokenAuth(raw_token='token_data', kwargs_perm=perms)
    ut = vt.is_valid()
    assert ut['username'] == 'crl'
    assert ut['email'] == 'admin@admin.com'
    assert ut['photo_url'] == ''


def test_raise_token_is_null():
    with pytest.raises(AuthException) as e:
        vt = VerifyTokenAuth(raw_token=None, kwargs_perm=perms)
        vt.is_valid()

    assert str(e.value) == 'token not found'


def test_permissions():
    vt = VerifyTokenAuth(raw_token='', kwargs_perm=perms)
    ut = vt.is_valid()

    assert ut['username'] == 'crl'


def test_permissions_raises():
    with pytest.raises(AuthException) as e:
        vt = VerifyTokenAuth(raw_token='',
                             kwargs_perm={
                                 'user': {'req': 'user'},
                                 'rule': {
                                     'path': 'scopes.articles.actions',
                                     'op': 'in',
                                     'value': 'w'
                                 }
                             })
        vt.is_valid()

    assert str(e.value) == 'user has not permission'


def test_create_resp():
    vt = VerifyTokenAuth(raw_token='')

    res = vt.create_resp_err('error')

    assert res == {'error': 'error'}


def test_create_resp_func():
    def custom_error_resp(err: str):
        return err

    class V(VerifyTokenAuth):
        class Meta:
            ERROR_FUNC = custom_error_resp

    vt = V(raw_token='')

    res = vt.create_resp_err('error')

    assert res == 'error'
