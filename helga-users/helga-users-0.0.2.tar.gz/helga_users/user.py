class User(object):
    def __init__(self, uid, client):
        """
        A user account

        :param uid: kerberos uid str like "kdreyer"
        :param client: LDAPClient
        """
        self.uid = uid
        self.client = client
        # Set these dynamically later:
        self.nick = None
        self.location = None

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.uid)
