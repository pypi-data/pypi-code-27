#!/usr/bin/python3
# encoding: utf-8
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib


host = "smtp.163.com"  # smtp服务器

postfix = "163.com"  # 后缀


class mail():

    def __init__(self, to_list, user, password):
        self.to_list = to_list
        self.user = user
        self.password = password

    def send_mail(self, sub, content):
        print('start send mail')
        me = self.user + "@" + postfix
        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(self.to_list)
        try:
            server = smtplib.SMTP()
            server.connect(host)
            server.login(self.user, self.password)
            server.sendmail(me, self.to_list, msg.as_string())
            server.close()
            return True
        except Exception as e:
            print(e)
            return False

    def send_mail_attach(self, sub, content, name):
        print('start send mail')

        msg = MIMEMultipart()
        file = name + '.xls'
        me = "朋友" + "<" + self.user + "@" + postfix + ">"
        msg.attach(MIMEText(content, _subtype='plain', _charset='utf-8'))
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(self.to_list)
        xlsxpart = MIMEApplication(open(file, 'rb').read())
        xlsxpart.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(xlsxpart)
        try:
            server = smtplib.SMTP()
            server.connect(host)
            server.login(self.user, self.password)
            server.sendmail(me, self.to_list, msg.as_string())
            server.close()
            os.remove(file)  # Delete file
            return True
        except Exception as e:
            print(e)
            return False

if __name__ == "__main__":

    test = mail()
    #     test.send_mail('aloha', 'hello')
#     test.send_mail_attach('aloha', '中文撒旦撒旦', 'item')
