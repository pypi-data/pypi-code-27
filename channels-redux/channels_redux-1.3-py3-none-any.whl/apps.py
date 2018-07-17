from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

from channels_redux.notify import NotifierMixin, NotifyConsumer


class ChannelsReduxConfig(AppConfig):
    name = 'channels_redux'

    def ready(self):
        def object_saved(sender, instance: NotifierMixin, created, **kwargs):
            if created:
                NotifyConsumer.object_created(instance)
            else:
                NotifyConsumer.object_updated(instance)
        post_save.connect(object_saved, NotifierMixin, weak=False)

        def object_deleted(sender, instance: NotifierMixin, **kwargs):
            NotifyConsumer.object_deleted(instance)
        post_delete.connect(object_deleted, NotifierMixin, weak=False)

        super(ChannelsReduxConfig, self).ready()
