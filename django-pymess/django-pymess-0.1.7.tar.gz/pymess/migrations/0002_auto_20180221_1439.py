# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-02-21 13:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields

from pymess.config import settings


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pymess', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='changed at')),
                ('file', models.FileField(upload_to='pymess/emails', verbose_name='file')),
                ('content_type', models.CharField(verbose_name='content type', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'attachments',
                'verbose_name': 'attachment',
            },
        ),
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='changed at')),
                ('sent_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='sent at')),
                ('recipient', models.EmailField(max_length=254, verbose_name='recipient')),
                ('sender', models.EmailField(max_length=254, verbose_name='sender')),
                ('sender_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='sender name')),
                ('subject', models.TextField(verbose_name='subject')),
                ('content', models.TextField(verbose_name='content')),
                ('template_slug',
                 models.SlugField(blank=True, editable=False, max_length=100, null=True, verbose_name='slug')),
                ('state',
                 models.IntegerField(choices=[(1, 'waiting'), (2, 'sending'), (3, 'sent'), (4, 'error'), (5, 'debug')],
                                     editable=False, verbose_name='state')),
                ('backend', models.CharField(blank=True, editable=False, null=True, verbose_name='backend',
                                             max_length=250)),
                ('error', models.TextField(blank=True, editable=False, null=True, verbose_name='error')),
                ('extra_data',
                 jsonfield.fields.JSONField(blank=True, editable=False, null=True, verbose_name='extra data')),
                ('extra_sender_data',
                 jsonfield.fields.JSONField(blank=True, editable=False, null=True, verbose_name='extra sender data')),
                ('tag', models.SlugField(blank=True, editable=False, null=True, verbose_name='tag')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'e-mail message',
                'verbose_name_plural': 'e-mail messages'
            }
        ),
        migrations.CreateModel(
            name='EmailRelatedObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='changed at')),
                ('object_id', models.TextField(verbose_name='ID of the related object')),
                ('object_id_int', models.PositiveIntegerField(db_index=True, blank=True, null=True,
                                                              verbose_name='ID of the related object in int format')),
                ('content_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType',
                                   verbose_name='content type of the related object')),
                ('email_message',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_objects',
                                   to='pymess.EmailMessage', verbose_name='e-mail message')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'related object of a e-mail message',
                'verbose_name_plural': 'related objects of e-mail messages',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='changed at')),
                ('slug', models.SlugField(editable=False, max_length=100, verbose_name='slug')),
                ('sender', models.EmailField(blank=True, max_length=200, null=True, verbose_name='sender')),
                ('sender_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='sender name')),
                ('body', models.TextField(null=True, verbose_name='message body')),
                ('subject', models.TextField(verbose_name='subject')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name_plural': 'e-mail templates',
                'verbose_name': 'e-mail template',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutputSMSMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='changed at')),
                ('sent_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='sent at')),
                ('sender', models.CharField(blank=True, max_length=20, null=True, verbose_name='sender')),
                ('recipient', models.CharField(max_length=20, verbose_name='recipient')),
                ('content', models.TextField(max_length=700, verbose_name='content')),
                ('template_slug',
                 models.SlugField(blank=True, editable=False, max_length=100, null=True, verbose_name='slug')),
                ('state', models.IntegerField(
                    choices=[(1, 'waiting'), (2, 'unknown'), (3, 'sending'), (4, 'sent'), (5, 'error'), (6, 'debug'),
                             (7, 'delivered')], editable=False, verbose_name='state')),
                ('backend', models.CharField(blank=True, editable=False, null=True, verbose_name='backend',
                                             max_length=250)),
                ('error', models.TextField(blank=True, editable=False, null=True, verbose_name='error')),
                ('extra_data',
                 jsonfield.fields.JSONField(blank=True, editable=False, null=True, verbose_name='extra data')),
                ('extra_sender_data',
                 jsonfield.fields.JSONField(blank=True, editable=False, null=True, verbose_name='extra sender data')),
                ('tag', models.SlugField(blank=True, editable=False, null=True, verbose_name='tag')),
            ],
            options={
                'verbose_name_plural': 'output SMS',
                'verbose_name': 'output SMS',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OutputSMSRelatedObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='changed at')),
                ('object_id', models.TextField(verbose_name='ID of the related object')),
                ('object_id_int', models.PositiveIntegerField(db_index=True, blank=True, null=True,
                                                              verbose_name='ID of the related object in int format')),
                ('content_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType',
                                   verbose_name='content type of the related object')),
                ('output_sms_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                         related_name='related_objects', to='pymess.OutputSMSMessage',
                                                         verbose_name='output SMS message')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'related object of a SMS message',
                'verbose_name_plural': 'related objects of SMS messages',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SMSTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='changed at')),
                ('slug', models.SlugField(editable=False, max_length=100, verbose_name='slug')),
                ('body', models.TextField(null=True, verbose_name='message body')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name_plural': 'SMS templates',
                'verbose_name': 'SMS template',
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='userdevice',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserDevice',
        ),
        migrations.AddField(
            model_name='outputsmsmessage',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='output_sms_messages', to=settings.SMS_TEMPLATE_MODEL,
                                    verbose_name='template'),
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='email_messages', to=settings.EMAIL_TEMPLATE_MODEL,
                                    verbose_name='template'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='email_message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments',
                                    to='pymess.EmailMessage', verbose_name='e-mail message'),
        ),
    ]
