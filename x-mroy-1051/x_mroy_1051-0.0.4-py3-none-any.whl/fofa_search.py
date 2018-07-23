import pickle, json, os, re
from qlib.data import Cache
from termcolor import colored

from FlowWork.Net.flownet import  FLowNet
from bs4 import BeautifulSoup as BS
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .data import Info
from .log import lprint, rprint, gprint
from .setting import DB_FOFA, LOGIN_INFO_SESSION, LOGIN_INFO

import getpass
import argparse
import sys



class Fofa:

    def __init__(self, proxy=False):
        self.main_url = "https://fofa.so"
        self.flow = FLowNet("https://fofa.so", proxy=proxy)
        self.waiter = WebDriverWait(self.flow.phantom, 12)
        self.LOGIN_INFO =  LOGIN_INFO
        self.LOGIN_INFO_SESSION = LOGIN_INFO_SESSION
        self.DB_Handle = Cache(DB_FOFA)
        

    def selector(self, x, time=0):
        try:
            r =  self.waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, x)))
            if r:
                return r
        except TimeoutException as e:
            if isinstance(time, int) and time > 3:
                rprint("not found : %s , you can see error page in " % x + colored("/tmp/TimeoutException.png ",'red') )
                
                self.flow.screenshot("TimeoutException")
                with open("/tmp/TimeoutException.html", "w") as fp:
                    fp.write(self.flow.html())
                # raise TimeoutException("time out not found : %s" %x)
                sys.exit(0)
            return self.selector(x, time+1)

    def load_session_login(self):
        if os.path.exists(self.LOGIN_INFO_SESSION):
            self.load_session()
        else:
            self.login()

    def login(self, u=None):
        user = None
        passwd = None
        
        if not u:
            if os.path.exists(self.LOGIN_INFO):
                with open(LOGIN_INFO) as fp:
                    u = json.load(fp)

                    user = u['username']
                    passwd = u['password']
            else:
                user = input("email>")
                passwd = getpass.getpass("passwd>")
        else:
            user = u['username']
            passwd = u['password']

        
        gprint("try login")
        
        #selector = lambda x: waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, x)))

        to_login = self.selector("a#but_zc")
        self.flow.screenshot('login')
        to_login.click()
        
        input_user = self.selector('#username')
        input_pass = self.selector('#password')

        input_user.send_keys(user)
        input_pass.send_keys(passwd+"\n")
        gprint(" --- Login ---")
        # with open(LOGIN_INFO_SESSION, 'w') as fp:

        u = {'username':user, 'password':passwd}
        with open(self.LOGIN_INFO, 'w') as fp:
            json.dump(u,fp)

        self.save_session()
        return user,passwd

    def save_session(self):
        gprint(" save session cookies")
        with open(self.LOGIN_INFO_SESSION, 'wb') as fp:
            pickle.dump(self.flow.phantom.get_cookies() , fp)

    def load_session(self):
        gprint(" load cookies from")
        cookies = pickle.load(open(self.LOGIN_INFO_SESSION, "rb"))
        self.flow.go(self.main_url)
        for cookie in cookies:
            gprint(str(cookie))
            self.flow.phantom.add_cookie(cookie)
            
    def search(self, key, page=0):
        search_input = self.selector("input#q")
        search_input.send_keys("{}\n".format(key))
        self.flow.screenshot("mod")
        check_if_found = self.selector(".list_jg")
        check_if_found = check_if_found.get_attribute('outerHTML')
        try:
            num = re.findall(r'Total\ results:\s(\d+)', check_if_found)[0]
            gprint("found result in :%s = %s" % (key, num ))
            if int(num) == 0:
                return
        except IndexError:
            self.flow.screenshot("error.png")
            rprint("page load error !! see /tmp/error.png ")
            return
        self.selector(".list_mod")
        res = self.flow.html()
        self.parse(res)
        gprint(" page 1")
        if page and isinstance(page, int):
            for i in range(page):
                next_page = self.selector("a.next_page")
                next_page.click()
                self.selector(".list_mod")
                res = self.flow.html()
                gprint(" page " + str(i+2))
                self.parse(res)



    def parse(self, res):
        mods = BS(res, 'html.parser').select('.list_mod')
        infos = []

        c = 0
        for m in mods:
            c += 1
            ports = '/'.join([i.text for i in  m.select('.list_mod_t > .span > span')]).replace("\n","").replace(" ","")
            pa = m.select(".list_sx1 > li")
            ti = pa[0].text.replace('\n', '').replace(' ','')
            ip = pa[1].text.replace('\n', '').replace(' ','')
            time = pa[2].text.replace('\n', '').replace(' ','')
            geo = pa[3].text.replace('\n', '').replace(' ','')
            try:
                os = pa[5].text.replace('\n', '').replace(' ','')
            except IndexError:
                os = 'Unknow'
                rprint(str(pa))
            body = m.select('.auto-wrap')[0]
            if len(list(body)) > 1:
                body = ''.join([i.__str__() for i in list(body)])
            else:
                body = body.text

            lprint(title=ti,ip=ip,ports=ports,os=os,time=time,geo=geo,body=body)
            info = Info(title=ti,ip=ip,ports=ports,os=os,ctime=time,geo=geo,body=body)
            infos.append(info)

        iis = []
        for i in infos:
            # if not self.DB_Handle.query_one(Info, ip=ip,ports=ports, ctime=time):
               iis.append(i)
        self.DB_Handle.save_all(*iis) 

