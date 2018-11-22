from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError
from .models import *
from recycler_management.models import *
from hotel_management.models import LoadDashboard
#from django.forms.fields import DateField



class RecyclerRegisterForm(forms.ModelForm):

    class Meta:
        model = RecyclerMaster
        fields = ['recycler_name', 'recycler_address1','recycler_address2', 'recycler_city',
                    'recycler_zip', 'recycler_state', 'recycler_country', 'recycler_phone_no',]



class RecyclerDashboardForm(forms.ModelForm):
    no_of_bags = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    weight = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    load_no = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    date_and_time = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    #date_and_time = forms.DateField(widget = forms.SelectDateWidget())
    contact_details = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    status = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta():
        model = LoadDashboard
        fields = ['load_no', 'no_of_bags', 'weight', 'date_and_time', 'actual_no_of_bags', 'actual_weight', 'pickup_date', 'status', 'contact_details', ]









# class RecyclerRegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     conform_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = RecyclerMaster
#         fields = ['recycler_name', 'email','password', 'conform_password',
#                     'address', 'city', 'state', 'zip', 'country', 'phone_no', ]
                    
#     def clean_conform_password(self):
#         cd = self.cleaned_data
#         if cd['conform_password'] != cd['password']:
#             raise ValidationError("Password don't match")
#         return cd['conform_password']



# class RecyclerLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
