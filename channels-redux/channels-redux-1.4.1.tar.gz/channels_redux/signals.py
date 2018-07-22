from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels_redux.notify import NotifyConsumer, NotifierMixin


@receiver(post_save, dispatch_uid="channels_redux.signals.object_saved")
def object_saved(sender, instance: NotifierMixin, created, **kwargs):
    if not isinstance(instance, NotifierMixin):
        return
    if created:
        NotifyConsumer.object_created(instance)
    else:
        NotifyConsumer.object_updated(instance)


@receiver(post_delete, dispatch_uid="channels_redux.signals.object_deleted")
def object_deleted(sender, instance: NotifierMixin, **kwargs):
    if not isinstance(instance, NotifierMixin):
        return
    NotifyConsumer.object_deleted(instance)
