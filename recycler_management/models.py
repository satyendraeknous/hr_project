# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from hotel_management.models import City, Zip, State, Country

# Create your models here.


class RecyclerMaster(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recycler_id = models.AutoField(primary_key=True)
    recycler_name = models.CharField(max_length=150)
    recycler_address1 = models.CharField(max_length=150)
    recycler_address2 = models.CharField(max_length=150)
    recycler_city = models.ForeignKey(City, on_delete=models.CASCADE)
    recycler_zip = models.OneToOneField(Zip, on_delete=models.CASCADE)
    recycler_state = models.ForeignKey(State, on_delete=models.CASCADE)
    recycler_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    recycler_phone_no = models.IntegerField()

    def __str__(self):
        return str(self.recycler_name)









# class RecyclerMaster(models.Model):
#     recycler_id = models.AutoField(primary_key=True)
#     recycler_name = models.CharField(max_length=150)
#     recycler_address1 = models.CharField(max_length=150)
#     recycler_address2 = models.CharField(max_length=150)
#     recycler_city = models.ForeignKey(City)
#     recycler_zip = models.ForeignKey(Zip)
#     recycler_state = models.ForeignKey(State)
#     recycler_country = models.ForeignKey(Country)
#     recycler_phone_no = models.IntegerField()

#     def __str__(self):
#         return str(self.recycler_name)
