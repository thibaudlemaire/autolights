# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 00:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0014_auto_20170624_0825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='modification',
        ),
        migrations.AddField(
            model_name='configuration',
            name='active',
            field=models.BooleanField(default=True, unique=True),
            preserve_default=False,
        ),
    ]
