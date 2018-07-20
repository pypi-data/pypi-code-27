# coding=utf-8

import time


def test_ws_client(ep):
    from poco.utils.simplerpc.transport.ws.main import WebSocketClient
    from poco.utils.simplerpc.rpcclient import RpcClient
    conn = WebSocketClient(ep)
    client = RpcClient(conn)
    client.connect()

    for i in range(1000):
        client.call("getSDKVersion")
        time.sleep(1)


if __name__ == '__main__':
    test_ws_client('ws://10.252.61.62:15003')
    while True:
        time.sleep(5)
