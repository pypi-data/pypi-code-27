
from pytube import YouTube
import os
#from lxml import html
#import requests

#import urlparse
from selenium import webdriver
import time

base_href="https://www.youtube.com"
watch_href="https://www.youtube.com/watch?"
start_page="https://www.youtube.com/results?search_query=car+accident+\"dashcam\""


def downloadYouTube(videourl, path):
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not os.path.exists(path):
        os.makedirs(path)
    yt.download(path)

def crawl():
    driver = webdriver.Firefox()
    driver.get(start_page)
    time.sleep(0.5)
    SCROLL_PAUSE_TIME = 1

    for i in range(20):
        driver.execute_script("window.scrollTo(0,"+str(3000*i)+");")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

    elems = driver.find_elements_by_xpath("//a[@href]")

    waiting=set()
    crawled=set()

    for elem in elems:
        if watch_href in elem.get_attribute("href"):
            waiting.add(elem.get_attribute("href"))
            print elem.get_attribute("href")

    while(len(waiting)!=0):
        current_page=waiting.pop()
        downloadYouTube(current_page, './accidentvideos')   
        crawled.add(current_page)