# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-25 12:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_management', '0018_auto_20181025_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remark',
            name='load_remark',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_management.LoadDashboard'),
        ),
    ]
