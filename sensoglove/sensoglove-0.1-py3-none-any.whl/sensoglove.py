import sys
import socket
from .hand import Hand

from .helpers import read_json_payload


class SensoGlove:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hand = None
        self.src = None
        self.name = None
        self.battery = None
        self.temperature = None

    def _init_header_props(self):
        data = None
        while data is None:
            data = read_json_payload(self.socket)
            self.src = data['src']
            self.name = data['name']

    def connect(self):
        self.socket.settimeout(5)
        try:
            self.socket.connect((self.host, self.port))
            self._init_header_props()
        except Exception as err:
            print('Socket connection failed with %s:%d.' % (self.host, self.port))
            raise

    def fetch_data(self):
        data = read_json_payload(self.socket)
        if data is None:
            return
        self.type = data['type']
        if self.type != 'position':
            return
        self.battery = data['data']['battery']
        self.hand = Hand(data)
        self.temperature = data['data']['temperature']

    def send_vibration(self, fingers=[], duration=655, strength=9):
        for finger in fingers:
            payload = '{"dst": "%s","type": "vibration","data": {"type": "%s","dur": %s, "str": %s}}\n' % (self.src, finger, duration, strength)
            payload = payload.encode('utf-8')
            self.socket.send(payload)
