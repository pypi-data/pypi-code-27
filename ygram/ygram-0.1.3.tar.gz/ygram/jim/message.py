from jim.config import *
import abc
import time

class Message(abc.ABC):

    def __init__(self, action):
        self.ACTION = action
        self.TIME = time.time()

    @abc.abstractmethod
    def to_dict(self):
        pass


class PresenceMessage(Message):

    def __init__(self, account_name):
        super().__init__(PRESENCE)
        self.ACCOUNT_NAME = account_name
        self.message = self.to_dict()

    def to_dict(self):
        message = {
            ACTION: self.ACTION,
            TIME: self.TIME,
            USER: {
                ACCOUNT_NAME: self.ACCOUNT_NAME
            }
        }
        return message

class TextMessage(Message):

    def __init__(self, addressee, text, account_name):
        super().__init__(MSG)
        self.TO = addressee
        self.MESSAGE = text
        self.ACCOUNT_NAME =  account_name
        self.message = self.to_dict()

    def to_dict(self):
        message = {
            ACTION: self.ACTION,
            TIME: self.TIME,
            TO: self.TO,
            FROM: self.ACCOUNT_NAME,
            MESSAGE: self.MESSAGE
        }
        return message

class AddContactMessage(Message):

    def __init__(self, contact, account_name):
        super().__init__(ADD_CONTACT)
        self.CONTACT = contact
        self.ACCOUNT_NAME = account_name
        self.message = self.to_dict()

    def to_dict(self):
        message = {
            ACTION: self.ACTION,
            TIME: self.TIME,
            CONTACT: self.CONTACT,
            ACCOUNT_NAME: self.ACCOUNT_NAME,
        }
        return message

class AddUserMessage(Message):

    def __init__(self, account_name, password, address, custom_profile_image):
        super().__init__(ADD_USER)
        self.ACCOUNT_NAME = account_name
        self.PASSWORD = password
        self.ADDR = address
        self.IMAGE = custom_profile_image
        self.message = self.to_dict()

    def to_dict(self):
        message = {
            ACTION: self.ACTION,
            TIME: self.TIME,
            ACCOUNT_NAME: self.ACCOUNT_NAME,
            PASSWORD: self.PASSWORD,
            IMAGE: str(self.IMAGE),
            ADDR: self.ADDR
        }
        return message

class CheckLoginMessage(Message):

    def __init__(self, account_name, password, address):
        super().__init__(CHECK)
        self.ACCOUNT_NAME = account_name
        self.PASSWORD = password
        self.ADDR = address
        self.message = self.to_dict()

    def to_dict(self):
        message = {
            ACTION: self.ACTION,
            TIME: self.TIME,
            ACCOUNT_NAME: self.ACCOUNT_NAME,
            PASSWORD: self.PASSWORD,
            ADDR: self.ADDR
        }
        return message

class DeleteContactMessage(Message):

    def __init__(self, contact, account_name):
        super().__init__(DEL_CONTACT)
        self.CONTACT = contact
        self.ACCOUNT_NAME = account_name
        self.message = self.to_dict()

    def to_dict(self):
        message = {
            ACTION: self.ACTION,
            TIME: self.TIME,
            CONTACT: self.CONTACT,
            ACCOUNT_NAME: self.ACCOUNT_NAME,
        }
        return message

class ListContactsMessage(Message):

    def __init__(self, account_name):
        super().__init__(LIST_CONTACTS)
        self.ACCOUNT_NAME = account_name
        self.message = self.to_dict()

    def to_dict(self):
        message = {
            ACTION: self.ACTION,
            TIME: self.TIME,
            ACCOUNT_NAME: self.ACCOUNT_NAME,
        }
        return message

class ListContactsResponseMessage(Message):

    def __init__(self, account_name, contacts):
        super().__init__(LIST_CONTACTS)
        self.ACCOUNT_NAME = account_name
        self.CONTACTS = contacts
        self.message = self.to_dict()

    def to_dict(self):
        message = {
            ACTION: self.ACTION,
            TIME: self.TIME,
            ACCOUNT_NAME: self.ACCOUNT_NAME,
            CONTACTS: self.CONTACTS
        }
        return message

if __name__ == '__main__':
    pass
