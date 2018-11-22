# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from hotel_management.models import City, Zip, State, Country, HotelMaster
from recycler_management.models import RecyclerMaster

# Create your models here.

class SyccoProfile(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zip = models.ForeignKey(Zip, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    phone_no = models.IntegerField()

    def __str__(self):
        return str(self.user)


class SyccoMaster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=250)
    weight = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    green_point = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_greenpoint = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.user)


class SyccoHRtable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_name = models.ForeignKey(HotelMaster, on_delete=models.CASCADE)
    recycler_name = models.ForeignKey(RecyclerMaster, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
