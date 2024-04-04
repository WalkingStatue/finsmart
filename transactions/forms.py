from django import forms
from .models import Category,Wallet,Transaction
from django.core.exceptions import ValidationError
from budgets.models import Budget
from goals.models import Goal

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

    def form_valid(self, form):
        #form.instance.user = self.request.user  # Assuming the Transaction model links directly to the Django User
        #form.instance.account = self.request.user.account  # If your Transaction model links to a custom Account model
        response = super().form_valid(form)  # This saves the Transaction
        transaction = form.instance
        if transaction.budget:
            transaction.budget.update_amount_spent()  # Make sure your Budget model has this method
            transaction.budget.save()
        if transaction.goal:
            transaction.goal.update_amount_earned()  # Make sure your Goal model has this method
            transaction.goal.save()
        return response
    def clean(self):
        cleaned_data = super().clean()
        wallet = cleaned_data.get('wallet')
        transaction_type = cleaned_data.get('transaction_type')
        amount = cleaned_data.get('amount')
        budget = cleaned_data.get('budget')
        goal = cleaned_data.get('goal')

        if goal and amount:
            # Directly use the amount_remaining field to check if transaction exceeds the goal
            if goal.amount_earned - amount < 0:
                raise ValidationError({
                    'amount': 'This goal is achieved. Please create a new goal'
                })

        if budget and amount:
            # Directly use the amount_remaining field to check if transaction exceeds the budget
            if budget.amount_remaining - amount < 0:
                raise ValidationError({
                    'amount': 'This transaction cannot be completed as it exceeds the budget available.'
                })

        # Check if the transaction amount is negative
        if amount is not None and amount < 0:
            self.add_error('amount', 'The amount cannot be negative.')

        # Existing check for insufficient funds
        if transaction_type == 'debit' and wallet and wallet.balance < amount:
            self.add_error('amount', 'Insufficient funds in wallet.')

        return cleaned_data


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

