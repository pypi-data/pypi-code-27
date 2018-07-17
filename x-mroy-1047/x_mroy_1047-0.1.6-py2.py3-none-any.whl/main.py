
#!/usr/bin/python
## write by qingluan
# just a run file

import tornado.ioloop
import os
from tornado.ioloop import IOLoop
from web.setting import  appication, port
from qlib.io import GeneratorApi


def main():
    args = GeneratorApi({
        'port':"set port ",
        'test':"test shadowsocks auto in backgend [start/stop]",
        })
    if args.test == 'start':
        os.popen("x-sstest start")
    elif args.test == "stop":
        os.popen("x-sstest stop")
    
    if args.port:
        os.popen("m-asyncs start")
        port = int(args.port)
        appication.listen(port)
        tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
