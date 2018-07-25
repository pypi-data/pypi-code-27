#!/usr/bin/python

import sys
import threading
import time
import requests

data = []
thread_limit = 50


class myThread (threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        val = requests.get(self.url).status_code
        data.append(str(val) + ":" + self.url)


def getStatus(urls):
    """
    getStatus(list_of_urls)
    """
    initial = threading.activeCount()
    for url in urls:
        if url == '' or url == '\n':
            continue
        myThread(url.strip()).start()
        # do not increase the max number of threads more tha 99
        # while threading.activeCount() > 50: ; 50 is max number of threads
        while threading.activeCount() > thread_limit:
            time.sleep(1)
    while threading.activeCount() > initial:
        time.sleep(1)
    return data
