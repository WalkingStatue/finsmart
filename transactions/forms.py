from django import forms
from .models import Category,Wallet,Transaction

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
        fields = ['wallet', 'transaction_type', 'amount', 'description', 'category']
        
    def __init__(self, *args, user=None, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['wallet'].queryset = Wallet.objects.filter(account__user=user)
            self.fields['category'].queryset = Category.objects.filter(account__user=user)

    def clean(self):
        cleaned_data = super().clean()
        wallet = cleaned_data.get('wallet')
        transaction_type = cleaned_data.get('transaction_type')
        amount = cleaned_data.get('amount')

        if transaction_type == 'debit' and wallet.balance < amount:
            self.add_error('amount', 'Insufficient funds in wallet.')

        return cleaned_data

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

