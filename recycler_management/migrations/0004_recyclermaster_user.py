# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-08 06:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recycler_management', '0003_remove_recyclermaster_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='recyclermaster',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
