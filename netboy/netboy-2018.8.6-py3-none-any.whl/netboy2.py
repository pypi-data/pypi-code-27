import functools
import json

from netboy.multi_pycurl.curl_one import work as curl_work
from netboy.netboy import NetBoy

class NetBoyObjects(list):
    def __init__(self, resps):
        # self.objects = []
        for group in resps:
            for elem in group:
                self.append(NetBoyObject(elem))

    def __getattr__(self, item):
        return [{'id':index, 'url': obj.url, item: getattr(obj, item)} for index,obj in enumerate(self)]

    def __getitem__(self, key):
        if isinstance(key, int):
            return list.__getitem__(self, key)
        if isinstance(key, str):
            for o in self:
                if o.url == key:
                    return o
        return None

    def __iter__(self):
        return list.__iter__(self)



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
    def __init__(self, **kwargs):
        self.boy = NetBoy()
        self.kwargs = kwargs

    def getparam(self, config, key, default=None):
        return config.get(key, self.kwargs.get(key, default))

    def request(self, urls, **kwargs):
        boy = NetBoy()
        boy.use_spider(self.getparam(kwargs, 'spider', 'pycurl')) \
            .use_filter(self.getparam(kwargs, 'filter', ['url', 'title', 'effect', 'data', 'code', 'time', 'header'])) \
            .use_mode(self.getparam(kwargs, 'mode', 'thread')) \
            .use_timeout(*self.getparam(kwargs, 'timeout', (10, 5, 5, 5))) \
            .use_workers(*self.getparam(kwargs, 'workers', (4, 2, 2))) \
            .use_cookies(self.getparam(kwargs, 'cookies', None)) \
            .use_headers(self.getparam(kwargs, 'headers', None)) \
            .use_useragent(self.getparam(kwargs, 'useragent', 'Mozilla/5.0 (X11; Linux x86_64; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm; Baiduspider/2.0; +http://www.baidu.com/search/spider.html) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80() Safari/537.36')) \
            .use_prepares(self.getparam(kwargs, 'prepares', None)) \
            .use_triggers(self.getparam(kwargs, 'triggers', None)) \
            .use_analysers(self.getparam(kwargs, 'analysers', None)) \
            .use_final(self.getparam(kwargs, 'final', None)) \
            .use_http_proxy(self.getparam(kwargs, 'http_proxy', None)) \
            .use_socks5_proxy(self.getparam(kwargs, 'socks5_proxy', None)) \
            .use_queue(self.getparam(kwargs, 'queue', None)) \
            .use_logger(self.getparam(kwargs, 'logger', None)) \
            .use_maxredirs(self.getparam(kwargs, 'maxredirs', 10)) \
            .use_followlocation(self.getparam(kwargs, 'followlocation', 1)) \
            .use_info(self.getparam(kwargs, 'info', None))

        postfields = kwargs.get('postfields')
        if postfields:
            boy.use_postfields(postfields, kwargs.get('method', 'post'))
        resp = boy.run(urls)
        return resp

    def work(self, url, method, **kwargs):
        kwargs['postfields'] = self.getparam(kwargs, 'data', None)
        kwargs['method'] = method
        resp = self.request([url], **kwargs)
        return NetBoyObject(resp[0][0])

    def works(self, *args, **kwargs):
        kwargs['postfields'] = self.getparam(kwargs, 'data', None)
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
    boy = NetBoy2(data={'你好': '世界'})
    # resp = boy.get('127.0.0.1:9994',headers=['test: again'])
    # print(resp.data)
    # resp = boy.get('127.0.0.1:9994',cookies={'test': 'again', 'what': 'whack'})
    # print(resp.data)
    resp = boy.gets('www.douban.com', 'bing.com', filter=['title','time','url'])
    print(resp)
    print(resp.title, resp.time)
    for r in resp:
        print(r)
    print(resp[0].title)
    print(resp[1].title)
    print(len(resp))
    o = resp['www.douban.com']
    print(o, type(o), o.title)

    # resp = boy.get('www.douban.com')
    # print(resp.title)
    # # resp = boy.gets(['www.douban.com', 'bing.com'])
    # # print(resp.code)
    # resp = boy.posts('127.0.0.1:9995', '127.0.0.1:9995', data={'你好': '世界'})
    # print(resp.json, type(resp.json))
    # resp = boy.deletes('127.0.0.1:9995/delete', '127.0.0.1:9995/delete', data={1:2})
    # print(json.dumps(resp.data, indent=2, ensure_ascii=False))
    # resp = boy.patches('127.0.0.1:9995/patch', '127.0.0.1:9995/patch', data={'你好': '世界'})
    # print(json.dumps(resp.data, indent=2, ensure_ascii=False))
    # resp = boy.heads('127.0.0.1:9995/head','127.0.0.1:9995/get', 'www.baidu.com', data={'你好': '世界'})
    # print(json.dumps(resp.code, indent=2, ensure_ascii=False))
    # print(resp.json, type(resp.json))
    # print(resp.data, type(resp.data))
