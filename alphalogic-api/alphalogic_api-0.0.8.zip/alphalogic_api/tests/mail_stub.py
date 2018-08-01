# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from operator import methodcaller

from alphalogic_api import options
from alphalogic_api.objects import Root, Device
from alphalogic_api.attributes import Visible, Access
from alphalogic_api.objects import ParameterBool, ParameterInt, ParameterDouble, ParameterDatetime, ParameterString
from alphalogic_api.decorators import command, run
from alphalogic_api.logger import log


#
# How to send an email with Python
# http://naelshiab.com/tutorial-send-email-python/
#
def send_mail(smtp, message, topic, recipients):
    host = smtp.ServerAddress.val
    port = smtp.Port.val
    user = smtp.Login.val
    password = smtp.Password.val
    timeout = smtp.TimeoutMillisec.val / 1000.0  # in seconds
    from_addr = smtp.SenderAddress.val
    to_addrs = map(methodcaller('strip'), recipients.split(','))  # 'mike@mail.com, tom@mail.com'

    msg = MIMEMultipart()
    msg['From'] = smtp.SenderName.val
    msg['To'] = recipients
    msg['Subject'] = topic

    body = message
    charset = dict(Smtp.ENCODING_CHOICES)[smtp.Encoding.val]
    msg.attach(MIMEText(body, 'plain', charset))

    server = smtplib.SMTP(host=host, port=port, timeout=timeout)
    server.starttls()
    server.login(user=user, password=password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addrs, text)
    server.quit()
    return ''

#
# Adapter Stub. 
# Tree:
# MailAdapter
#     |
#     |__Smtp
#     |    |__MailMessage
#     |
#     |__Profile
#
class MailAdapter(Root):
    
    def handle_get_available_children(self):
        return [
            (Smtp, 'Smtp'),
            (Profile, 'Profile'),
        ]

class Smtp(Device):

    PORT_CHOICES = (
        (25, '25'),
        (465, '465'),
        (587, '587'),
        (2525, '2525'),
    )

    ENCODING_CHOICES = (
        (0, 'utf-8'),
        (1, 'koi8-r'),
        (2, 'windows-1251'),
        (3, 'windows-1252'),
    )

    # parameters
    ServerAddress = ParameterString(visible=Visible.setup)
    SenderAddress = ParameterString(visible=Visible.setup)
    Login = ParameterString(visible=Visible.setup)
    Password = ParameterString(visible=Visible.setup)
    SenderName = ParameterString(visible=Visible.setup)
    Port = ParameterInt(visible=Visible.setup, choices=PORT_CHOICES, default=587)
    TimeoutMillisec = ParameterInt(visible=Visible.common, default=5000)
    Encoding = ParameterInt(visible=Visible.common, choices=ENCODING_CHOICES, default=0)

    # commands
    @command(result_type=unicode)
    def SendMail(self, message='', topic='', recipients=''):
        return send_mail(self, message=message, topic=topic, recipients=recipients)

    def handle_get_available_children(self):
        return [
            (MailMessage, 'MailMessage'),
        ]


def update_topic(node, parameter):
    node.Topic.val = node.TopicTemplate.val


def update_recipients(node, parameter):
    node.Recipients.val = node.RecipientsTemplate.val


class MailMessage(Device):

    # parameters
    TopicTemplate = ParameterString(visible=Visible.common, choices=(('', ''),), callback=update_topic)
    Topic = ParameterString(visible=Visible.common)
    RecipientsTemplate = ParameterString(visible=Visible.common, choices=(('', ''),), callback=update_recipients)
    Recipients = ParameterString(visible=Visible.common)
    Message = ParameterString(visible=Visible.common)

    # commands
    @command(result_type=unicode)
    def SendMail(self):
        return send_mail(self, message=self.Message.val, topic=self.Topic.val, recipients=self.Recipients.val)

    def update(self, topic_enums, recipients_enums):
        self.TopicTemplate.clear()
        self.TopicTemplate.set_enums(topic_enums)
        self.RecipientsTemplate.clear()
        self.RecipientsTemplate.set_enums(recipients_enums)


def update_templates(node, parameter):
    is_profile = lambda x: isinstance(x, Profile)
    is_smtp = lambda x: isinstance(x, Smtp)
    is_mail_message = lambda x: isinstance(x, MailMessage)

    profile_nodes = filter(is_profile, node.root().children())
    smpt_nodes = filter(is_smtp, node.root().children())
    mail_message_nodes = reduce(lambda acc, smtp: acc + filter(is_mail_message, smtp.children()), smpt_nodes, [])

    if parameter is None:
        profile_nodes = filter(lambda x: x.id != node.id, profile_nodes)

    # create new enums
    topic_enums = [('', '')]
    recipients_enums = [('', '')]
    for x in profile_nodes:
        topic_enums.append((x.Topic.val, x.Topic.val))
        recipients_enums.append((x.Recipients.val, x.Recipients.val))

    # set new enums
    for x in mail_message_nodes:
        x.update(topic_enums=topic_enums, recipients_enums=recipients_enums)


class Profile(Device):

    # parameters
    Topic = ParameterString(visible=Visible.common, callback=update_templates)
    Recipients = ParameterString(visible=Visible.common, callback=update_templates)

    def handle_before_remove_device(self):
        update_templates(self, None)


if __name__ == '__main__':
    # main loop
    root = MailAdapter(options.host, options.port)
    root.join()