# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0009_auto_20170624_0613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankrule',
            name='max_duration_beats',
        ),
        migrations.AddField(
            model_name='bankrule',
            name='max_duration',
            field=models.IntegerField(null=True),
        ),
    ]
