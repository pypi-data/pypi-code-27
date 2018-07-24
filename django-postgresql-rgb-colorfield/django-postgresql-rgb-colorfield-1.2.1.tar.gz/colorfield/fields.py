from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
import webcolors
from django import forms
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


class ColorWidget(forms.Widget):
    class Media:
        if settings.DEBUG:
            js = ['colorfield/jscolor.js']
        else:
            js = ['colorfield/jscolor.min.js']

    def render(self, name, value, attrs=None):
        is_required = self.is_required
        return render_to_string('colorfield/color.html', locals())

    def value_from_datadict(self, data, files, name):
        val = data[name]
        if val:
            hex_val = '#' + data[name]
            logger.critical("hex: {}".format(hex_val))
            color = webcolors.hex_to_rgb(hex_val)
            return [color.red, color.green, color.blue]
        else:
            return []


class ColorField(ArrayField):

    def __init__(self, base_field=None, size=3, **kwargs):
        size = 3
        base_field = models.PositiveSmallIntegerField(validators=[MaxValueValidator(255), MinValueValidator(0)])
        super().__init__(base_field, size=size, **kwargs)


    @property
    def description(self):
        return 'Array of RGB Colors'


    def formfield(self, **kwargs):
        kwargs['widget'] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)
