from pusher import pusher
from django.conf import settings


class SenderApplication(object):
    app_id = settings.PUSHER_APP_ID or ''
    appkey = settings.PUSHER_APP_KEY or ''
    secret = settings.PUSHER_SECRET or ''
    cluster = settings.PUSHER_CLUSTER or ''
    secure = settings.PUSHER_SECURE 

    def __init__(self):
        """
        Construtor
        :param channel: Canal
        :param event: Evento
        :param data: Dicionario
        """
        self.client = pusher.Pusher(
            app_id=self.app_id,
            key=self.appkey,
            secret=self.secret,
            cluster=self.cluster,
            ssl=self.secure
        )

    def send(self, channel, event, data):
        self.client.trigger(channel, event, data)

    def set_channel(self, channel):
        def func(self, event, data):
            self.client.trigger(channel, event, data)

        return func
