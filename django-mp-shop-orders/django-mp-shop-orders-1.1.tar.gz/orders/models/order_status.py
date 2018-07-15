
from django.db import models
from django.utils.translation import ugettext_lazy as _


class OrderStatusName(models.CharField):

    def __init__(
            self,
            verbose_name=_('Name'),
            max_length=255,
            *args, **kwargs):

        super(OrderStatusName, self).__init__(
            verbose_name=verbose_name,
            max_length=max_length,
            *args,
            **kwargs)


class OrderStatusCode(models.CharField):

    def __init__(
            self,
            verbose_name=_('Code'),
            max_length=255,
            unique=True,
            *args, **kwargs):

        super(OrderStatusCode, self).__init__(
            verbose_name=verbose_name,
            max_length=max_length,
            unique=unique,
            *args, **kwargs)


class OrderStatusDescription(models.TextField):

    def __init__(
            self,
            verbose_name=_('Description'),
            max_length=1000,
            blank=True,
            *args, **kwargs):

        super(OrderStatusDescription, self).__init__(
            verbose_name=verbose_name,
            max_length=max_length,
            blank=blank,
            *args, **kwargs)


class AbstractOrderStatus(models.Model):

    name = OrderStatusName()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = _('Order status')
        verbose_name_plural = _('Order statuses')
