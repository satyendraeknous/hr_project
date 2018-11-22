# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-10 08:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotel_management', '0008_syccomaster_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyccoProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=150)),
                ('address2', models.CharField(max_length=150)),
                ('phone_no', models.IntegerField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_management.City')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_management.Country')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_management.State')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('zip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_management.Zip')),
            ],
        ),
    ]