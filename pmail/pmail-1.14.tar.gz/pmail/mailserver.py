# Mail server configuration
class MailServer:
    def __init__(self, data={}):
        self.host = data.get("host")
        self.port = data.get("port")
        self.login = data.get("login")
        self.password = data.get("password")
        self.security = data.get("security")

    # Returns true if server configuration is valid and can be used for sending messages
    def isvalid(self):
        return self.host and \
               self.port and \
               self.security and \
               self.security in ["none", "ssl", "tls"]

    # Returns server configuration as serializable dictionary
    def todict(self):
        return {
            "host": self.host,
            "port": self.port,
            "login": self.login,
            "password": self.password,
            "security": self.security
        }

    # Creates server configuration from dictionary
    @staticmethod
    def fromdict(data):
        if data:
            return MailServer(data)


