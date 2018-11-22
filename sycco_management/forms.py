from hotel_management.models import *
from django.db import models
from django.contrib.auth.models import User
from django import forms
from .models import *


class SyccoProfileForm(forms.ModelForm): 

    class Meta:
        model = SyccoProfile
        fields = ('address1', 'address2', 'city', 'zip', 'state', 'country', 'phone_no',)


class SyccoMasterForm(forms.ModelForm):

    class Meta:
        model = SyccoMaster
        fields = ('weight', 'green_point', 'amount',)