from clean.entities.token import UserToken
from clean.auth.perm_inspector import PermissionInspector


def test_not_allow_if_user_is_not_set():
    ut = UserToken(username='crl', email='', photo_url='',
                   app_meta={}, user_meta={}, admin=False, staff=False, scopes={}).to_dict()

    pv = PermissionInspector(user={}, rule={}, allow_super=False)
    assert pv.verify(ut) is False


def test_allow_just_with_token():
    ut = UserToken(username='crl', email='', photo_url='',
                   app_meta={}, user_meta={}, admin=False, staff=False, scopes={}).to_dict()

    pv = PermissionInspector(user={'req': 'user'}, rule={}, allow_super=False)
    assert pv.verify(ut) is True


def test_admin_can_do_anything():
    ut = UserToken(username='crl', email='', photo_url='',
                   app_meta={}, user_meta={}, admin=True, staff=False, scopes={}).to_dict()

    pv = PermissionInspector(user={'req': 'staff'},
                             rule={'path': 'scopes.users.actions', 'op': 'in', 'value': 'w'},
                             allow_super=True)
    assert pv.verify(ut) is True


def test_admin_cannot_do_anything_if_is_not_allow():
    scopes = {
        'users': {
            'actions': ['w', 'r', 'd', 'u']
        }
    }
    ut = UserToken(username='crl', email='', photo_url='',
                   app_meta={}, user_meta={}, admin=True, staff=False, scopes=scopes).to_dict()

    pv = PermissionInspector(user={'req': 'staff'},
                             rule={'path': 'scopes.users.actions', 'op': 'in', 'value': 'w'},
                             allow_super=False)
    assert pv.verify(ut) is False


def test_staff_need_permissions():
    ut = UserToken(username='crl', email='', photo_url='',
                   app_meta={}, user_meta={}, admin=False, staff=True, scopes={}).to_dict()
    pv = PermissionInspector(user={'req': 'staff'},
                             rule={'path': 'scopes.users.actions', 'op': 'in', 'value': 'w'},
                             allow_super=False)
    assert pv.verify(ut) is False


def test_staff_have_permissions():
    ut = UserToken(username='crl', email='', photo_url='',
                   app_meta={}, user_meta={}, admin=False, staff=True,
                   scopes={'users': {'actions': ['w']}}).to_dict()

    pv = PermissionInspector(user={'req': 'staff'},
                             rule={'path': 'scopes.users.actions', 'op': 'in', 'value': 'w'},
                             allow_super=False)
    assert pv.verify(ut) is True


def test_even_admin_needs_scopes_if_allow_super_is_false():
    ut = UserToken(username='crl', email='', photo_url='',
                   app_meta={}, user_meta={}, admin=True, staff=True,
                   scopes={'users': {'actions': ['w']}}).to_dict()

    pv = PermissionInspector(user={'req': 'staff'},
                             rule={'path': 'scopes.users.actions', 'op': 'in', 'value': 'w'},
                             allow_super=False)
    assert pv.verify(ut) is False


def test_only_match_allow_admin():
    ut = UserToken(username='crl', email='', photo_url='',
                   app_meta={}, user_meta={}, admin=True, staff=True,
                   scopes={'users': {'actions': ['w']}}).to_dict()

    pv = PermissionInspector(user={'req': 'staff', 'match': 'min'},
                             rule={'path': 'scopes.users.actions', 'op': 'in', 'value': 'w'},
                             allow_super=False)
    assert pv.verify(ut) is False


def test_get_permissions_admin():
    ut = UserToken(username='crl', email='', admin=True, staff=True, special=1).to_dict()
    pv = PermissionInspector()

    assert pv.get_user_type(ut) == 'admin'


def test_get_permissions_staff():
    ut = UserToken(username='crl', email='', admin=False, staff=True, special=1).to_dict()
    pv = PermissionInspector()

    assert pv.get_user_type(ut) == 'staff'


def test_get_permissions_special():
    ut = UserToken(username='crl', email='', admin=False, staff=False, special=1).to_dict()
    pv = PermissionInspector()

    assert pv.get_user_type(ut) == 1


def test_get_permissions_user():
    ut = UserToken(username='crl', email='', admin=False, staff=False, special=0).to_dict()
    pv = PermissionInspector()

    assert pv.get_user_type(ut) == 'user'


def test_get_permissions_user_2():
    ut = UserToken(username='crl', email='', admin=False, staff=False, special='').to_dict()
    pv = PermissionInspector()

    assert pv.get_user_type(ut) == 'user'
