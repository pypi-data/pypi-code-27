# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navsy', '0003_page_sitemap'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='seo_description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='seo_keywords',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='seo_title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
