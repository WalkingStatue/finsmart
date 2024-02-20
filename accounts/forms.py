# forms.py
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.models import User
from .models import Account
from django import forms

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        # Example of adding a CSS class to the existing fields
        self.fields['login'].widget.attrs.update({'class': 'block w-full text-white border-0 bg-transparent p-0 text-sm file:my-1 file:rounded-full file:border-0 file:bg-accent file:px-4 file:py-2 file:font-medium placeholder:text-muted-foreground/90 focus:outline-none focus:ring-0 sm:leading-7 text-foreground rounded-lg' })
        self.fields['password'].widget.attrs.update({'class': 'block text-white w-full border-0 bg-transparent p-0 text-sm file:my-1 placeholder:text-muted-foreground/90 focus:outline-none focus:ring-0 focus:ring-teal-500 sm:leading-7 text-foreground'})
        
        # If you want to add a placeholder:
        self.fields['login'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        
        # Add CSS classes to the default fields
        self.fields['email'].widget.attrs.update({'class': 'block w-full text-white border-0 bg-transparent p-0 text-sm file:my-1 file:rounded-full file:border-0 file:bg-accent file:px-4 file:py-2 file:font-medium placeholder:text-muted-foreground/90 focus:outline-none focus:ring-0 sm:leading-7 text-foreground rounded-lg'})
        self.fields['username'].widget.attrs.update({'class': 'block w-full text-white border-0 bg-transparent p-0 text-sm file:my-1 file:rounded-full file:border-0 file:bg-accent file:px-4 file:py-2 file:font-medium placeholder:text-muted-foreground/90 focus:outline-none focus:ring-0 sm:leading-7 text-foreground rounded-lg'})
        self.fields['password1'].widget.attrs.update({'class': 'block w-full text-white border-0 bg-transparent p-0 text-sm file:my-1 file:rounded-full file:border-0 file:bg-accent file:px-4 file:py-2 file:font-medium placeholder:text-muted-foreground/90 focus:outline-none focus:ring-0 sm:leading-7 text-foreground rounded-lg'})
        self.fields['password2'].widget.attrs.update({'class': 'block w-full text-white border-0 bg-transparent p-0 text-sm file:my-1 file:rounded-full file:border-0 file:bg-accent file:px-4 file:py-2 file:font-medium placeholder:text-muted-foreground/90 focus:outline-none focus:ring-0 sm:leading-7 text-foreground rounded-lg'})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['image']  # Add other Account model fields here
