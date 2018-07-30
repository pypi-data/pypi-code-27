# Mail recipient
class Recipient:
    # Initializes a recipient
    #     address: email address
    #     name: user-friendly name
    def __init__(self, address=None, name=None):
        self.address = address
        self.name = name

    # Returns true if recipient is valid and can be used for sending messages
    def isvalid(self):
        return self.address and Recipient.isemail(self.address)

    # Text representation of the recipient
    def text(self):
        if self.isvalid():
            return "{} <{}>".format(self.name, self.address) if self.name else self.address

    # Returns recipient as dictionary
    def todict(self):
        return {
            "name": self.name,
            "address": self.address
        }

    # Creates recipient from dictionary
    @staticmethod
    def fromdict(data):
        if data:
            return Recipient(data.get("address"), data.get("name"))

    # Returns text representation of the sender
    def text(self):
        if self.isvalid():
            name = self.name or self.createname(self.address)
            return "{} <{}>".format(name, self.address)

    # Checks whether input is a valid email address
    @staticmethod
    def isemail(text):
        return text and len(text.split("@")) == 2 and "." in text.split("@")[1]

    # Tries to create recipient name from provided email address
    @staticmethod
    def createname(address):
        if Recipient.isemail(address):
            name = address.split("@")[0].replace(".", " ").replace("_", " ").replace("-", " ").title()
            return name

    # Creates a list of recipients from the provided e-mail addresses.
    # Addresses are separated with ;
    # Tries to match found addresses against the specified contacts,
    # in order to resolve user-friendly recipient names
    @staticmethod
    def fromstring(text, contacts, sender, separator=";"):
        recipients = []
        contacts = contacts or []
        for entry in [e.strip() for e in (text or "").split(separator)]:
            recipient = Recipient.resolve(entry, contacts, sender)
            if recipient and recipient.isvalid():
                recipients.append(recipient)
        return recipients

    # Resolves recipient specified by name or email
    @staticmethod
    def resolve(text, contacts, sender):
        if text:
            text = text.strip()
            if Recipient.isemail(text):
                found = [c for c in contacts if (c.address or "").lower() == text]
            else:
                found = [c for c in contacts if (c.name or "").lower() == text]
                if not found and text.lower() in ["me", "self"] and sender:
                    found = [sender]
            recipient = found[0] if found else Recipient(text, Recipient.createname(text))
            return recipient
