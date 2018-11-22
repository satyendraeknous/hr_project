# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . models import *

# Register your models here.



class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ['user', 'phone_no', 'company',]
admin.site.register(UserProfile, UserProfileAdmin)






class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display = ['country_id', 'country_name',]

admin.site.register(Country, CountryAdmin)


class StateAdmin(admin.ModelAdmin):
    model = State
    list_display = ['state_id', 'state_name',]

admin.site.register(State, StateAdmin)



class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ['city_id', 'city_name',]

admin.site.register(City, CityAdmin)



class ZipAdmin(admin.ModelAdmin):
    model = Zip
    list_display = ['zip_id', 'zip',]

admin.site.register(Zip, ZipAdmin)


class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['brand_id', 'brand_name',]

admin.site.register(Brand, BrandAdmin)


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['category_id', 'category_name',]

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['product_id', 'product_name',]

admin.site.register(Product, ProductAdmin)


class HotelMasterAdmin(admin.ModelAdmin):
    model = HotelMaster
    list_display = ['hotel_id', 'hotel_name', 'hotel_address1', 'hotel_address2', 'hotel_city', 'hotel_zip', 'hotel_state', 'hotel_country', 'hotel_brand', 'hotel_phone_no',]

admin.site.register(HotelMaster, HotelMasterAdmin)


class LoadDashboardAdmin(admin.ModelAdmin):
    model = LoadDashboard
    list_display = ['load_no', 'hotel_id', 'user_id',  'date_and_time', 
                    'contact_details', 'product', 'category', 'no_of_bags', 'weight', 'status',  'pickup_date',
                     'actual_no_of_bags', 'actual_weight', 'green_point_hotel', 'green_point_recycler', 'remarks',]

admin.site.register(LoadDashboard, LoadDashboardAdmin)


class RemarkAdmin(admin.ModelAdmin):
    model = Remark
    list_display = ['load_remark', 'user', 'comment', 'date',]
admin.site.register(Remark, RemarkAdmin)












# class SyccoMasterAdmin(admin.ModelAdmin):
#     model = SyccoMaster
#     list_display = ['user', 'company_name', 'weight', 'green_point', 'amount', 'total_greenpoint', 'total_amount']

# admin.site.register(SyccoMaster, SyccoMasterAdmin)


# class SyccoProfileAdmin(admin.ModelAdmin):
#     model = SyccoProfile
#     list_display = ['user', 'address1', 'address2', 'city', 'zip', 'state', 'country', 'phone_no',]

# admin.site.register(SyccoProfile, SyccoProfileAdmin)



