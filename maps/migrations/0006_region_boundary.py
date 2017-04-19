# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 23:43
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0005_auto_20170418_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='boundary',
            field=django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326),
        ),
    ]
