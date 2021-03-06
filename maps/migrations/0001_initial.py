# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 00:22
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DHS_cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255, null=True)),
                ('data_year', models.CharField(max_length=255, null=True)),
                ('dhs_wealth_idx', models.DecimalField(decimal_places=10, max_digits=15)),
                ('latitude', models.DecimalField(decimal_places=10, max_digits=15, null=True)),
                ('longitude', models.DecimalField(decimal_places=10, max_digits=15, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('predicted_wealth_idx', models.DecimalField(decimal_places=10, max_digits=15)),
                ('wealth_decile', models.IntegerField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326)),
            ],
        ),
    ]
