import socket
import ssl
import pprint


class ssl_WsClient():
    def __init__(self, ip, port, para, token=' '):
        self.ip = str(ip)
        self.port = int(port)
        self.f = open('log.txt', 'w')

        if token != ' ':
            para = eval(para)
            para['token'] = str(token)
            para = str(para)
        self.para = para.encode()

    def connect(self):
        while True:
            try:
                print('连接中')
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                self.ssl_sock = ssl.wrap_socket(sock,
                                                ca_certs="server.crt",
                                                cert_reqs=ssl.CERT_REQUIRED)

                self.ssl_sock.connect((self.ip, self.port))
                print('连接成功')

                self.ssl_sock.sendall(self.para)
                return
            except BaseException as e:
                print(e)
                continue


    def run(self):
        self.connect()
        self.ssl_sock.settimeout(120)
        while True:
            try:
                msg_len = int(self.ssl_sock.recv(4))
                msg = self.ssl_sock.recv(msg_len)
                msg = msg.decode()
                self.handle_msg(msg)
            except:
                self.connect()
                self.f.write('重连\n')
                continue


    def ssl_info(self):
        pprint.pprint(self.ssl_sock.getpeercert())


if __name__ == '__main__':
    ws = ssl_WsClient('gw.blueye.info', 5003, '{"event":"quote","content":"sub_huobi_$symbol_ticker"}', ' ')
    for data in ws.run():
        print(data)