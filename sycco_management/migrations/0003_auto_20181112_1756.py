# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-12 12:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sycco_management', '0002_syccohrtable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='syccohrtable',
            old_name='hotelsycco_name',
            new_name='hotel_name',
        ),
        migrations.RenameField(
            model_name='syccohrtable',
            old_name='recyclersyco_name',
            new_name='recycler_name',
        ),
    ]
