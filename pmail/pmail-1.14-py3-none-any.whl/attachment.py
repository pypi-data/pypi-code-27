import os
from email.mime.base import MIMEBase
from email.encoders import encode_base64


# Mail attachment
class Attachment:
    # Initializes the attachment with specified file name
    # Path can be relative or absolute.
    def __init__(self, filename=None):
        self.filename = filename
        if self.filename:
            if self.filename[0] == "~":
                self.filename = os.path.expanduser(self.filename)
            elif not os.path.isabs(self.filename):
                self.filename = os.path.abspath(self.filename)
        self.name = os.path.basename(self.filename or "")

    # Returns true if attachment is valid (file exists)
    def isvalid(self):
        return self.filename and os.path.isfile(self.filename)

    # Creates MIME message part with the attachment data
    def createmessagepart(self):
        if self.isvalid():
            with open(self.filename, "rb") as file:
                data = file.read()
            if data:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(data)
                encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(self.filename)))
                return part

    # Creates a list of attachments from the specified file names
    @staticmethod
    def fromfilenames(filenames):
        return [Attachment(filename) for filename in filenames or [] if filename]

    # Creates a list of attachments from semicolon-separated file name list
    @staticmethod
    def fromstring(filenames, separator=";"):
        return [Attachment(filename) for filename in (filenames or "").split(separator) if filename]
