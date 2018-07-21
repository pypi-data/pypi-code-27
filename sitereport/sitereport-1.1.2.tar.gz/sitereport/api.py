# -*- coding: utf-8 -*-
import sys
import pycurl
import time
import base64
import demjson
from hashlib import md5
try:
    from StringIO import StringIO as BytesIO
    from urllib import quote
    python_version=2
except ImportError:#python3
    from io import BytesIO
    from urllib.parse import quote
    python_version=3

class Api:
    c = pycurl.Curl()
    c.setopt(pycurl.ENCODING, 'gzip')
    c.setopt(pycurl.NOSIGNAL, True)
    c.setopt(pycurl.CONNECTTIMEOUT, 30)  #连接超时时间
    c.setopt(pycurl.TIMEOUT, 60) #请求超时时间
    c.setopt(pycurl.FOLLOWLOCATION, False)
    c.setopt(pycurl.MAXREDIRS, 1)
    access_key=""
    access_secret=""
    endpoint="http://api.sitereport.cn:5566"
    version="1.1.2"

    def __init__(self,access_key,access_secret):
        self.access_key=access_key
        self.access_secret=access_secret

    def v(self):
        return self.version

    def setEndPoint(self,endpoint):
        self.endpoint=endpoint

    def json_decode(self,jsontxt):
        try:
            obj=demjson.decode(jsontxt)
            return obj
        except:
            return None

    def __sign(self,params):
        params=sorted(params.items(), key=lambda item: item[0], reverse=False)
        stringToSignTalbe=[]
        for param in params:
            stringToSignTalbe.append(param[0]+"="+quote(str(param[1])))
        stringToSign = "&".join(stringToSignTalbe)
        sign=md5((self.access_secret+stringToSign).encode()).hexdigest()
        stringToSignTalbe.append("sign="+quote(sign))
        return "&".join(stringToSignTalbe)

    def request(self,path,params):
        params['t']=int(time.time())
        params['access_key']=self.access_key
        buf=BytesIO()
        request_url=self.endpoint+path+"?"+self.__sign(params)
        self.c.setopt(pycurl.WRITEFUNCTION, buf.write)
        self.c.setopt(pycurl.URL,request_url)
        try:
            self.c.perform()
        except Exception as err:
            return (False,err)

        status=self.c.getinfo(pycurl.HTTP_CODE)
        body=buf.getvalue()

        if status==200:
            return True,self.json_decode(body)
        return False,body

    def haosou_count(self,params):
        return self.request("/360/count",params)

    def haosou_search(self,params):
        return self.request("/360/search",params)

    def haosou_hit(self,params):
        return self.request("/360/hit",params)

    def baidu_count(self,params):
        return self.request("/baidu/count",params)

    def baidu_search(self,params):
        return self.request("/baidu/search",params)

    def baidu_searchjson(self,params):
        return self.request("/baidu/searchjson",params)

    def baidu_fengchao(self,params):
        return self.request("/baidu/fengchao",params)

    def baidu_age(self,params):
        return self.request("/baidu/age",params)

    def baidu_fengchao(self,params):
        return self.request("/baidu/fengchao",params)

    def baidu_hit(self,params):
        return self.request("/baidu/hit",params)

    def sm_count(self,params):
        return self.request("/sm/count",params)

    def sm_search(self,params):
        return self.request("/sm/search",params)

    def sm_hit(self,params):
        return self.request("/sm/hit",params)

    def domain_check(self,params):
        return self.request("/domain/check",params)
