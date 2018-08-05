import json


def read_json_payload(s):
    data = s.recv(1024)
    dataList = data.decode().split('\n')
    for data in dataList:
        try:
            pdata = json.loads(data)
            return pdata
        except json.decoder.JSONDecodeError:
            pass
