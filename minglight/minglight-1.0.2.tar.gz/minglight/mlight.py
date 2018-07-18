import threading
import socket
import re
import os.path
from urllib.parse import urlparse  #解析地址，将地址信息按类分开
from .tm import render_template

class light():
    def __init__(self):
        self.host = ''
        self.port = 8888
        self.listen = 512
        self.recvNum=1024
        self.routeInfo=[]
        self.rootdir='static'
        self.ico='1.ico'
        self.type=".jpg,.png,.css,.html,.js,.ico"
        self.MimeType={'.jpg':'image/jpeg','.png':'image/png','.css':'text/css','.html':'text/html','.js':'application/x-javascript','.icon':'image/x-icon'}
    def route(self,url,methods):
        def run(callback):
            self.flag=0
            obj={}
            obj['param']=re.findall(r':([^/]+)',url) #保存所有冒号后面的id名
            obj['url']=re.sub(r':[^/]+','(\w+)',url) #将route函数参入的地址进行标准化并保存
            obj['callback']=callback
            obj['methods']=methods
            self.routeInfo.append(obj)
        return run
    #处理静态文件
    def static_handle(self,requestDate,client):
        url=requestDate['path']
        realpath = os.path.join(self.rootdir, url[1:])
        if os.path.isfile(realpath):
            source = open(realpath, 'rb')
            content = source.read()
            source.close()
            client.send(b'http/1.1 200 ok\r\ncontent-type:' + (self.MimeType[
                os.path.splitext(url)[1]] + '\r\n\r\n').encode('utf8') + content)
            client.close()
        else:
            client.send(b'http/1.1 404 not find')
            client.close()
    #处理动态文件
    def route_handle(self,requestData,clientTCP):
        flag = True
        for item in self.routeInfo:
            reg=item['url']
            url=requestData['path']
            result = re.match(r'%s'%(reg),url)
            if result and (requestData['type'] in item['methods']): #地址栏和route函数的参数进行匹配
                #保存地址栏中的每个id值：requestData['id'] = aa,requestData['id1'] = bb
                for i in range(len(item['param'])):
                    requestData['params'][item['param'][i]]=result.group(i+1)
                flag=False
                #向服务器传送callback返回的数据
                responseData={}
                responseData['headers']={}
                responseData['headers']['pool']='http/1.1'
                responseData['headers']['status_code'] = '200 ok'
                responseData['headers']['content-type'] = 'text/html;charset=utf-8'
                headers=responseData['headers']['pool']+" "+responseData['headers']['status_code']+"\r\ncontent-type:"+responseData['headers']['content-type']+"\r\n\r\n"
                content=item['callback'](requestData,responseData)
                clientTCP.send((headers+content).encode('utf8'))
                clientTCP.close()
        if flag:
            clientTCP.send(
                b"HTTP /1.1 404 NOT FIND\r\ncontent-type:text/html;charset=utf-8\r\n\r\nthis page is not find")
            clientTCP.close()
    #处理客户端返回的数据
    def requestData_handle(self, clientData):
        url=re.match(r'\w+\s+(/[^\s]*)', clientData).group(1) #接收到的地址
        parseResult=urlparse(url)  #将地址按类分开，返回元组
        urlObj={}  #创建request请求对象
        urlObj['params']={} #保存每个变量id对应的值
        urlObj['path'] = parseResult[2]  #保存路径
        urlObj['type'] = re.match(r'[^\s]+',clientData).group(0) #保存传输类型get/post
        urlObj['args']={} #保存地址栏的参数
        if parseResult[4]:
            arr=parseResult[4].split('&')
            for item in arr:
                arr1=item.split('=')
                urlObj['args'][arr1[0]] = arr1[1]
        return urlObj
    #接收客户端数据，并返回
    def receive_handle(self,clientTCP,address):
        try:
            clientDate = clientTCP.recv(self.recvNum).decode('utf8').splitlines()[0]
        except:
            pass
        else:
            requestData=self.requestData_handle(clientDate) #处理后的客户端请求数据，字典格式
            url=requestData['path']
        #处理图标
            if url == '/favicon.ico':
                realpath = os.path.join(self.rootdir,self.ico)
                if os.path.isfile(realpath):
                    source = open(realpath, 'rb')  # 考虑到.ico的文件必须以rb形式才能读取到
                    content = source.read()
                    source.close()
                    clientTCP.send(
                    b'http/1.1 200 ok\r\ncontent-type:image/x-icon\r\n\r\n'+content)
                    clientTCP.close()
                else:
                    clientTCP.send(b'http/1.1 404 not find')
                    clientTCP.close()
            elif url != '/favicon.ico':
                end = os.path.splitext(url)[1]  # 后缀名
                #静态
                if self.type.find(end) > -1 and end: #如果后缀名存在且在该类的可处理范围内
                    self.static_handle(requestData,clientTCP)
                #动态
                else:
                    self.route_handle(requestData,clientTCP)
    #创建客户端
    def makeServer(self):
        serverTCP=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverTCP.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        serverTCP.bind((self.host,self.port))
        serverTCP.listen(self.listen)
        while True:
            clientTCP,clientAddress=serverTCP.accept()
            obj=threading.Thread(target=self.receive_handle, args=(clientTCP,clientAddress))
            obj.start()
    def start(self,host='', port=8888, listen=512):
        self.host=host
        self.port=port
        self.listen=listen
        self.makeServer()

def template(url,data):
    resource=open('templates/'+url,'r')
    content=resource.read()
    resource.close()
    content=re.sub(r'\n','',content)  #将所有空格去除
    reg=re.compile(r'(?<=){{\w+}}(?=)')
    def fn(a):
        return "'+"+str(a.group(0)[2:-2])+"+'"  #a是从content中匹配到reg的每一个字符串
    content=reg.sub(fn,content)
    return eval("'"+content+"'",data)  #将字符串当做命令去执行
app=light()
@app.route('/aaa/:id2',methods=['POST','GET'])
def aa(req,res):
    return render_template('templates/1.html',{"name":"zhangsan","age":"15",'arr':[1,2,3,4,5]})

@app.route('/bbb/:id/:id1',methods=['POST','GET'])
def bb(req,res):
    print(req['params'])
    return template('1.html',{"place":"beijing"})

@app.route('/ccc/:id',methods=['POST','GET'])
def cc(req,res):
    print(res['headers'])
    return '头信息'

app.start(host='',port=8080)
