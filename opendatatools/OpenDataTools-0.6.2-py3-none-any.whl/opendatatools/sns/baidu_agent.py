# coding=utf-8

from opendatatools.common import RestAgent

from functools import wraps
import re
import time
import json
import os
import logging
import pickle
import base64
from urllib import parse as urlparse
import requests
import rsa

class LoginFailed(Exception):
    """因为帐号原因引起的登录失败异常
    如果是超时则是返回Timeout的异常
    """
    pass

def check_login(func):
    """检查用户登录状态
    :param func: 需要被检查的函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if type(ret) == requests.Response:
            try:
                foo = json.loads(ret.content.decode('utf-8'))
                if 'errno' in foo and foo['errno'] == -6:
                    logging.debug(
                            'Offline, deleting cookies file then relogin.')
                    path = '.{0}.cookies'.format(args[0].username)
                    if os.path.exists(path):
                        os.remove(path)
                    args[0]._initiate()
            except:
                raise LoginFailed('User unsigned in.')
        return ret

    return wrapper

class BaiduAgent(RestAgent):

    # 某些情况下会遇到请求多次被拦截。增加全局codeString方便应对
    codeString = None
    BAIDUPAN_SERVER = 'index.baidu.com'
    api_template = 'http://%s/api/{0}' % BAIDUPAN_SERVER

    def __init__(self):
        RestAgent.__init__(self)
        self.username = ''
        self.password = ''
        self.user = {}
        self.captcha_func = self.default_captcha_handler
        self.verify_func = input

    def prepare_cookies(self, url):
        response = self.do_request(url, None)
        if response is not None:
            cookies = self.get_cookies()
            return cookies
        else:
            return None

    def default_captcha_handler(self, image_url):
        captcha_file = open("captcha.png", 'wb')
        data = self.do_request(image_url, type='binary')
        captcha_file.write(data)
        captcha_file.flush()
        captcha_file.close()

        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        pic = mpimg.imread('captcha.png')
        plt.imshow(pic)
        plt.show()

        verify_code = input('Input verify code > ')
        return verify_code

    def login(self, username, password):
        self.username = username
        self.password = password

        if not self._load_cookies():
            self.do_request('http://www.baidu.com')
            self.user['token'] = self._get_token()
            self._login()

    def _get_token(self):

        home_url = 'https://index.baidu.com/'
        cookies = self.prepare_cookies(home_url)

        # Token
        token_url = 'https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&class=login&tt=%s&logintype=dialogLogin&callback=0' % int(time.time())
        response = self.do_request(token_url, cookies=cookies)
        response = response.replace('\'', '\"')
        foo = json.loads(response)
        print('token %s' % foo['data']['token'])
        return foo['data']['token']

    def _save_cookies(self):
        cookies_file = '.{0}.cookies'.format(self.username)
        with open(cookies_file, 'wb') as f:
            pickle.dump(
                    requests.utils.dict_from_cookiejar(self.session.cookies), f)

    def _load_cookies(self):
        cookies_file = '.{0}.cookies'.format(self.username)
        logging.debug('cookies file:' + cookies_file)
        if os.path.exists(cookies_file):
            logging.debug('%s cookies file has already existed.' %
                          self.username)
            with open(cookies_file, 'rb') as cookies_file:
                cookies = requests.utils.cookiejar_from_dict(
                        pickle.load(cookies_file))
                logging.debug(str(cookies))
                self.session.cookies = cookies
                self.user['BDUSS'] = self.session.cookies['BDUSS']
                self.user['token'] = self._get_token()
                return True
        else:
            return False

    def _get_captcha(self, code_string):
        # Captcha
        if code_string:
            verify_code = self.captcha_func("https://passport.baidu.com/cgi-bin/genimage?" + code_string)
        else:
            verify_code = ""

        return verify_code

    def _get_publickey(self):
        url = 'https://passport.baidu.com/v2/getpublickey?token=' + self.user['token']
        content = self.do_request(url)
        jdata = json.loads(content.replace('\'', '"'))
        return jdata['pubkey'], jdata['key']

    def _login(self):
        # Login
        # code_string, captcha = self._get_captcha()
        captcha = ''
        code_string = ''
        pubkey, rsakey = self._get_publickey()
        key = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey)
        password_rsaed = base64.b64encode(rsa.encrypt(self.password.encode(), key))

        while True:
            login_data = {'staticpage': 'http://www.baidu.com/cache/user/html/v3Jump.html',
                          'charset': 'UTF-8',
                          'token': self.user['token'],
                          'tpl': 'nx',
                          'subpro': '',
                          'apiver': 'v3',
                          'tt': str(int(time.time())),
                          'codestring': code_string,
                          'isPhone': 'false',
                          'safeflg': '0',
                          'u': 'https://passport.baidu.com/',
                          'quick_user': '0',
                          'logLoginType': 'pc_loginBasic',
                          'loginmerge': 'true',
                          'logintype': 'basicLogin',
                          'username': self.username,
                          'password': password_rsaed,
                          'verifycode': captcha,
                          'mem_pass': 'on',
                          'rsakey': str(rsakey),
                          'crypttype': 12,
                          'ppui_logintime': '50918',
                          'callback': 'parent.bd__pcbs__oa36qm'}

            login_url = 'https://passport.baidu.com/v2/api/?login'
            result = self.do_request(login_url, param=login_data, method='POST')

            # 是否需要验证码
            if 'err_no=257' in result or 'err_no=6' in result:
                code_string = re.findall('codeString=(.*?)&', result)[0]
                self.codeString = code_string
                logging.debug('need captcha, codeString=' + code_string)
                captcha = self._get_captcha(code_string)
                continue

            break

        # check exception
        self._check_account_exception(result)

        if result is None:
            raise LoginFailed('Logging failed.')

        logging.info('COOKIES' + str(self.session.cookies))
        try:
            self.user['BDUSS'] = self.session.cookies['BDUSS']
        except:
            raise LoginFailed('Logging failed.')
        logging.info('user %s Logged in BDUSS: %s' %
                     (self.username, self.user['BDUSS']))

        self.user['token'] = self._get_token()
        self._save_cookies()

    def _check_account_exception(self, content):
        err_id = re.findall('err_no=([\d]+)', content)[0]

        if err_id == '0':
            return

        if err_id == '120021':
            # 如果用户需要外部认证(邮箱)
            auth_token = re.findall('authtoken=([^&]+)', content)[0]
            loginproxy_url = re.findall('loginproxy=([^&]+)', content)[0]
            verify_url = 'https://passport.baidu.com/v2/sapi/authwidgetverify'
            params = {'authtoken': urlparse.unquote(auth_token),
                      'type': 'email',
                      'apiver': 'v3',
                      'action': 'send',
                      'vcode': '',
                      'questionAndAnswer': '',
                      'needsid': '',
                      'rsakey': '',
                      'countrycode': '',
                      'subpro': '',
                      'callback': '',
                      'tpl': 'nx',
                      'u': 'https://www.baidu.com/'
                      }
            resp = self.do_request(verify_url, param=params, method='GET')

            if resp is not None:
                while 1:
                    # get vcode
                    vcode = input('Verification Code> ')
                    params = {'authtoken': urlparse.unquote(auth_token),
                              'type': 'email',
                              'apiver': 'v3',
                              'action': 'check',
                              'vcode': vcode,
                              'questionAndAnswer': '',
                              'needsid': '',
                              'rsakey': '',
                              'countrycode': '',
                              'subpro': '',
                              'callback': ''
                              }
                    vresp = self.do_request(verify_url)
                    vresp_data = json.loads(vresp)
                    if vresp_data['errno'] == 110000:
                        loginproxy_resp = self.session.get(urlparse.unquote(loginproxy_url))
                        err_id = re.findall('err_no=([\d]+)', loginproxy_resp)[0]
                        if err_id == '0':
                            return True
                        else:
                            raise LoginFailed("安全验证失败")

            else:
                raise LoginFailed("发送安全验证请求失败")

        error_message = {
            '-1': '系统错误, 请稍后重试',
            '1': '您输入的帐号格式不正确',
            '3': '验证码不存在或已过期,请重新输入',
            '4': '您输入的帐号或密码有误',
            '5': '请在弹出的窗口操作,或重新登录',
            '6': '验证码输入错误',
            '16': '您的帐号因安全问题已被限制登录',
            '257': '需要验证码',
            '100005': '系统错误, 请稍后重试',
            '120016': '未知错误 120016',
            '120019': '近期登录次数过多, 请先通过 passport.baidu.com 解除锁定',
            '120021': '登录失败,请在弹出的窗口操作,或重新登录',
            '500010': '登录过于频繁,请24小时后再试',
            '400031': '账号异常，请在当前网络环境下在百度网页端正常登录一次',
            '401007': '您的手机号关联了其他帐号，请选择登录'}
        try:
            msg = error_message[err_id]
        except KeyError:
            msg = 'unknown err_id=' + err_id
        raise LoginFailed(msg)

    def get_index(self, word):
        url = 'http://index.baidu.com/?tpl=trend&word=%s' % word
        response = self.do_request(url)
        return response

if __name__ == '__main__':
    agent = BaiduAgent()
    agent.set_proxies({'https':'https://127.0.0.1:1080'})
    agent.login('xxxxxxx', 'xxxxxx')
    response = agent.get_index('华谊兄弟')
    print(response)

