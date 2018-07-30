import pysher
import sys
import time
# Add a logging handler so we can see the raw communication data
import logging
from django.conf import settings


root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)


class PysherApplication(object):
    appkey = settings.PUSHER_APP_KEY or ''
    secret = settings.PUSHER_SECRET or ''
    cluster = settings.PUSHER_CLUSTER or ''
    secure = settings.PUSHER_SECURE 

    def __init__(self):
        self.client = pysher.Pusher(key=self.appkey, secret=self.secret, cluster=self.cluster, secure=self.secure)


    def prepare_event(self, channel_name, event_name, function):
        def connect_handler(data):
            channel = self.client.subscribe(channel_name)
            channel.bind(event_name, function)

        self.client.connection.bind('pusher:connection_established', connect_handler)


    def prepare_events(self):
        self._autodiscover_events()
        from dj_pysher.tools import events
        for event in events:
            self.prepare_event(
                event['channel_name'],
                event['event_name'],
                event['function']
            )

        self.client.connect()

    def _autodiscover_events(self):
        for package in (lambda: settings.INSTALLED_APPS)():
            try:
                exec('from {}.events import *'.format(package))
                print('Loaded {}'.format(package))
            except Exception as ex:
                print(ex)



    def main(self):
        self.prepare_events()
        while True:
            # Do other things in the meantime here...
            time.sleep(1)