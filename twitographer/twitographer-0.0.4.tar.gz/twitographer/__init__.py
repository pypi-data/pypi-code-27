# twitographer.py -- a parallelized web crawler to traverse the twitter graph
# liveb33f

import os
import sys
import time
import json
import redis
import signal
import asyncio
import logging
import credentials
import multiprocessing as mp
from pyppeteer import launch


class Logger:
    def __init__(self):
        self.logger = logging.basicConfig(format='%(asctime)s \033[31;1m'+str(os.getpid())+'\033[0m: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')


    def log(self, msg, level='info'):
        if level == 'info':
            logging.info(msg)
        elif level == 'warn':
            logging.warning(msg)


class Crawler:
    async def login(self, creds):
        username_selector = ".js-username-field"
        password_selector = ".js-password-field"
        login_selector = "button.submit"
        url = "https://twitter.com/login"
        browser = await launch({"headless": True})
        self.page = await browser.newPage()
        await self.page.goto(url)
        await self.page.waitForSelector(password_selector)
        await self.page.click(username_selector)
        await self.page.waitFor(50) # these delays are mostly arbirtary, how low can we push them? can we just go by selector detection?
        await self.page.keyboard.type(creds['username'])
        await self.page.waitFor(200)
        await self.page.click(password_selector)
        await self.page.waitFor(50)
        await self.page.keyboard.type(creds['password'])
        await self.page.waitFor(200)
        await self.page.click(login_selector)


    async def crawl(self, user):
        scroll_delay = 500
        await self.page.waitFor(scroll_delay)
        await self.page.goto('https://twitter.com/'+user+'/following')
        try:
            await self.page.waitForSelector('div.GridTimeline-items > div.Grid--withGutter')
        except:
            return False
        await self.page.waitFor(200)
        valid = await self.is_page_valid()
        if valid == False:
            return False
        follows = {}
        scrolls = 0
        while True:
            if scrolls == 0:
              previous_height = 0
            else:
              previous_height = await self.page.evaluate('document.body.scrollHeight')
            follows = await self.extract_items(user)
            await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await self.page.waitFor(scroll_delay)
            new_height = await self.page.evaluate('document.body.scrollHeight')
            scrolls += 1
            if previous_height == new_height:
                break

        return follows


    async def is_page_valid(self):
        # check for too many followers
        follower_count = await self.page.querySelector('a[data-nav="following"] > span.ProfileNav-value')
        follower_count = await self.page.evaluate('(element) => element.getAttribute("data-count")', follower_count)
        if int(follower_count) > 1000:
            return False
        # account locked?
        protected = await self.page.querySelector('div.ProtectedTimeline')
        if protected:
            return false
        # no follows?
        empty = await self.page.querySelector('div.GridTimeline-emptyText')
        empty = await self.page.evaluate('(element) => element.getAttribute("display")', empty)
        if empty == 'none':
            return False
        return True


    async def extract_items(self, user):
        follows = {}
        extracted_elements = await self.page.querySelectorAll('div.ProfileCard')
        for element in extracted_elements:
            follow_screen_name = await self.page.evaluate('(element) => element.getAttribute("data-screen-name")', element)
            if follow_screen_name == user:
                continue
            follow_user_id = await self.page.evaluate('(element) => element.getAttribute("data-user-id")', element)
            follows[follow_screen_name] = follow_user_id

        return follows


class Recorder:
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def save_graph(self, user, follows):
        self.r.sadd('graph:'+user, follows)
        self.r.sadd('parsed_users', user)


    def add_to_queue(self, list):
        if(len(list) > 0):
            self.r.sadd('queue', *list)


    def save_duplicates(self, list):
        if(len(list) > 0):
            self.r.rpush('duplicates', *list)


    def skip_user(self, user):
        self.r.rpush('skipped', user)


    def set_in_progress(self, user):
        self.r.sadd('in_progress', user)


    def resolve_in_progress(self, user):
        self.r.srem('in_progress', user)


    def resume_in_progress(self):
        self.r.spop('in_progress')


class Cartographer:
    def __init__(self):
        signal.signal(signal.SIGINT, self.catch_interrupt)
        self.recorder = Recorder()
        self.logger = Logger()


    def process_follows(self, user, follows):
        duplicates = []
        duplicates = self.deduplicate_follows(user, follows)

        self.recorder.save_graph(user, follows)
        self.recorder.add_to_queue(follows)
        self.recorder.save_duplicates(duplicates)

        print('=================================================================================================================')
        self.logger.log('@'+user+' follows '+str(len(follows))+' accounts; found '+str(len(duplicates))+' duplicates; adding '+str(len(follows) - len(duplicates))+' accounts to queue.')
        self.logger.log('The queue has '+str(self.recorder.r.scard('queue'))+' accounts; we\'ve explored '+str(self.recorder.r.scard('parsed_users'))+' nodes so far.')
        print('=================================================================================================================')


    def deduplicate_follows(self, user, follows):
        duplicates = self.recorder.r.sinter('graph:'+user, 'parsed_users')
        return duplicates


    def catch_interrupt(self, sig_num, stack_frame):
        self.logger.log('Caught exit signal')
        self.logger.log('Flushing data to db...')
        self.recorder.r.save()
        self.logger.log('Exiting')
        sys.exit(0)
        return


async def Conductor(creds):
    crawler = Crawler()
    await crawler.login(creds)
    cartographer = Cartographer()

    while True:
        if cartographer.recorder.r.scard('queue') <= 0:
            time.sleep(60)
            if cartographer.recorder.r.scard('queue') <= 0:
                cartographer.logger.log('Graph traversed')
                cartographer.recorder.r.save()
                return
        user = cartographer.recorder.r.spop('queue')
        user = user.decode("utf-8") # spop returns bytes b'key
        cartographer.recorder.set_in_progress(user)
        cartographer.logger.log('Crawling @'+user+'...')
        follows = await crawler.crawl(user)
        if follows == False:
            cartographer.logger.log('====== Skipping @'+user+'; either the user follows too many accounts or we can\'t see the page ======')
            cartographer.recorder.skip_user(user)
        else:
            cartographer.process_follows(user, follows)
        cartographer.recorder.resolve_in_progress(user)

def initialize_queue():
    if len(sys.argv) >= 2:
        entry_point = str(sys.argv[1])
    else:
        entry_point = 'dril'
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    resume = r.spop('in_progress')
    if resume:
        r.sadd('queue', resume)
    elif r.scard('queue') == 0:
        r.sadd('queue', entry_point)
    r = None


def Manager(creds):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(Conductor(creds))


if __name__ == "__main__":
    initialize_queue()
    cred_list = credentials.creds
    if len(cred_list) <= mp.cpu_count():
        size = len(cred_list)
    else:
        size = mp.cpu_count

    jobs = []
    for _ in range(size):
        cred = cred_list.pop()
        job = mp.Process(target=Manager, args=(cred,))
        jobs.append(job)
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
