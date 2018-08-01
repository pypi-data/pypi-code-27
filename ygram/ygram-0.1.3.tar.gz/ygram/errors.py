class UserNameTooLong(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return 'User name should be no longer than 25 symbols'

class InvalidUserName(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return 'User name must have only letters, digits or underscores'


class ResponseCodeError(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return 'Invalid response code {}'.format(self.code)


class ResponseCodeLenError(ResponseCodeError):
    def __str__(self):
        return 'Invalid code length: {}. Code should be longer than 3 symbols.'.format(self.code)


class MandatoryKeyError(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return 'Lacks mandatory key {}'.format(self.key)
