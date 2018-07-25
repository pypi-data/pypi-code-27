
from django.db import models
from django.template import Template
from django.utils.translation import ugettext_lazy as _


class PageMeta(models.Model):

    META_ROBOTS_CHOICES = (
        ('index, follow', _('Index, Follow')),
        ('noindex, nofollow', _('No Index, No Follow')),
        ('index, nofollow', _('Index, No Follow')),
        ('noindex, follow', _('No Index, Follow')),
    )

    FIELDS_FOR_RENDERING = [
        'title', 'keywords', 'description', 'breadcrumb', 'header']

    url = models.CharField(
        _('URL'), max_length=255, blank=False, unique=True, db_index=True)

    title = models.CharField(_('Title'), max_length=68, blank=False)

    keywords = models.CharField(_('Keywords'), max_length=100, blank=True)

    description = models.CharField(
        _('Description'), max_length=155, blank=True)

    breadcrumb = models.CharField(_('Breadcrumb'), max_length=100, blank=True)

    header = models.CharField(_('Header'), max_length=100, blank=True)

    robots = models.CharField(
        _('Robots'), max_length=30, blank=True, default='index, follow',
        choices=META_ROBOTS_CHOICES)

    def render(self, context):

        for field in self.FIELDS_FOR_RENDERING:

            value = Template(getattr(self, field)).render(context)

            setattr(self, 'printable_' + field, value)

    def __str__(self):
        return '{} - {}'.format(self.url, self.title)

    class Meta:
        verbose_name = _('Page meta')
        verbose_name_plural = _('Pages meta')
