from django.apps import AppConfig


class ChannelsReduxConfig(AppConfig):
    name = 'channels_redux'

    def ready(self):
        from channels_redux import signals
        super(ChannelsReduxConfig, self).ready()
