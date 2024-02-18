# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Account

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['image']  # Add other Account model fields here
