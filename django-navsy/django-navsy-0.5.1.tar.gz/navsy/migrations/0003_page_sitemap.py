# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navsy', '0002_route_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='sitemap_changefreq',
            field=models.CharField(blank=True, choices=[
                    ('always', 'always'),
                    ('hourly', 'hourly'),
                    ('daily', 'daily'),
                    ('weekly', 'weekly'),
                    ('monthly', 'monthly'),
                    ('yearly', 'yearly'),
                    ('never', 'never')
                ], default='never', max_length=50),
        ),
        migrations.AddField(
            model_name='page',
            name='sitemap_item',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='page',
            name='sitemap_priority',
            field=models.CharField(blank=True, choices=[
                    ('0.0', '0.0'),
                    ('0.1', '0.1'),
                    ('0.2', '0.2'),
                    ('0.3', '0.3'),
                    ('0.4', '0.4'),
                    ('0.5', '0.5'),
                    ('0.6', '0.6'),
                    ('0.7', '0.7'),
                    ('0.8', '0.8'),
                    ('0.9', '0.9'),
                    ('1.0', '1.0')
                ], default='0.5', max_length=5),
        ),
    ]
