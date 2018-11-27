from hotel_management.models import *
from django.db import models
from django.contrib.auth.models import User
from django import forms
from .models import *


class SyccoProfileForm(forms.ModelForm): 

    class Meta:
        model = SyccoProfile
        fields = ('address1', 'address2', 'city', 'zip', 'state', 'country', 'phone_no',)




# Select_Group = [
#     ('hotel', 'Hotel'),
#     ('recycler', 'Recycler'),
# ]

class SyccoMasterForm(forms.ModelForm):
    #Select_Group = forms.ChoiceField(required=True, widget=forms.RadioSelect( attrs={'class': 'Radio'}), choices= Select_Group)
    class Meta:
        model = SyccoMaster
        fields = ('weight', 'green_point', 'amount',)
        #fields = ('weight', 'green_point', 'amount', 'Select_Group',)