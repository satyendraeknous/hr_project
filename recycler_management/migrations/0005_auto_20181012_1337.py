# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-12 08:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recycler_management', '0004_recyclermaster_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recyclermaster',
            name='recycler_zip',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hotel_management.Zip'),
        ),
    ]
