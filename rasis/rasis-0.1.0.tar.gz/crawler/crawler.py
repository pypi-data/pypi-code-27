# -*- coding: utf-8 -*-

"""Module crawler contains method to crawl web pages.
"""

import scrapy
import scrapy.crawler
import spider

def start(username, password,
    splash_url='http://127.0.0.1:8050', work_dir='.'):

    """start starts a new scrapy crawler process with options.

    Parameters
    ----------
    username : str
        The username(KONAMI ID).
    password : str
        The password.
    splash_url : str
        This crawler need a splash server. Specify the url here.
    work_dir : str
        The directory where places data and logs.

    Some key settings of scrapy are provided below.
    **IMPORTANT** Though it's polite to set a "DOWNLOAD_DELAY" value, the urls
    of ranking pages are changing periodically, which contain an encoded string.
    If the delay is too large(greater than 1sec), the crawler may try to crawl
    a large amount of expired ranking pages containing no data.
    I haven't found a good solution to this issue for now.

    """
    
    process = scrapy.crawler.CrawlerProcess(
        settings={

            'BOT_NAME': 'RASISismyWIFE',

            'USERNAME': username,
            'PASSWORD': password,

            'USER_AGENT': 'scrapy_splash-crawler-by-HinanawiTenshi(dr.paper@live.com)',
            # 'DOWNLOAD_DELAY': 2.0,
            'ROBOTSTXT_OBEY': True,
            'LOG_LEVEL': 'INFO',

            # middlewares
            'SPIDER_MIDDLEWARES': {
                'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
            },
            'DOWNLOADER_MIDDLEWARES': {
                'scrapy_splash.SplashCookiesMiddleware': 723,
                'scrapy_splash.SplashMiddleware': 725,
                'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
            },

            # item pipelines
            'ITEM_PIPELINES': {
                'crawler.pipelines.ItemPipeline': 1,
                'scrapy.pipelines.images.ImagesPipeline': 2,
            },

            # splash configuration
            'SPLASH_URL': splash_url,
            'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
            'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',

            # feed configuration
            'FEED_CSV_URI': work_dir,
            'IMAGES_STORE': work_dir,

            # log configuration
            'LOG_FILE': work_dir + '/crawler.log',
        }
    )

    process.crawl(spider.Spider)

    process.start()
