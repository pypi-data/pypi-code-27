# -*- coding: utf-8 -*-

from __future__ import print_function

import scrapy
import scrapy_splash
import logging

script = """
function main(splash)
  splash:init_cookies(splash.args.cookies)
  assert(splash:go{
    splash.args.url,
    headers=splash.args.headers,
    http_method=splash.args.http_method,
    body=splash.args.body,
    })
  assert(splash:wait(0.5))

  local entries = splash:history()
  local last_response = entries[#entries].response
  return {
    url = splash:url(),
    headers = last_response.headers,
    cookies = splash:get_cookies(),
    html = splash:html(),
  }
end
"""

class Spider(scrapy.Spider):

    """Spider defines the actions to crawl the data pages.
    """

    name = 'ranking'
    allowed_domains = ['p.eagate.573.jp']
    start_urls = ['https://p.eagate.573.jp/gate/p/login.html']
    data_url = 'https://p.eagate.573.jp/game/sdvx/iv/p/ranking/index.html'

    username = ''
    password = ''

    tune_id = 0

    def start_requests(self):

        self.username = self.settings['USERNAME']
        self.password = self.settings['PASSWORD']

        for url in self.start_urls:
            yield scrapy_splash.SplashRequest(
                url,
                self.parse,
                cache_args=['lua_source'],
                endpoint='execute',
                args={'lua_source': script}
        )

    def parse(self, response):

        """parse processes login page.

        Login Page https://p.eagate.573.jp/gate/p/login.html contains a captcha
        with 6 pictures. One should select the pictures which are similar to
        the first one from the last 5. After plenty of trials, it's likely that
        the number of correct pictures is always 2.

        The current method to do this captcha work is manually opening the 
        picture urls and typing the numbers by hand. The urls will be printed 
        to stdout.

        The form need to be POST to https://p.eagate.573.jp/gate/p/login.html is
            {
                'KID': username,
                'pass': password,
                'kcsess': kcsess,
                'OTP': '',
                'chk_cX': (hash_value),
                'chk_cY': (hash_value)
            }
        X and Y are numbers from {0, 1, 2, 3, 4}.

        """

        print("Logging...")

        kcsess = response.css('input[name="kcsess"]::attr(value)').extract_first()
        chk_origin = response.css('div[style="float:left;"] img::attr(src)').extract_first()
        chks = [{
                'img': response.css('label[for="id_kcaptcha_c0"] img::attr(src)').extract_first(),
                'value': response.css('input[name="chk_c0"]::attr(value)').extract_first(),
            },{
                'img': response.css('label[for="id_kcaptcha_c1"] img::attr(src)').extract_first(),
                'value': response.css('input[name="chk_c1"]::attr(value)').extract_first(),
            },{
                'img': response.css('label[for="id_kcaptcha_c2"] img::attr(src)').extract_first(),
                'value': response.css('input[name="chk_c2"]::attr(value)').extract_first(),
            },{
                'img': response.css('label[for="id_kcaptcha_c3"] img::attr(src)').extract_first(),
                'value': response.css('input[name="chk_c3"]::attr(value)').extract_first(),
            },{
                'img': response.css('label[for="id_kcaptcha_c4"] img::attr(src)').extract_first(),
                'value': response.css('input[name="chk_c4"]::attr(value)').extract_first()
            }
        ]

        formdata = {
            'KID': self.username,
            'pass': self.password,
            'kcsess': kcsess,
            'OTP': '',
        }

        print("Please click the following links and type the number of the two images that are similar to the original one.")
        print("Input two digits, with space as seperator.")
        print("Origin: %s" % (chk_origin))
        print("0: %s" % (chks[0]['img']))
        print("1: %s" % (chks[1]['img']))
        print("2: %s" % (chks[2]['img']))
        print("3: %s" % (chks[3]['img']))
        print("4: %s" % (chks[4]['img']))

        chk_result = raw_input("Please select:")
        for number in chk_result.split(' '):
            formdata['chk_c' + number] = chks[int(number)]['value']

        request = scrapy_splash.SplashFormRequest(
            url=self.start_urls[0],
            method='POST',
            formdata=formdata,
            callback=self.authorized,
            endpoint='execute',
            args={'lua_source': script}
        )

        yield request

        print("Logging...Complete")

    def authorized(self, response):

        """authorized opens the first index pages of all sorts.

        The index pages of music are separated to 10 sorts(五十音順). Each sort
        contains several index pages, and each page contains 10 songs with
        several difficulties. Each difficulty is a link to the ranking page.
        Each page also contains a link to the next page.

        """
        
        for sort in range(1, 11):
            yield scrapy_splash.SplashRequest(
                url=self.data_url + '?sort=' + str(sort) + '&page=1',
                callback=self.parse_ranking_index,
                cache_args=['lua_source'],
                endpoint='execute',
                args={'lua_source': script}
            )

    def parse_ranking_index(self, response):

        """parse_ranking_index processes a index page.

        First, yield all difficulties on this page. Second, go to next page if
        exists.

        """

        for href in response.css('div[class="music_difficulty"] a::attr(href)').extract():
            yield scrapy_splash.SplashRequest(
                url=response.urljoin(href),
                callback=self.parse_ranking,
                cache_args=['lua_source'],
                endpoint='execute',
                args={'lua_source': script}
            )

        next_page = response.css('ddispnext a::attr(href)').extract_first()
        if next_page:
            yield scrapy_splash.SplashRequest(
                url=response.urljoin(next_page),
                callback=self.parse_ranking_index,
                cache_args=['lua_source'],
                endpoint='execute',
                args={'lua_source': script}
            )

    def parse_ranking(self, response):

        """parse_ranking processes a ranking page.

        """

        if not response.css('div#musicname::text').extract_first():
            print('[ERROR]Retrying %s' % (response.url))
            yield scrapy_splash.SplashRequest(
                url=response.url,
                callback=self.parse_ranking,
                cache_args=['lua_source'],
                endpoint='execute',
                args={'lua_source': script}
            )
            return

        tune = {
            'title': response.css('div#musicname::text').extract_first(),
            'artist': response.css('div#artistname::text').extract_first(),
            'level': response.css('div[class="diff_plate"]::text').extract_first(),
            'diff': response.css('div[class="diff_plate"]::attr(id)').extract_first().split('_')[1],
        }

        print("%d: Crawling %s[%s]" % (self.tune_id, tune['title'], tune['diff']))
        self.tune_id += 1

        lines_data = response.css('div[class="player_line"]')
        lines = []
        for i, line in enumerate(lines_data):
            lines.append({
                'rank': i + 1,
                'player_name': line.css('div[class="playername"] a::text').extract_first(),
                'score': line.css('div[class="score"]::text').extract_first(),
                'date': line.css('div[class="date"]::text').extract_first()
            })

        yield {
            'tune': tune,
            'data': lines,
        }

        # yield {
        #     'image_urls': [response.urljoin(response.css('div#artist_area img::attr(src)').extract_first())]
        # }

def save_html(response, path):

    with open(path, 'wb') as f:
        f.write(response.body)
