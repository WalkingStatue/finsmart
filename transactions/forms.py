from django import forms
from .models import Category,Wallet,Transaction
from django.core.exceptions import ValidationError
from budgets.models import Budget
from goals.models import Goal
from django import forms
from django.utils import timezone

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'balance']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['wallet', 'transaction_type', 'amount', 'description', 'category', 'budget', 'goal']
        
    def __init__(self, *args, user=None, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['wallet'].queryset = Wallet.objects.filter(account__user=user)
            self.fields['category'].queryset = Category.objects.filter(account__user=user)
            self.fields['budget'].queryset = Budget.objects.filter(account__user=user)
            self.fields['goal'].queryset = Goal.objects.filter(account__user=user)

    def clean(self):
        cleaned_data = super().clean()
        wallet = cleaned_data.get('wallet')
        transaction_type = cleaned_data.get('transaction_type')
        amount = cleaned_data.get('amount')
        budget = cleaned_data.get('budget')
        goal = cleaned_data.get('goal')

        if goal and amount:
            if goal.amount_earned - amount < 0:
                raise ValidationError({
                    'amount': 'This goal is achieved. Please create a new goal'
                })

        if budget and amount:
            if budget.amount_remaining - amount < 0:
                raise ValidationError({
                    'amount': 'This transaction cannot be completed as it exceeds the budget available.'
                })

        if amount is not None and amount < 0:
            self.add_error('amount', 'The amount cannot be negative.')

        if transaction_type == 'debit' and wallet and wallet.balance < amount:
            self.add_error('amount', 'Insufficient funds in wallet.')

        return cleaned_data


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date cannot be before the start date.")

        return cleaned_data
