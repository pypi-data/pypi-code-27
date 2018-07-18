import socket,threading,re,os.path
from urllib.parse import  urlparse

class Server():
    def __init__(self):
        self.host = ""
        self.port = 2121
        self.listenNum = 512
        self.recvNum = 1024
        self.routeInfo = []
        self.staticDir = "static"
        self.staticType = ".jpg,.css,.js,.png,.html,.ico"
        self.mimeType = {".css":"text/css",".html":"text/html",".js":"application/x-javascript",".jpg":"application/x-jpg",".ico":"application/x-ico"}
        self.ico = "fish.ico"
        self.temDir = "template"

    #启动
    def start(self,host="",port=2121,listenNum=512):
        self.host = host
        self.port = int(port)
        self.listenNum = listenNum
        self.createSocket()   #调用创建tcp服务器方法

    #创建tcp服务器
    def createSocket(self):
        serverTCP = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #创建tcp协议
        serverTCP.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        serverTCP.bind((self.host,self.port))   #绑定IP和端口
        serverTCP.listen(self.listenNum)   #监听
        while True:
            clientTCP,clientInfo = serverTCP.accept()   #阻塞，等待客户端连接
            # print(str(self.port)+"端口连接成功！")
            threading.Thread(target=self.client_handle,args=(clientTCP,)).start()   #开启线程，并调用处理客户端请求的方法

    #多线程处理客户端的请求
    def client_handle(self,clientTCP):
        requestData = clientTCP.recv(self.recvNum).decode("utf8")   #接收客户端的请求
        #对请求的信息格式化
        requestData = self.requestData_handle(requestData)   #调用格式化请求的信息的方法，并接收格式化后的请求(字典类型)
        #对每一个请求做处理
        self.request_handle(requestData,clientTCP)   #调用处理请求的方法

    # 对请求的信息格式化
    def requestData_handle(self,requestData):
        requestData = requestData.splitlines()   #splitlines()按照行('\r','\r\n',\n')分隔，返回一个包含各行作为元素的列表
        urlInfo = requestData[0]   #取得列表中的第一个元素
        requestType = re.match(r"[^\s]+",urlInfo).group(0)   #查找请求方式
        # print(requestType)
        obj = {}   #创建一个字典对象，用来存放格式化后请求的信息
        obj["requestType"] = requestType   #存放请求方式到字典
        # 请求的路径、参数等
        url = urlparse(re.match(r"\w+\s+([^\s]*)", urlInfo).group(1)) #urlparse返回元组
        # print("url:", url)
        obj["path"] = url[2]   #存放请求的路径到字典
        obj["query"] = {}   #存放请求的问号(?)后参数到字典里
        if url[4]:
            for i in url[4].split("&"):
                obj["query"][i.split("=")[0]] = i.split("=")[1]
        # print('+++',obj)
        return obj

    # 处理请求
    def request_handle(self, clientData, clientTCP):
        url = clientData["path"]   #从字典里拿出请求的路径
        # ico处理
        if url == "/favicon.ico":
            try:
                f = open(self.ico, 'rb')
                icoInfo = f.read()
                f.close()
                clientTCP.send(b"HTTP/1.1 200 OK\r\ncontent-type:image/x-icon\r\n\r\n" + icoInfo)
            except:
                clientTCP.send(b"HTTP/1.1 404 NOT FIND\r\n")
            finally:
                clientTCP.close()
        # 静态文件处理
        # 首先，判断是否是请求静态处理文件，若os.path.splitext(url)[1]有值就是客户端请求静态文件
        # 最后，判断服务器是否有处理客户端请求静态文件类型的能力，所有能力在self.staticType中体现
        elif os.path.splitext(url)[1] and self.staticType.find(os.path.splitext(url)[1]) != -1:
            if os.path.isdir(self.staticDir):   #判断静态文件夹存在
                rootStatic = os.path.abspath(self.staticDir)   #得到静态文件夹的绝对路径
                fullPath = os.path.join(rootStatic, url[1:])   #将静态文件夹的绝对路径和请求的静态文件组合成完整的路径
                # print('===',fullPath)
                if os.path.isfile(fullPath):   #判断组合成的完整路径是否是文件形式存在
                    # print(fullPath)
                    f = open(fullPath, 'rb')
                    fileContent = f.read()   #读出请求的静态文件中的内容
                    f.close()
                    result = "HTTP/1.1 200 OK\r\ncontent-type:" + self.mimeType[os.path.splitext(url)[1]] + ";charset=utf-8\r\n\r\n"
                    clientTCP.send(bytes(result, encoding="utf8") + fileContent)   #响应客户端请求的信息
                    clientTCP.close()
                else:
                    clientTCP.send(b"HTTP/1.1 404 NOT FIND\r\n")
                    clientTCP.close()
            else:   #判断静态文件夹不存在
                clientTCP.send(b"HTTP/1.1 404 NOT FIND\r\n")
                clientTCP.close()
        # 动态处理
        else:
            self.route_handle(clientData,clientTCP)   #调用动态处理的函数（路由处理方法）

    #动态处理请求的路由
    def route_handle(self,clientData,clientTCP):
        # print(clientData) #{'requestType': 'GET', 'path': '/c/21', 'query': {}}
        # print(self.routeInfo)
        #[{'params': ['dd'], 'url': '/abc/(\\w+)', 'callback': <function fun at 0x00000000029FB950>, 'methods': ['GET']}, {'params': ['id1', 'id2'], 'url': '/a/(\\w+)/b/(\\w+)', 'callback': <function fun2 at 0x00000000029FB9D8>, 'methods': ['GET']}, {'params': ['id'], 'url': '/c/(\\w+)', 'callback': <function fun3 at 0x00000000029FBA60>, 'methods': ['GET']}]
        flag = True
        for i in self.routeInfo:   #self.routeInfo：用来存放路由信息的列表
            reg = re.compile(i["url"])   #构成正则表达式
            reResult = reg.match(clientData["path"])   #将reg正则表达式与客户端请求的路径进行匹配
            if reResult and i["methods"].count(clientData["requestType"])>0:   #匹配到且客户端请求的方式在服务器请求能力的范围内
                values = reg.findall(reResult.group(0))[0]   #根据reg正则表达式匹配客户端请求路径中的值，元组形式
                response = ''
                clientData["params"] = {}   #在字典clientData中，以params为键，以字典为值的键值对
                for j in range(len(i["params"])):   #i["params"][j]参数名，values[j]参数值
                    clientData["params"][i["params"][j]]=values[j]   #将参数名和参数值以字典的形式存放到字典clientData中
                response={}
                response["header"]={}
                response["header"]["po"] = "HTTP/1.1"
                response["header"]["status_code"] = "200 OK"
                response["header"]["content_type"] = "text/html;charset=utf-8"
                body = i["callback"](clientData,response)
                headerInfo = self.parse_header(response)
                clientTCP.send(headerInfo+body.encode("utf8"))
                clientTCP.close()
                flag = False
                break
        if flag:
            clientTCP.send(b"HTTP/1.1 404 NOT FIND\r\n\r\nnot find")
            clientTCP.close()

    #对响应头进行处理
    def parse_header(self,response):
        info = ''
        info += response["header"]["po"] + " " + response["header"]["status_code"] + "\r\n"
        info += "content-type:" + " " + response["header"]["content_type"] + "\r\n\r\n"
        return info.encode("utf8")

    #采集路由信息
    def route(self,url,methods=["GET"]):
        # print("---route---",url)
        def runRoute(callback):
            # print("---runRoute---")
            obj={}   #用来存放所有路由信息的字典
            obj["params"] = re.findall(r":([^/]+)",url)   #存放路由中的参数名
            obj["url"] = re.sub(r":([^/]+)","(\w+)",url)   #存放路由中url的正则表达式
            obj["callback"] = callback   #存放回调函数
            obj["methods"] = methods   #存放能请求的类型
            self.routeInfo.append(obj)   #追加到self.routeInfo列表中
            print('===',self.routeInfo)
        return runRoute


def template(url,data):
    tem = "template"
    url = os.path.join(os.path.abspath(tem),url)
    f = open(url,'r')
    con = f.read()
    f.close()
    # print(con)
    con = re.sub(r"\n","",con)
    # print(con)
    reObj = re.compile(r'((?=){{\w+}}(?=))')  #生成正则对象
    # print(reObj)
    def fn(a):
        # print("a：",a)
        return "'+"+a.group(0)[2:-2]+"+'"
    con = reObj.sub(fn,con)
    # print("con:",con)
    result = eval("'+"+con+"+'", data) #将字符串当成有效的表达式来求值并返回计算结果
    # print('==>',result)
    return result[1:-1]

