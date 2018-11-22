from django import forms
from .models import *
from django.db import models
from django.contrib.auth.models import User




class HotelsearchForm(forms.ModelForm):
    class Meta():
        model = HotelMaster
        fields = ['hotel_zip']


class HoteldashboardcreateForm(forms.ModelForm):
    class Meta():
        model = LoadDashboard
        fields = ['product', 'category', 'contact_details', 'no_of_bags', 'weight', 'remarks',]


#class RemakForm(forms.)