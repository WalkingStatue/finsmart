from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):    
    class Meta:
        model = Budget
        fields = ['name', 'total_budget', 'amount_spent', 'period', 'end_date']  # Add 'start_date' here if it's in the form
        widgets = {
            'end_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            # 'start_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

