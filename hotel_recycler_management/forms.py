from hotel_management.models import *
from django.db import models
from django.contrib.auth.models import User









Select_Group= [
    ('Hotel', 'Hotel'),
    ('Recycler', 'Recycler'),    
    ]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(max_length=150)
    #Select_Group = forms.CharField(label='Select Group', widget=forms.RadioSelect(choices=Select_Group))

    class Meta:
        model = User
        #fields = ('username', 'email', 'password',)
        fields = ('username', 'email', 'password',)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('phone_no', 'company',)


# class SyccoProfileForm(forms.ModelForm):

#     class Meta:
#         model = SyccoProfile
#         fields = ('address1', 'address2', 'city', 'zip', 'state', 'country', 'phone_no',)