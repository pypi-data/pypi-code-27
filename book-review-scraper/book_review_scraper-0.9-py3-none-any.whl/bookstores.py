import re
from requests_html import HTMLSession
from .exceptions import (FindBookIDError, ScrapeReviewContentsError, ISBNError, PagingError, NoReviewError)
from .helper import (ReviewPagingHelper, calculate_rating)
from .review import (NaverbookBookReviewInfo, KyoboBookReviewInfo, Yes24BookReviewInfo)
from .config import (NaverBookConfig, Yes24Config, KyoboConfig)
from .parsing import parsing_review_info

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://203.229.225.135/tm/?a=CR&b=MAC&c=300015071805&d=32&e=5301&f=Ym9vay5uYXZlci5jb20='
               '&g=1527138088560&h=1527138088581&y=0&z=0&x=1&w=2017-11-06&in=5301_00014684&id=20180524',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/66.0.3359.181 Safari/537.36',
}


class BookStore(object):
    """ 인터넷서점을 나타내는 클래스들의 부모 클래스

    """

    def __init__(self, scrape_config, search_url=None):
        """
        :param scrape_config: 가져올 리뷰 설정
        :param search_url: 책 id 를 찾기 위한 검색 url
        """
        self.session = HTMLSession()
        self.scrape_config = scrape_config
        self.search_url = search_url

    def get_review_info(self, isbn13):
        """ 책의 리뷰 정보를 리턴한다.(ex 리뷰 총 개수, 평점) 리뷰정보는 서점마다 다름

        :param isbn13: 책의 isbn
        :return: 책의 리뷰 정보
        """
        raise NotImplementedError()

    def prepare_gen_reviews(self, isbn13):
        """ 리뷰들을 가져올 준비를 한다.

        :param isbn13: 책의 isbn13
        :return: 리뷰를 가져오기 위한 준비물들을 튜플형태로 리턴
        isbn13 : 책 isbn13,
        book_id : 책 id,
        start_page : start_idx 번째에 있는 리뷰가 있는 페이지,
        end_page : end_idx 번째에 있는 리뷰가 있는 페이지,
        start_review_idx : start_page 안에서 start_idx 번째 리뷰의 idx
        end_review_idx : end_page 안에서 end_idx 번째 리뷰의 idx
        count_to_get : 총 얻을 리뷰의 개수
        html : 리뷰 페이지의 html

        ex) start = 16, end = 49, count of reviews per page = 10
        start_page = 2 , end_page = 5
        start_review_idx = 5, end_review_idx = 9
        count_to_get = 34
        """
        review_info = self.get_review_info(isbn13)
        book_id = review_info.book_id

        helper = ReviewPagingHelper(self.scrape_config.start,
                                    self.scrape_config.end,
                                    self.scrape_config.per_page)

        start_page = helper.start_page
        end_page = helper.end_page
        start_review_idx = helper.start_idx
        end_review_idx = helper.end_idx
        count_to_get = helper.count_to_get

        return isbn13, book_id, start_page, end_page, start_review_idx, end_review_idx, count_to_get

    def gen_reviews(self, isbn13, book_id, start_page, end_page,
                    start_review_idx, end_review_idx, count_to_get):
        """

        :param isbn13: 책의 isbn13
        :param book_id: 책 id
        :param start_page: 스크래핑을 시작할 리뷰 시작 페이지
        :param end_page: 스크래핑이 끝나야 하는 페이지
        :param start_review_idx: 스크래핑을 시작할 리뷰 위치
        :param end_review_idx: 스크래핑을 끝내야할 리뷰 위치
        :param count_to_get: 스크래핑할 최대 리뷰 수
        :return: 책에 대한 리뷰 제너레이터
        """
        cur_page = start_page
        cur_count = 0

        response = self.session.get(self.scrape_config.page_url(book_id, cur_page),
                                    headers=headers)
        if not response.ok:
            raise PagingError(bookstore=self.__str__(), isbn13=isbn13)

        ul = response.html.xpath(self.scrape_config.ul_xpath, first=True)

        if ul is None:
            raise NoReviewError(bookstore=self.__str__(), isbn13=isbn13)

        while cur_page <= end_page:
            s = 0 if (cur_page != start_page) else start_review_idx
            e = self.scrape_config.per_page + 1 if (cur_page != end_page) else end_review_idx

            try:
                for li in ul.xpath(self.scrape_config.li_xpath)[s:e]:
                    review_meta_class = self.scrape_config.review_meta_class
                    yield review_meta_class.instance(li, isbn13)
                    cur_count += 1
                    if cur_count >= count_to_get:
                        return
            except (IndexError, AttributeError, ValueError):
                raise ScrapeReviewContentsError(bookstore=self.__str__(), isbn13=isbn13, idx=cur_count)
            cur_page += 1
            response = self.session.get(self.scrape_config.page_url(book_id, cur_page),
                                        headers=headers)
            if not response.ok:
                raise PagingError(bookstore=self.__str__(), isbn13=isbn13)

            ul = response.html.xpath(self.scrape_config.ul_xpath, first=True)

    def get_reviews(self, isbn13):
        """ 책의 리뷰들을 가지고 온다. (각각 인터넷 서점의 기본 정렬 순)

        :param isbn13: 책 isbn13
        :return: 책 리뷰 제너레이터
        """
        prepared = self.prepare_gen_reviews(isbn13)
        yield from self.gen_reviews(*prepared)

    def __str__(self):
        return self.__class__.__name__


class Naverbook(BookStore):

    def __init__(self, scrape_config=NaverBookConfig.blog(1, 10)):
        super().__init__(
            scrape_config=scrape_config,
            search_url='http://book.naver.com/search/search.nhn?sm=sta_hty.book&sug=&where=nexearch&query='
        )
        self.id_a_tag_xpath = "//a[starts-with(@href,'http://book.naver.com/bookdb/book_detail.nhn?bid=')]"

    def get_review_info(self, isbn13):
        if re.match('[\d+]{13}', str(isbn13)) is None:
            raise ISBNError(bookstore=self, isbn13=isbn13)

        response = self.session.get(self.search_url + f'{isbn13}', headers=headers)

        try:
            row = response.html.xpath("//ul[@id='searchBiblioList']/li[@style='position:relative;']")[0]
            info_li = row.text.split('\n')
            info_text = info_li[3]
            id_a_tag = row.xpath(self.id_a_tag_xpath)[0]
            title = info_li[0]
            book_id = int(id_a_tag.attrs['href'].split('=')[-1])
            return NaverbookBookReviewInfo(book_id, title, *parsing_review_info(info_text))

        except (ValueError, IndexError, AttributeError):
            raise FindBookIDError(isbn13=isbn13, bookstore=self)


class Kyobo(BookStore):

    def __init__(self, scrape_config=KyoboConfig.klover(1, 10)):
        super().__init__(scrape_config=scrape_config,
                         search_url='http://www.kyobobook.co.kr/search/SearchKorbookMain.jsp?'
                                    'vPstrCategory=KOR&vPstrKeyWord={}&vPplace=top')

    def get_review_info(self, isbn13):
        if re.match('[\d+]{13}', str(isbn13)) is None:
            raise ISBNError(bookstore=self, isbn13=isbn13)

        response = self.session.get(self.search_url.format(isbn13), headers=headers)
        row = response.html.xpath("//table[@class='type_list']/tbody/tr")[0]

        book_title = row.xpath("//div[@class='title']//strong")[0].text
        klover_rating_text = row.xpath("//div[@class='review klover']//b")[0].text
        book_log_cnt_text = row.xpath("//div[@class='review booklog']//b")[0].text
        book_log_rating_text = row.xpath("//div[@class='rating']/img")[0].attrs['alt']

        klover_rating = float(re.search("\d+\.?\d{0,3}", klover_rating_text).group())
        book_log_cnt = int(book_log_cnt_text)
        book_log_rating = float(re.search('5점 만점에 (\d)점', book_log_rating_text).group(1))

        return KyoboBookReviewInfo(isbn13, book_title, klover_rating, book_log_rating, book_log_cnt)


class Yes24(BookStore):

    def __init__(self, scrape_config=Yes24Config.simple(1, 10)):
        super().__init__(scrape_config,
                         search_url='http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&query={}')

    def get_review_info(self, isbn13):
        if re.match('[\d+]{13}', str(isbn13)) is None:
            raise ISBNError(bookstore=self, isbn13=isbn13)

        response = self.session.get(self.search_url.format(isbn13), headers=headers)
        row = response.html.xpath("//div[@class='goodsList goodsList_list']//td[@ class ='goods_infogrp']")[0]
        book_id_text = row.xpath("td/p/a")[0].attrs['href']
        review_info_text = row.xpath("td/p[4]")[0].text
        review_rating_src = [img.attrs['src'] for img in row.xpath("td/p[4]/img")]

        book_id = int(re.search('goods\/(\d+)', book_id_text).group(1))
        book_title = row.xpath("td/p/a/strong")[0].text
        rating = calculate_rating(review_rating_src)
        member_review_count = 0
        compiled_review_text = re.search('회원리뷰 \((\d+)개\)', review_info_text)

        if compiled_review_text is not None:
            member_review_count = int(compiled_review_text.group(1))

        return Yes24BookReviewInfo(book_id, book_title, rating[0], rating[1], member_review_count)
