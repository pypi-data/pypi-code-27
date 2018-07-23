import requests
import logging
import getpass
import base64
import sys
import re
import os
import json
import pickle
from bs4 import BeautifulSoup as BS
from termcolor import cprint, colored
import argparse
from .test import load, ls_mod
from .libs import TestBase
from .log import gprint, lprint, rprint
from .fofa_search import Fofa
from .common_tools import search_in_db

global_res = []



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


def test(*module_names):
    if not len(prepare_test_info) > 0:
        rprint("No targets")
        return

    for name in module_names:
        Obj = load(name)
        if not Obj:continue
        for info in prepare_test_info:
            t = TestBase(info)
        TestBase.run(Obj)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--search', nargs='*',help='search key : -s ')
    parser.add_argument('--login', action='store_true', default=False, help='login in fofa')
    parser.add_argument('-l', '--list', action='store_true', default=False, help='list local db.')
    
    parser.add_argument('-L', '--local', action='store_false', default=True, help='search in local db.')
    parser.add_argument('-p', '--page', type=int, default=1, help='set page to search in web')
    parser.add_argument('-P', '--proxy', action='store_true', default=False, help='set proxy')
    parser.add_argument('-t', '--test', nargs='*', help='use test module to test result')
    parser.add_argument('--ls-mod', action='store_true', default=False, help='list module to use:')
    
    args = parser.parse_args()
    prepare_test_info = []
    fofa = None
    if args.page == 1:
        page = None
    else:
        page = args.page

    if args.proxy:
        proxy = 'socks5://127.0.0.1:1080'
    else:
        proxy = False
    if args.list:
        prepare_test_info = search_in_db()
        sys.exit(0)

    if args.login:
        fofa = Fofa(proxy=proxy)
        e,p = fofa.login()
        u = {'username':e, 'password':p}
        
    else:
        if not args.local:
            fofa = Fofa(proxy=proxy)
            fofa.load_session_login()

    if args.search:
        if  len(args.search) == 1:
            if args.local:
                prepare_test_info =search_in_db(args.search[0])
            else:
                fofa.search(key=args.search[0], page=page)
        elif len(args.search) > 1 and args.local:
            prepare_test_info = search_in_db(*args.search)

        elif len(args.search) > 1 and len(args.search) %2 == 0:
            keys = []
            for i in range(0,len(args.search), 2):
                keys.append("%s=\"%s\"" % (args.search[i],args.search[i+1]) ) 
            gprint(str(keys))
            fofa.search(key=" && ".join(keys), page=page)
    if args.ls_mod:
        ls_mod()
    if args.test and len(args.test)> 0:
        gprint("Test -- > %s " % " ".join(args.test))
        test(*args.test)

if __name__ == '__main__':
    main()