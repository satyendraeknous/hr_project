# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . models import RecyclerMaster

# Register your models here.



class RecyclerMasterAdmin(admin.ModelAdmin):
    model = RecyclerMaster
    list_display = ['user', 'recycler_id', 'recycler_name', 'recycler_address1', 'recycler_address2', 'recycler_city', 'recycler_zip', 'recycler_state', 'recycler_country', 'recycler_phone_no',]

admin.site.register(RecyclerMaster, RecyclerMasterAdmin)





