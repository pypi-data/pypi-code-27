import user
import user_org
from ..client_factory import ClientFactory

class ImportFactory(object):

    def get_importer(self, target, configuration):
        if target == 'user':
            return user.User(ClientFactory(configuration))
        if target == 'user-org':
            return user_org.UserOrg(ClientFactory(configuration))
        else:
            return None