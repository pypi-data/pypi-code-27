import requests
import logging
import getpass
import base64
import sys
import os
import json
import pickle
import urllib.parse as up
from concurrent.futures import ThreadPoolExecutor
from qlib.data import Cache,dbobj
from bs4 import BeautifulSoup as BS
from termcolor import cprint, colored
import argparse
from FlowWork.Net.flownet import  FLowNet
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.ERROR)
sess = requests.Session()
flow = None
waiter = None
parmes = {}

sess.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})

LOGIN_INFO =  os.path.expanduser("~/.config/fofa.user")
LOGIN_INFO_SESSION = os.path.expanduser("~/.config/fofa.sess")
DB_FOFA = os.path.expanduser("~/.config/fofa.db")

DB_Handle = Cache(DB_FOFA)

global_res = []
class Info(dbobj):pass

def gprint(args, **kargs):
    cprint(colored("[+] ",'green') + args, **kargs)

def rprint(args, **kargs):
    cprint(colored("[!] ",'red') + args, **kargs)


def selector(x, time=0):

    r =  waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, x)))
    if r:
        return r
    else:
        if isinstance(time, int) and time > 3:
            rprint("not found : %s" %x)
            raise TimeoutException("time out not found : %s" %x)
            sys.exit(0)
        return selector(x, time+1)

def login2(u=None, proxy=False):
    global flow
    global waiter
    flow = FLowNet("https://fofa.so", proxy=proxy)
    waiter = WebDriverWait(flow.phantom, 12)
    if not u:
        user = input("email>")
        passwd = getpass.getpass("passwd>")
    else:
        user = u['username']
        passwd = u['password']

    
    gprint("try login")
    
    #selector = lambda x: waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, x)))

    to_login = selector("a#but_zc")
    flow.screenshot('aadebug')
    to_login.click()
    
    input_user = selector('#username')
    input_pass = selector('#password')

    input_user.send_keys(user)
    input_pass.send_keys(passwd+"\n")
    gprint(" --- Login ---")
    return user,passwd

def logout():
    r = sess.get("https://fofa.so/users/sign_out")
    if r.status_code == 200:
        rprint('logout')

def search2(page=None, searchstr=None):
    # TEM="""input#q/I'{search}'R
# [over]"""
    search_input = selector("input#q")
    search_input.send_keys("{}\n".format(searchstr))
    flow.screenshot("mod")
    selector(".list_mod")
    res = flow.html()
    parse2(res)
    gprint(" page 1")
    if page and isinstance(page, int):
        for i in range(page):
            next_page = selector("a.next_page")
            next_page.click()
            selector(".list_mod")
            res = flow.html()
            gprint(" page " + str(i+2))
            parse2(res)
    DB_Handle.save_all(*global_res)


def lprint(title='' ,ports='', ip='', time='', geo='', os='', body=''):
    C = lambda x,y : colored(' ' + x+ ' ', on_color='on_'+y)
    labels = [C(i, 'red') for i in title.split("|")]
    print(C(ip, 'blue'),
        C(ports, 'cyan'),
        C(time, 'blue'),
        C(os, 'green'),
        C(geo, 'yellow'),
        *labels,
        sep=colored("|",attrs=['blink','bold']))
    if '<hr/>' in body:
        for i,b in enumerate(body.split("<hr/>")):
            if i % 2== 0:
                cprint(b, 'green', attrs=['bold'])
            else:
                cprint(b, 'blue', attrs=['bold'])
    else:
        cprint(body, 'green')

def parse2(res):
    global global_res
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
        infos.append(Info(title=ti,ip=ip,ports=ports,os=os,ctime=time,geo=geo,body=body))
    global_res += infos
    cprint(" save : {} ".format(c), on_color='on_blue', end='\r')


def parse(res):
    global  global_res
    if res.status_code != 200:
        rprint(res.status_code)
        print(res.text)
        return
    mods = BS(res.text, 'html.parser').select('.list_mod')
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
        infos.append(Info(title=ti,ip=ip,ports=ports,os=os,ctime=time,geo=geo,body=body))
    global_res += infos
    cprint(" save : {} ".format(c), on_color='on_blue', end='\r')

def parse_done(f):
    r = f.result()
    if r.status_code == 200:
        return parse(r)
    else:
        gprint("Failed:")



def search_in_db(key=None):
    if not key:
        for i in DB_Handle.query(Info):
            lprint(title=i.title, os=i.os, ip=i.ip, ports=i.ports, time=i.ctime, geo=i.geo, body=i.body)
    else:
        printer = lambda i : lprint(title=i.title, os=i.os, ip=i.ip, ports=i.ports, time=i.ctime, geo=i.geo, body=i.body)
        for i in DB_Handle.fuzzy_search(Info, key, printer=printer):
            pass
            

def login_pre(proxy=False):
    global sess
    # if os.path.exists(LOGIN_INFO_SESSION):
        # sess = pickle.load(open(LOGIN_INFO_SESSION,'rb'))

    if not os.path.exists(LOGIN_INFO):
        e,p = login2(proxy=proxy)
        u = {'username':e, 'password':p}
        with open(LOGIN_INFO, 'w') as fp:
            json.dump(u,fp)

        # with open(LOGIN_INFO_SESSION, 'wb') as fp:
            # pickle.dump(sess, fp)

    else:
        with open(LOGIN_INFO) as fp:
            u = json.load(fp)
            login2(u, proxy=proxy)
        # with open(LOGIN_INFO_SESSION, 'wb') as fp:
            # pickle.dump(sess, fp)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--search', nargs='*',help='search key : -s ')
    parser.add_argument('--login', action='store_true', default=False, help='login in fofa')
    parser.add_argument('-l', '--list', action='store_true', default=False, help='list local db.')
    
    parser.add_argument('-L', '--local', action='store_true', default=False, help='search in local db.')
    parser.add_argument('-p', '--page', type=int, default=1, help='set page to search in web')
    parser.add_argument('-P', '--proxy', action='store_true', default=False, help='set proxy')
    
    args = parser.parse_args()

    if args.page == 1:
        page = None
    else:
        page = args.page

    if args.proxy:
        proxy = 'socks5://127.0.0.1:1080'
    else:
        proxy = False
    if args.list:
        search_in_db()
        sys.exit(0)

    if args.login:
        e,p = login2(proxy=proxy)
        u = {'username':e, 'password':p}
        with open(LOGIN_INFO, 'w') as fp:
            json.dump(u,fp)

        with open(LOGIN_INFO_SESSION, 'wb') as fp:
            pickle.dump(sess, fp)
    else:
        if not args.local:
            login_pre(proxy=proxy)

    if len(args.search) == 1:
        if args.local:
            search_in_db(args.search[0])
        else:
            search2(searchstr=args.search[0], page=page)
    elif len(args.search) > 1 and len(args.search) %2 == 0:
        keys = []

        for i in range(0,len(args.search), 2):
            keys.append("%s=\"%s\"" % (args.search[i],args.search[i+1]) ) 
        gprint(str(keys))
        search2(searchstr=" && ".join(keys), page=page)
    


if __name__ == '__main__':
    main()