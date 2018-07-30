import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from pmail.message import Message


# Mail sender
class Sender:
    def __init__(self, configuration):
        self.configuration = configuration

    # Checks whether sender is ready to send e-mails
    def isvalid(self):
        return self.configuration and self.configuration.isvalid()

    # Sends mail message using the specified configuration
    def sendmail(self, message):
        if not self.isvalid():
            return "Invalid configuration"
        if not (message and message.isvalid()):
            return "Invalid message"

        result = ""
        try:
            server = smtplib.SMTP(self.configuration.server.host, self.configuration.server.port)
            if self.configuration.server.security == "tls":
                server.ehlo()
                server.starttls()
            if self.configuration.server.login:
                server.login(self.configuration.server.login, self.configuration.server.password)
            payload = self.createmessage(message)
            if payload:
                server.send_message(payload, self.configuration.sender.address, message.recipientaddresses())
                result = "ok"
            server.quit()
        except Exception as e:
            result = str(e)
        return result

    # Sends test message using the specified configuration
    def testmail(self):
        if self.isvalid():
            return self.sendmail(Message(
                                    [self.configuration.sender],
                                    "Test message from {}".format(self.configuration.name),
                                    "Yo, {} feels great today!".format(self.configuration.name)))
        else:
            return "Invalid configuration"

    # Creates the message to send
    def createmessage(self, data):
        if data:
            text = (data.body or "").replace("\\n", "\n")
            if data.attachments:
                message = MIMEMultipart()
                message.attach(MIMEText(text))
                for attachment in data.attachments:
                    part = attachment.createmessagepart()
                    if part:
                        message.attach(part)
            else:
                message = MIMEText(text)
            message["From"] = self.configuration.sender.text()
            message["To"] = ",".join(data.recipienttexts())
            message['Date'] = formatdate(localtime=True)
            message['Subject'] = data.subject
            return message
