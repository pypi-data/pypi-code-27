# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onfido', '0004_auto_20161023_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='user',
        ),
    ]
