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

    # def head(self, url, **kwargs):
    #     kwargs['postfields'] = kwargs.get('data')
    #     kwargs['method'] = 'head'
    #     resp = self.request([url], **kwargs)
    #     return NetBoyObject(resp[0][0])
    #
    # def heads(self, *args, **kwargs):
    #     kwargs['postfields'] = kwargs.get('data')
    #     kwargs['method'] = 'get'
    #     if isinstance(args[0], list):
    #         resp = self.request(args[0], **kwargs)
    #     else:
    #         resp = self.request(args, **kwargs)
    #     return NetBoyObjects(resp)

    # def get(self, url, **kwargs):
    #     kwargs['postfields'] = kwargs.get('data')
    #     kwargs['method'] = 'get'
    #     resp = self.request([url], **kwargs)
    #     return NetBoyObject(resp[0][0])
    #
    # def gets(self, *args, **kwargs):
    #     kwargs['postfields'] = kwargs.get('data')
    #     kwargs['method'] = 'get'
    #     if isinstance(args[0], list):
    #         resp = self.request(args[0], **kwargs)
    #     else:
    #         resp = self.request(args, **kwargs)
    #     return NetBoyObjects(resp)

    # def post(self, url, **kwargs):
    #     kwargs['postfields'] = kwargs.get('data')
    #     kwargs['method'] = 'post'
    #     resp = self.request([url], **kwargs)
    #     return NetBoyObject(resp[0][0])
    #
    # def posts(self, *args, **kwargs):
    #     kwargs['postfields'] = kwargs.get('data')
    #     kwargs['method'] = 'post'
    #     if isinstance(args[0], list):
    #         resp = self.request(args[0], **kwargs)
    #     else:
    #         resp = self.request(args, **kwargs)
    #     return NetBoyObjects(resp)
    #
    # def put(self, url, data, **kwargs):
    #     kwargs['postfields'] = data
    #     kwargs['method'] = 'put'
    #     resp = self.request([url], **kwargs)
    #     return NetBoyObject(resp[0][0])
    #
    # def puts(self, *args, **kwargs):
    #     kwargs['postfields'] = kwargs.get('data')
    #     kwargs['method'] = 'put'
    #     if isinstance(args[0], list):
    #         resp = self.request(args[0], **kwargs)
    #     else:
    #         resp = self.request(args, **kwargs)
    #     return NetBoyObjects(resp)
    #
    # def delete(self, url, data, **kwargs):
    #     kwargs['postfields'] = data
    #     kwargs['method'] = 'delete'
    #     resp = self.request([url], **kwargs)
    #     return NetBoyObject(resp[0][0])
    #
    # def deletes(self, *args, **kwargs):
    #     kwargs['postfields'] = kwargs.get('data')
    #     kwargs['method'] = 'delete'
    #     if isinstance(args[0], list):
    #         resp = self.request(args[0], **kwargs)
    #     else:
    #         resp = self.request(args, **kwargs)
    #     return NetBoyObjects(resp)
    #
    # def patch(self, url, data, **kwargs):
    #     kwargs['postfields'] = data
    #     kwargs['method'] = 'patch'
    #     resp = self.request([url], **kwargs)
    #     return NetBoyObject(resp[0][0])
    #
    # def patches(self, *args, **kwargs):
    #     kwargs['postfields'] = kwargs.get('data')
    #     kwargs['method'] = 'patch'
    #     if isinstance(args[0], list):
    #         resp = self.request(args[0], **kwargs)
    #     else:
    #         resp = self.request(args, **kwargs)
    #     return NetBoyObjects(resp)

    def request(self, urls, **kwargs):
        boy = NetBoy()
        boy.use_spider(kwargs.get('spider', 'pycurl')) \
            .use_filter(kwargs.get('filter', ['url', 'title', 'effect', 'data', 'code', 'header'])) \
            .use_mode(kwargs.get('mode', 'thread')) \
            .use_timeout(*kwargs.get('timeout', (10, 5, 5, 5))) \
            .use_workers(*kwargs.get('workers', (4, 2, 2))) \
            .use_headers(kwargs.get('headers', None))
        postfields = kwargs.get('postfields')
        if postfields:
            boy.use_postfields(postfields, kwargs.get('method', 'post'))
        cookies = kwargs.get('cookies')
        if cookies:
            boy.use_cookies(cookies)
        # boy.info['cookie'] = 't1=v1;t2=v2'.encode("utf8")
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
