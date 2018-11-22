# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . models import SyccoProfile, SyccoMaster, SyccoHRtable

# Register your models here.



class SyccoMasterAdmin(admin.ModelAdmin):
    model = SyccoMaster
    list_display = ['user', 'company_name', 'weight', 'green_point', 'amount', 'total_greenpoint', 'total_amount']

admin.site.register(SyccoMaster, SyccoMasterAdmin)


class SyccoProfileAdmin(admin.ModelAdmin):
    model = SyccoProfile
    list_display = ['user', 'address1', 'address2', 'city', 'zip', 'state', 'country', 'phone_no',]

admin.site.register(SyccoProfile, SyccoProfileAdmin)


class SyccoHRtableAdmin(admin.ModelAdmin):
    model = SyccoHRtable
    list_display = ['user', 'hotel_name', 'recycler_name',]

admin.site.register(SyccoHRtable, SyccoHRtableAdmin)


