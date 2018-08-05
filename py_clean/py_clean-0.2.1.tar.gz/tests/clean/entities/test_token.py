from clean.entities.token import UserToken


def test_user_token_obj():
    ut = UserToken(username='crl', email='admin@admin.com', photo_url='', app_meta={})

    assert ut.username == 'crl'
    assert ut.email == 'admin@admin.com'
    assert ut.photo_url == ''
    assert ut.app_meta == {}


def test_user_token_repr():
    ut = UserToken(username='crl', email='admin@admin.com', photo_url='', app_meta={})

    assert str(ut) == "I'am crl and have user permissions."


def test_user_token_repr_with_metadata():
    ut = UserToken(username='crl', email='admin@admin.com', photo_url='', app_meta={'foo': 'bar'})

    assert str(ut) == "I'am crl and have user permissions."


def test_user_token_from_dict():
    expected = UserToken(username='crl', email='admin@admin.com', photo_url='', app_meta={'foo': 'bar'})
    raw = {
        'username': 'crl',
        'email': 'admin@admin.com',
        'avatar': '',
        'metadata': {
            'foo': 'bar'
        }
    }

    res = UserToken.from_dict(raw)
    assert res == expected
