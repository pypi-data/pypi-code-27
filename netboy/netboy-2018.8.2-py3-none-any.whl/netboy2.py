import functools
import json

from netboy.multi_pycurl.curl_one import work as curl_work
from netboy.netboy import NetBoy

class NetBoyObjects(list):
    def __init__(self, resps):
        self.objects = []
        for group in resps:
            for elem in group:
                self.objects.append(NetBoyObject(elem))

    def __getattr__(self, item):
        return [{'id':index, 'url': obj.url, item: getattr(obj, item)} for index,obj in enumerate(self.objects)]


class NetBoyObject:
    def __init__(self, elem):
        self.__dict__.update(elem)
    def __getattr__(self, item):
        if item=='json':
            data = self.__dict__.get('data')
            if isinstance(data, str):
                return json.loads(data)
        return None



class NetBoy2:
    def __init__(self):
        self.boy = NetBoy()


    def request(self, urls, **kwargs):
        boy = NetBoy()
        boy.use_spider(kwargs.get('spider', 'pycurl')) \
            .use_filter(kwargs.get('filter', ['url', 'title', 'effect', 'data', 'code', 'time', 'header'])) \
            .use_mode(kwargs.get('mode', 'thread')) \
            .use_timeout(*kwargs.get('timeout', (10, 5, 5, 5))) \
            .use_workers(*kwargs.get('workers', (4, 2, 2))) \
            .use_cookies(kwargs.get('cookies', None)) \
            .use_headers(kwargs.get('headers', None)) \
            .use_useragent(kwargs.get('useragent', 'Mozilla/5.0 (X11; Linux x86_64; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm; Baiduspider/2.0; +http://www.baidu.com/search/spider.html) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80() Safari/537.36')) \
            .use_prepares(kwargs.get('prepares', None)) \
            .use_triggers(kwargs.get('triggers', None)) \
            .use_analysers(kwargs.get('analysers', None)) \
            .use_final(kwargs.get('final', None)) \
            .use_http_proxy(kwargs.get('http_proxy'), None) \
            .use_socks5_proxy(kwargs.get('socks5_proxy'), None) \
            .use_queue(kwargs.get('queue', None)) \
            .use_logger(kwargs.get('logger', None)) \
            .use_info(kwargs.get('info', None))

        postfields = kwargs.get('postfields')
        if postfields:
            boy.use_postfields(postfields, kwargs.get('method', 'post'))
        resp = boy.run(urls)
        return resp

    def work(self, url, method, **kwargs):
        kwargs['postfields'] = kwargs.get('data')
        kwargs['method'] = method
        resp = self.request([url], **kwargs)
        return NetBoyObject(resp[0][0])

    def works(self, *args, **kwargs):
        kwargs['postfields'] = kwargs.get('data')
        kwargs['method'] = kwargs.get('method', 'get')
        if isinstance(args[0], list):
            resp = self.request(args[0], **kwargs)
        else:
            resp = self.request(args, **kwargs)
        return NetBoyObjects(resp)

    def __getattr__(self, item):
        if item in ['gets', 'posts', 'heads', 'deletes', 'puts', 'patches']:
            if item == 'patches':
                method = item.replace('es', '')
            else:
                method = item.replace('s', '')
            return functools.partial(self.works, method=method)
        if item in ['get', 'post', 'head', 'delete', 'put', 'patch']:
            return functools.partial(self.work, method=item)
        return None


if __name__ == '__main__':
    boy = NetBoy2()
    # resp = boy.get('127.0.0.1:9994',headers=['test: again'])
    # print(resp.data)
    # resp = boy.get('127.0.0.1:9994',cookies={'test': 'again', 'what': 'whack'})
    # print(resp.data)
    # resp = boy.gets('www.douban.com', 'bing.com', filter=['title','time'])
    # print(resp.title, resp.time)
    # resp = boy.get('www.douban.com')
    # print(resp.title)
    # # resp = boy.gets(['www.douban.com', 'bing.com'])
    # # print(resp.code)
    # resp = boy.posts('127.0.0.1:9995', '127.0.0.1:9995', data={'你好': '世界'})
    # print(resp.json, type(resp.json))
    resp = boy.deletes('127.0.0.1:9995/delete', '127.0.0.1:9995/delete', data={'你好': '世界'})
    print(json.dumps(resp.data, indent=2, ensure_ascii=False))
    # resp = boy.patches('127.0.0.1:9995/patch', '127.0.0.1:9995/patch', data={'你好': '世界'})
    # print(json.dumps(resp.data, indent=2, ensure_ascii=False))
    # resp = boy.heads('127.0.0.1:9995/head','127.0.0.1:9995/get', 'www.baidu.com', data={'你好': '世界'})
    # print(json.dumps(resp.code, indent=2, ensure_ascii=False))
    # print(resp.json, type(resp.json))
    # print(resp.data, type(resp.data))
