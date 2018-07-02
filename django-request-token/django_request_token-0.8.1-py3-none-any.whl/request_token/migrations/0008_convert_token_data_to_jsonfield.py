# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-27 14:23
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request_token', '0007_add_client_ipv6'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requesttoken',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, help_text='Custom data add to the token, but not encoded (must be fetched from DB).', null=True),
        ),
        migrations.AlterField(
            model_name='requesttokenlog',
            name='token',
            field=models.ForeignKey(help_text='The RequestToken that was used.', on_delete=models.deletion.CASCADE, related_name='logs', to='request_token.RequestToken'),
        ),
    ]
