import pytest

from clean.entities.token import UserToken
from clean.auth.abs import DecodeToken
from clean.auth.decorator import DecoratorBuilder
from clean.exceptions import AuthException


class VerifyTokenAuth(DecodeToken):

    def get_token(self):
        raw = self.raw_token.get('token', None)
        if raw is None:
            raise AuthException('null token')
        return raw

    def verify(self, token: str):
        return UserToken('crl', 'admin@admin.com',
                         photo_url='',
                         scopes={'bar': 'foo'},
                         app_meta={'bar': 'foo'}).to_dict()


def test_create_decorator():
    def token_finder():
        return {'token': 'bar'}

    db = DecoratorBuilder(verify_class=VerifyTokenAuth, token_finder_func=token_finder)
    protect = db.create()
    result = dict()

    @protect(user={'req': 'user'})
    def my_endpoint(user_token, *args, **kwargs):
        result['user_token'] = user_token
        return True

    res = my_endpoint()
    usr_token = result['user_token']

    assert res is True
    assert usr_token is not None
    assert usr_token['username'] == 'crl'


def test_auth_exception():
    def token_finder():
        return None

    db = DecoratorBuilder(verify_class=VerifyTokenAuth, token_finder_func=token_finder)
    protect = db.create()
    result = dict()

    @protect()
    def my_endpoint(user_token, *args, **kwargs):
        result['user_token'] = user_token
        return True

    res = my_endpoint()

    assert res == {'error': 'token not found'}


def test_verify_class_is_subclass_of_decode_token():
    def token_finder():
        return None

    db = DecoratorBuilder(verify_class=VerifyTokenAuth, token_finder_func=token_finder)
    protect = db.create()

    assert callable(protect) is True


def test_verify_class_is_not_subclass_of_decode_token():
    def token_finder():
        return None

    class Foo:
        pass

    with pytest.raises(AttributeError):
        DecoratorBuilder(verify_class=Foo, token_finder_func=token_finder)


def test_token_finder_func_is_not_callable():
    token = {}

    with pytest.raises(AttributeError):
        DecoratorBuilder(verify_class=VerifyTokenAuth, token_finder_func=token)


def test_auth_exception_with_invalid_scopes():
    def token_finder():
        return None

    db = DecoratorBuilder(verify_class=VerifyTokenAuth, token_finder_func=token_finder)
    protect = db.create()
    result = dict()

    @protect(user={'req': 'user'}, rule={'path': 'scopes.bar', 'op': 'eq1', 'value': 'foo'})
    def my_endpoint(user_token, *args, **kwargs):
        result['user_token'] = user_token
        return True

    res = my_endpoint()

    assert res == {'error': 'token not found'}


def test_auth_with_valid_scopes():
    def token_finder():
        return {'token': 'bar'}

    db = DecoratorBuilder(verify_class=VerifyTokenAuth, token_finder_func=token_finder)
    protect = db.create()
    result = dict()

    @protect(user={'req': 'user'}, rule={'path': 'scopes.bar', 'op': 'eq', 'value': 'foo'})
    def my_endpoint(user_token, *args, **kwargs):
        result['user_token'] = user_token
        return True

    res = my_endpoint()
    usr_token = result['user_token']

    assert res is True
    assert usr_token is not None
    assert usr_token['username'] == 'crl'
