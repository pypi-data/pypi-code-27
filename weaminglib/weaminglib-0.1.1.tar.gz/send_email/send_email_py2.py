# coding: utf-8

import os
import json
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

EMAIL_CHARSET = 'UTF-8'


def send_email(client,
               from_addr,
               to_addr,
               subject,
               text=None,
               html=None,
               cc=None,
               bcc=None,
               attachments=None,
               client_type='smtp'):
    print('send mail, from: %s, to: %s, subject: %s' % (from_addr, to_addr,
                                                        subject))
    print('send mail, text: %s...' % (text or html)[:20])
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    if cc:
        msg['CC'] = cc
    if bcc:
        msg['BCC'] = bcc

    if text is not None:
        msg.preamble = text + '\n'
        msg.attach(MIMEText(text, _charset=EMAIL_CHARSET))

    if html is not None:
        msg.preamble = html + '\n'
        msg.attach(MIMEText(html, 'html', _charset=EMAIL_CHARSET))

    if attachments:
        if not isinstance(attachments, [list, tuple]):
            attachments = [attachments]

        for attachment in attachments:
            if attachment is not None:
                with open(attachment, 'rb') as f:
                    part = MIMEApplication(f.read())
                part.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(attachment))
                part.add_header('Content-Type',
                                'application/pdf; charset=UTF-8')
                msg.attach(part)

    if client_type == 'aws_ses':
        print('sending using aws_ses')
        return aws_ses_send_raw_mail(client, msg)
    if client_type == 'smtp':
        print('sending using normal stmp')
        return smtp_send_mail(client, msg)


def gen_receiver_str(contacts_list):
    return ', '.join(contacts_list)


def new_smtp_client(smtp_server, port, userid=None, passwd=None):
    smtp = smtplib.SMTP_SSL(smtp_server, port)
    smtp.ehlo()
    if userid and passwd:
        smtp.login(userid, passwd)
    return smtp


def smtp_send_mail(smtp, msg):
    try:
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())
        smtp.close()
        return 'success'
    except Exception as e:
        return str(e)


def aws_ses_send_raw_mail(client, msg):
    r = client.send_raw_email(
        RawMessage={
            'Data': msg.as_string(),
        }, )
    return r


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def test():
    import sys

    html = "<h2> Hello weaming </h2> <small> Best, </small>"
    smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
    smtp_ssl_port = 465
    username = 'garden.yuen'  # USERNAME or EMAIL ADDRESS
    password = '' or sys.argv[1]

    from_addr = 'weaming <garden.yuen@gmail.com>'
    to_addr = 'bitworld@live.com'
    bcc = 'iweaming@gmail.com'

    client = new_smtp_client(smtp_ssl_host, smtp_ssl_port, username, password)
    res = send_email(
        client, from_addr, to_addr, 'Hello from python2', html=html, bcc=bcc)
    print(res)


if __name__ == '__main__':
    test()
