# forms.py
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.models import User
from .models import Account
from django import forms

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
      

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['image']  # Add other Account model fields here

from django import forms
from django.contrib.auth.models import User
from .models import Account

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['image']
