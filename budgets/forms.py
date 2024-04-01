from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'total_budget', 'amount_spent','end_date', 'period', 'is_repetitive']  # Include 'is_repetitive' and optionally 'start_date'
        widgets = {
            #'start_date': forms.widgets.DateInput(attrs={'type': 'date'}),  # Make sure to include 'start_date' if you're allowing users to set it
            'end_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            # You might add more widgets for other fields as needed, for styling or functionality purposes.
        }

