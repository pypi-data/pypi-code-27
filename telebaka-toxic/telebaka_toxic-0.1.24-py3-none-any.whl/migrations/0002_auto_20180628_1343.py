# Generated by Django 2.0.5 on 2018-06-28 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telebaka_toxic', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='string',
            old_name='max_rating',
            new_name='min_rating',
        ),
        migrations.AlterField(
            model_name='string',
            name='text',
            field=models.TextField(help_text='Placeholders: `{warned_link}`, `{warned_rating}`, `{warner_link}`, `{warner_rating}`'),
        ),
    ]
