#!/usr/bin/python3
# encoding: utf-8
import os
import pickle
import random
import shutil
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


cookie_dict = {}
url_login = 'https://i.dmzj.com/login'


class cookie(object):

    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd

    def get_cookie_dmzj(self):
        '''
        TODO 获取excel宝贝信息 保存本地cookie
        '''
        if ':' in self.username:
            dirname = self.username[:self.username.index(':')]
        else:
            dirname = self.username

        if os.path.isfile(dirname):  # Delete file
            os.remove(dirname)
        elif os.path.isdir(dirname):  # Delete dir
            shutil.rmtree(dirname, True)
        os.makedirs(dirname)

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36")

        driver = webdriver.PhantomJS(desired_capabilities=dcap)

    #         options = webdriver.ChromeOptions()
    #         prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.shopdir}
    #         options.add_experimental_option('prefs', prefs)
    #         driver = webdriver.Chrome(chrome_options=options)
        driver.implicitly_wait(20)

        driver.get(url_login)
        # 登录
        driver.find_element_by_name('username').send_keys(self.username)
        driver.find_element_by_name('password').send_keys(self.pwd)
        time.sleep(1)

        driver.find_element_by_id('landBtn').click()
        time.sleep(random.randint(1, 3))

        # 获得 cookie信息
        cookie_list = driver.get_cookies()
        print(cookie_list)

        for cookie in cookie_list:
            f = open(dirname + '/' + cookie['name'] + '.dmzj', 'wb+')
            pickle.dump(cookie, f)
            f.close()
        driver.quit()

    def cache_dmzj(self):
        '''
        TODO 从本地文件夹获取cookie
        '''

    #         dirname = name[:name.index(':')]

        self.get_cookie_dmzj()

        o_cookie = []
        for parent, dirnames, filenames in os.walk('./' + self.username):
            for filename in filenames:
                if filename.endswith('.dmzj'):
                    with open(self.username + '/' + filename, 'rb') as f:
                        d = pickle.load(f)
                    if 'name' in d and 'value' in d:
                        cookie_dict[d['name']] = d['value']
                        o_cookie.append(d)
                    else:
                        return {}

        '''过期处理(dmzj的expires和expiry字段记录的是登录时间，情况不明)'''
    #             if 'name' in d and 'value' in d and 'expiry' in d:
    #                 expiry_date = int(d['expiry'])
    #                 if expiry_date > (int)(time.time()):
    #                     cookie_dict[d['name']] = d['value']
    #                 else:
    #                     return {}
        shutil.rmtree(self.username, True)
        return cookie_dict, o_cookie

if __name__ == '__main__':
    username = ''
    pwd = ''
    test = cookie(username, pwd)
    test.cache_dmzj()
