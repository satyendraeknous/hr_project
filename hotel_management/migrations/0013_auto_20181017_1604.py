# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-17 10:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_management', '0012_auto_20181017_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loaddashboard',
            name='pickup_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
