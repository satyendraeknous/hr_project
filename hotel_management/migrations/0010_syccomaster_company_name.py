# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-10 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_management', '0009_syccoprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='syccomaster',
            name='company_name',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
    ]
