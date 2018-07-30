from pmail.attachment import Attachment
from pmail.recipient import Recipient


# Mail message
class Message:
    # Initializes mail message
    #    recipients: list of Recipient instances
    #    subject: subject text
    #    body: body text, can contain \n literals which will be replaced with linebreaks during message preparation
    #    attachments: list of Attachment instances
    def __init__(self, recipients=[], subject="", body="", attachments=[]):
        self.recipients = [recipient for recipient in recipients if recipient]
        self.subject = subject
        self.body = body
        self.attachments = [attachment for attachment in attachments if attachment]

    # Verifies whether the message is valid and can be sent
    def isvalid(self):
        return self.recipients and self.subject

    # Verifies whether the message is complete - has recipient, subject and message body
    def iscomplete(self):
        return self.isvalid() and self.body

    # Returns a list of message recipient addresses
    def recipientaddresses(self):
        if self.recipients:
            return [recipient.address for recipient in self.recipients]

    # Returns a list of message recipient names
    def recipientnames(self):
        if self.recipients:
            return [recipient.name if recipient.name else Recipient.createname(recipient.address) for recipient in self.recipients]

    # Returns a list of message attachments
    def attachmentnames(self):
        if self.attachments:
            return [attachment.name for attachment in self.attachments]

    # Returns a list of message recipient names and addresses
    # Returns a list of message recipient names and addresses
    def recipienttexts(self):
        if self.recipients:
            return [recipient.text() for recipient in self.recipients]

    # Creates a message from a list of command line arguments
    # Expected sequence of arguments: recipient(s), subject, body
    @staticmethod
    def fromargs(args, configuration):
        message = Message()
        if configuration and args:
            if len(args) >= 1:
                message.recipients = Recipient.fromstring(args[0], configuration.contacts, configuration.sender)
            if len(args) >= 2:
                message.subject = args[1]
            if len(args) >= 3:
                message.body = args[2]
            if len(args) >= 4:
                message.attachments = Attachment.fromstring(args[3])
        return Message(message.recipients, message.subject, message.body, message.attachments)
