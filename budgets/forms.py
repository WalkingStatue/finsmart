from django import forms
from django.utils import timezone
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'total_budget', 'amount_spent','end_date', 'period', 'is_repetitive']
        widgets = {
            'end_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def clean_total_budget(self):
        total_budget = self.cleaned_data.get('total_budget')
        if total_budget is not None:
            if total_budget <= 0:
                self.add_error('total_budget', 'Total budget must be greater than 0.')
        return total_budget

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date is not None:
            if end_date < timezone.now().date():
                raise forms.ValidationError("End date cannot be before today's date.")
        return end_date
