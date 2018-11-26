# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.contrib.auth.models import User 
from datetime import datetime
from decimal import Decimal


# Create your models here.

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.country_name)


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=150)
    #country = models.ForeignKey(Country)

    def __str__(self):
        return str(self.state_name)


class City(models.Model): 
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=150)
    #state = models.ForeignKey(State)

    def __str__(self):
        return str(self.city_name)


class Zip(models.Model):
    zip_id = models.AutoField(primary_key=True)
    zip = models.IntegerField()
    #city = models.ForeignKey(City)

    def __str__(self):
        return str(self.zip)



class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.category_name)


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=150)
    #category = models.ForeignKey(Category)

    def __str__(self):
        return str(self.product_name)


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.brand_name)


class HotelMaster(models.Model): 
    hotel_id = models.AutoField(primary_key=True)
    hotel_name = models.CharField(max_length=150)
    hotel_address1 = models.CharField(max_length=150)
    hotel_address2 = models.CharField(max_length=150)
    hotel_city = models.ForeignKey(City, on_delete=models.CASCADE)
    hotel_zip = models.ForeignKey(Zip, on_delete=models.CASCADE)
    hotel_state = models.ForeignKey(State, on_delete=models.CASCADE)
    hotel_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    hotel_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    hotel_phone_no = models.IntegerField()

    def __str__(self):
        return str(self.hotel_name)


class LoadDashboard(models.Model): 
    load_no = models.AutoField(primary_key=True)
    hotel_id = models.ForeignKey(HotelMaster, on_delete=models.CASCADE)
    #recycler_id = models.ForeignKey(RecyclerMaster)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField(default=datetime.now)
    contact_details = models.PositiveIntegerField()
    status = models.CharField(max_length=150, default="Processing")
    pickup_date = models.DateField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    no_of_bags = models.PositiveIntegerField(blank=True, null=True)
    #weight = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True )

    actual_no_of_bags = models.PositiveIntegerField(blank=True, null=True)
    actual_weight = models.PositiveIntegerField(blank=True, null=True)
    green_point_hotel = models.PositiveIntegerField(blank=True, null=True)
    green_point_recycler = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.TextField(max_length=524, blank=True, null=True)

    def __str__(self):
        return str(self.load_no)


class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.IntegerField()
    company = models.CharField(max_length=150)
    group = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.user)


class Remark(models.Model):
    load_remark = models.ForeignKey(LoadDashboard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)











# class SyccoMaster(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=250)
#     weight = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#     green_point = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#     amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#     total_greenpoint = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#     total_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)



# class SyccoProfile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     address1 = models.CharField(max_length=150)
#     address2 = models.CharField(max_length=150)
#     city = models.ForeignKey(City)
#     zip = models.ForeignKey(Zip)
#     state = models.ForeignKey(State)
#     country = models.ForeignKey(Country)
#     phone_no = models.IntegerField()

#     def __str__(self):
#         return str(self.user)

