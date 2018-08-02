# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0018_auto_20180118_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='payment_key',
            field=models.CharField(max_length=7, null=True, blank=True),
            preserve_default=True,
        ),
    ]
