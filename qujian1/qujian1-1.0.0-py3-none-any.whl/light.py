import socket
import threading
import re
import os.path
from urllib.parse import urlparse
from .tm import render_template   #导入模板引擎tm 里边的render_template 方法。

class server():
    def __init__(self):
        self.host = ""
        self.port = 8888
        self.listen = 512
        self.recvNum=1024
        self.staticDir="static"
        self.ico="1.ico"
        self.staticType=".jpg,.png,.gif,.css,.js,.html"
        self.mimeType={".jpg":"image/jpeg",".png":"image/png",".gif":"image/gif",".css":"text/css",".js":"application/x-javascript",".html":"text/html"}
        self.routeInfo=[]
        self.template_dir="template"

    #采集路由的信息
    def route(self,url,methods=["GET"]):
        def fn(callback):
            obj={}
            obj["params"]=re.findall(r':([^/]+)',url)
            obj["url"]=re.sub(r':[^/]+',"(\w+)",url)
            obj["callback"]=callback
            obj["methods"]=methods
            self.routeInfo.append(obj)
        return fn

    #请求头信息
    def parse_headers(self,response):
        info=""
        info+=response["headers"]["pool"]+" "+response["headers"]["status_code"]+"\r\n"
        info+="content-type:"+response["headers"]["content-type"]+"\r\n\r\n"
        return info.encode(encoding="utf8")

    #请求的动态的路由做处理
    def route_handle(self,requestData,clientTcp):
        flag=True
        for item in self.routeInfo:
            reg=item["url"]
            result=re.match(r'%s'%(reg),requestData["path"])
            if  result and item["methods"].count(requestData["type"])>0:
                for item1 in range(len(item["params"])):
                    requestData["params"][item["params"][item1]]=result.group(item1+1)

                flag=False
                response={}
                response["headers"]={}
                response["headers"]["pool"]="HTTP/1.1"
                response["headers"]["status_code"]="200 ok"
                response["headers"]["content-type"]="text/html;charset=utf-8"
                body=item["callback"](requestData,response)
                headers=self.parse_headers(response)
                clientTcp.send(headers+body.encode(encoding="utf8"))
                clientTcp.close()
                break
        if flag:

            clientTcp.send(b"HTTP/1.1 404 \r\n\r\n this page not find")
            clientTcp.close()

    #对请求的数据进行格式化
    def requestData_handle(self,requestData):
        obj={}
        requestInfo = (requestData.decode(encoding="utf8").splitlines())
        if len(requestInfo)>0:
            firstInfo = requestInfo[0]  #获取客户端请求的地址 和协议
            type=re.match(r'[^\s]+',firstInfo).group(0) #获取请求的方法，"GET"
            obj["type"]=type #记录obj里边的type为 GET
            requestUrl = urlparse(re.match(r'\w+\s+(/[^\s]*)', firstInfo).group(1))
            #urlparse 正则匹配firstInfo 的信息 获得6个参数其中第三个参数path为GET 方法和 路径
            obj["path"]=requestUrl[2] # 记录obj里边的path为 /a/2
            obj["query"]={}
            obj["params"]={}
            if requestUrl[4]: #此为query参数记录的值
                for item in requestUrl[4].split("&"):
                #split() 通过指定分隔符对字符串进行切片,此处先用数据中的&切片，再用数据中的=切片
                #比如数据是name=lisi&id=1
                    arr=item.split("=")
                    obj["query"][arr[0]]=arr[1]  #记录obj里边query为{'name': 'lisi', 'id': '1'}
        return obj #将格式化好的obj返回

    # 处理请求的逻辑
    def request_handle(self,requestData,clientTcp):
        requestUrl=requestData["path"]
        if requestUrl=="/favicon.ico": #判断path记录的路径是否为icon如果是尝试打开文件
            try: #尝试打开
                fobj=open(self.ico,"rb")
                content=fobj.read()
                fobj.close()
                clientTcp.send(b"HTTP/1.1 200 OK\r\ncontent-type:image/x-icon\r\n\r\n"+content)
                clientTcp.close()
            except: #没有icon文件打开失败
                clientTcp.send(b"HTTP/1.1 404 not find")
                clientTcp.close()
        elif self.staticType.find(os.path.splitext(requestUrl)[1])>-1 and os.path.splitext(requestUrl)[1]:
            #and前边是判断截取的路径的类型在初始化定义中存在
            print(1)
            if os.path.isdir(self.staticDir):
                fullpath=os.path.join(self.staticDir,requestUrl[1:])
                if os.path.isfile(fullpath):
                    fobj=open(fullpath,"rb")
                    con=fobj.read()
                    fobj.close()
                    clientTcp.send(("HTTP/1.1 200 OK\r\ncontent-type:"+self.mimeType[os.path.splitext(requestUrl)[1]]+";charset=utf-8\r\n\r\n").encode(encoding="utf8")+con)
                    clientTcp.close()
                else:
                    clientTcp.send(b"HTTP/1.1 404 not find")
                    clientTcp.close()
        else:
            # 用户发起请求
            self.route_handle(requestData,clientTcp)

    # 多线程处理客户端的请求
    def client_handle(self,clientTcp,clientInfo):
        requestData=clientTcp.recv(self.recvNum)
        # requestData为接收客户端传递过来的数据

        # 对每一个请求做处理的的时候，获得请求的信息，并且格式化
        # 实现具体的http协议
        self.request_handle(self.requestData_handle(requestData),clientTcp)
        #此时参数requestData_handle(requestData)经过格式化处理后，和参数clientTcp一起传递给request_handle方法去继续执行。
    # 创建tcp服务器
    def createTcp(self):
        socketTcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socketTcp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        socketTcp.bind((self.host,self.port))
        socketTcp.listen(self.listen)
        while True:
            clientTcp,clientInfo=socketTcp.accept()
            threading.Thread(target=self.client_handle,args=(clientTcp,clientInfo)).start()
            #线程里边传入俩个实际参数clientTcp,clientInfo分别为socket对象和地址信息。调用client_handle函数，并将参数传过去。
    # 启动函数
    def start(self,host="",port=8888,listen=512):
        self.host=host
        self.port=port
        self.listen=listen
        self.createTcp()
