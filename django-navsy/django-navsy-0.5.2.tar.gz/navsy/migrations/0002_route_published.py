# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navsy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]
