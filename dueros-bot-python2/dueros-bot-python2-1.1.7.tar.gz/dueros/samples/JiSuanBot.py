#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/7/19

"""
    desc:pass
"""
from dueros.Bot import Bot
from dueros.card.TextCard import TextCard
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from dueros.directive.Display.template.TextContentPosition import TextContentPosition
class JiSuanBot(Bot):

    def __init__(self, request_data):
        super(JiSuanBot, self).__init__(request_data)
        self.add_launch_handler(self.launch_request)

    def launch_request(self):
        self.wait_answer()

        card = TextCard('欢迎使用')
        body_template1 = BodyTemplate1()
        body_template1.set_plaintext_content('aaaa', TextContentPosition.TOP_LEFT)
        body_template1.set_background_image('https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=3076902991,1977352976&fm=173&app=25&f=JPEG?w=550&h=314&s=83901CC7047293D448C9F4A20300E041')
        directive = RenderTemplate(body_template1)

        self.ask('aaa')
        return {
            'card': card,
            'directives': [directive],
            'outputSpeech': '欢迎使用'
        }


if __name__ == '__main__':

    pass