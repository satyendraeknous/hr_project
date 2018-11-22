# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-03 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_management', '0005_auto_20181003_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loaddashboard',
            name='actual_weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='loaddashboard',
            name='green_point_hotel',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='loaddashboard',
            name='green_point_recycler',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='loaddashboard',
            name='no_of_bags',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loaddashboard',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
