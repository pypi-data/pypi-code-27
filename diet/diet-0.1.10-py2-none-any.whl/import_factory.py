from dash_import import user, user_org
from client_factory import ClientFactory


def get_importer(configuration=None):
    return {
        'users': user.User(ClientFactory(configuration)),
        'users-orgs': user_org.UserOrg(ClientFactory(configuration))
    }