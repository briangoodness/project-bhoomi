# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-11 17:10
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0004_cell_prediction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region_Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255, null=True)),
                ('admin_level', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('predicted_wealth_idx', models.DecimalField(decimal_places=10, max_digits=15)),
                ('wealth_decile', models.IntegerField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
        ),
    ]
