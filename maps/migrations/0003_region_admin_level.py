# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 23:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0002_auto_20170424_0426'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='admin_level',
            field=models.IntegerField(null=True),
        ),
    ]
