import json
import os
import keyring
from pmail.mailserver import MailServer
from pmail.recipient import Recipient
from pmail.screen import Screen
from pmail.text import Text


# Application configuration
class Configuration:
    KEYRING_SERVICE_NAME = "agilisconsultinglimited_pmail"
    CONFIDENTIAL_PASSWORD = "**********"

    def __init__(self):
        self.name = "pmail"
        self.server = MailServer()
        self.sender = Recipient()
        self.contacts = []
        self.configurationfile = os.path.expanduser("~/.pmail/configuration.json")
        self.load()

    # Returns true if configuration is complete and valid
    def isvalid(self):
        return self.server and \
               self.server.isvalid() and \
               self.sender and \
               self.sender.isvalid()

    # Converts configuration to dictionary
    def todict(self, confidential=True):
        data = {
            "name": self.name,
            "server": self.server.todict(),
            "sender": self.sender.todict(),
            "contacts": [contact.todict() for contact in self.contacts]
        }
        data["server"]["login"] = data["server"].get("login")
        if confidential:
            data["server"]["password"] = Configuration.CONFIDENTIAL_PASSWORD
        else:
            data["server"]["password"] = data["server"].get("password")
        return data

    # Saves the configuration to JSON file
    # Vulnerable data is stored in system keyring
    def save(self):
        path = os.path.dirname(self.configurationfile)
        if not os.path.isdir(path):
            os.mkdir(path)
        data = self.todict()
        with open(self.configurationfile, mode="w") as file:
            file.write(json.dumps(data, indent=2))
        keyring.set_password(Configuration.KEYRING_SERVICE_NAME, self.server.login, self.server.password)

    # Loads the configuration from JSON file
    def load(self):
        if os.path.isfile(self.configurationfile):
            with open(self.configurationfile, mode="r") as file:
                data = json.loads(file.read())
                if data:
                    self.name = data.get("name", self.name)
                    self.server = MailServer.fromdict(data.get("server"))
                    self.sender = Recipient.fromdict(data.get("sender"))
                    self.contacts = [Recipient.fromdict(contact) for contact in data.get("contacts", [])]
                    self.server.login = self.server.login
                    self.server.password = self.server.password
                    if self.server.password == Configuration.CONFIDENTIAL_PASSWORD:
                        self.server.password = keyring.get_password(Configuration.KEYRING_SERVICE_NAME, self.server.login)

    # Asks the user to enter the configuration
    def collect(self):
        choice = "y"
        if self.isvalid():
            Screen.print("Current configuration:")
            Screen.print()
            Screen.print("    SMTP host: {}".format(self.server.host))
            Screen.print("    SMTP port: {}".format(self.server.port))
            Screen.print("    Login: {}".format(self.server.login))
            Screen.print("    Password: {}".format(self.server.password))
            Screen.print("    Security: {}".format(self.server.security.upper()))
            Screen.print("    Sender name: {}".format(self.sender.name))
            Screen.print("    Sender address: {}".format(self.sender.address))
            Screen.print()
            choice = Screen.input("Do you want to change it? (Y/N): ", ["y", "n"]).lower()
            Screen.print()
        else:
            Screen.print("Please enter configuration:")
            Screen.print()

        if choice == "y":
            self.server = MailServer()
            self.sender = Recipient()
            self.server.host = Screen.input("    SMTP host: ").strip()
            self.server.port = Screen.inputnumber("    SMTP port: ")
            self.server.login = Screen.input("    Login: ").strip()
            self.server.password = Screen.input("    Password: ").strip()
            self.server.security = Screen.input("    Security (none|ssl|tls): ").lower().strip()
            self.sender.name = Screen.input("    Sender name: ").strip()
            self.sender.address = Screen.input("    Sender address: ").strip()
            Screen.print()
            if self.isvalid():
                self.save()
                Screen.print("Configuration saved to {}, thank you!".format(self.configurationfile))
            else:
                Screen.print("Invalid configuration, please try again.")
            return True

    # Asks the user to edit contacts in the address book
    def editcontacts(self):
        finish = False
        while not finish:
            if self.contacts:
                Screen.print("Contacts currently in your address book:")
                Screen.print()
                i = 1
                for contact in self.contacts:
                    Screen.print("    {}. {}: {}".format(i, contact.name, contact.address))
                    i += 1
                Screen.print()
                Screen.print("Enter 'd' followed by contact number to delete it.")
            else:
                Screen.print("There are no contacts yet in your address book, let's add some:")
                Screen.print()
            Screen.print("Enter 'n' to add new contact.")
            Screen.print("Press ENTER to leave.")
            Screen.print()
            choice = Screen.input("Your choice: ").lower()
            Screen.print()
            command = choice[0] if choice else "exit"
            argument = choice[1:].strip() if choice else ""
            if command == "n":
                self.addcontact()
            elif command == "d" and argument:
                self.removecontact(argument)
            finish = command == "exit"
            if not finish:
                Screen.clear()
        self.save()

    # Asks the user to add contact the address book
    def addcontact(self):
        Screen.print("Add new contact:")
        Screen.print()
        contact = Recipient()
        contact.name = Screen.input("    Name: ")
        contact.address = Screen.input("   E-mail: ")
        if contact.isvalid():
            self.contacts.append(contact)

    # Removes a contact from the address book
    def removecontact(self, index):
        try:
            index = int(index) - 1
            if 0 <= index < len(self.contacts):
                del self.contacts[index]
        except:
            Screen.print("Invalid index {}".format(index))

