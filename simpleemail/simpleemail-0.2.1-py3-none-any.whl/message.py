import mimetypes
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email import encoders


def attach_file(file_to_send: str):
    ctype, encoding = mimetypes.guess_type(file_to_send)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    with open(file_to_send, "rb") as fp:
        if maintype == "text":
            attachment = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == "image":
            attachment = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == "audio":
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=file_to_send)

    return attachment


def create_email_message(subject: str, sender: str, recipient: str, text: str, html: str,
                         params: dict = dict(), fileToSend: str = ""):
    """
    Sends an email using both an html and text version.\n
    Based originally on example from: https://docs.python.org/3/library/email-examples.html
    :param subject: Subject of the email.
    :param sender: Email address to send from.
    :param recipient: Email address to send to.
    :param text: Text version of the email.
    :param html: HTML version of the email.
    :param params: dictionary of items to replace in the message body, using square brackets.\n
                    \t Example: "[firstname]" would be replaced by "John"
    :return: Email message to send through SMTP.
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    html, text = merge_params(html, text, params)
    part1 = ''
    part2 = ''
    if text:
        part1 = MIMEText(text, 'plain')
    if html:
        part2 = MIMEText(html, 'html')

    if part1:
        msg.attach(part1)
    if part2:
        msg.attach(part2)

    if fileToSend:
        msg.attach(attach_file(fileToSend))
        
    return msg


def merge_params(html, text, params):
    for key in params.keys():
        text = text.replace('[{}]'.format(key), params[key])
        html = html.replace('[{}]'.format(key), params[key])

    return html, text

