# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-18 01:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0004_auto_20170714_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermailer',
            name='label',
            field=models.CharField(max_length=128, unique=True, verbose_name='Label'),
        ),
    ]
