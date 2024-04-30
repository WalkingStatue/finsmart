from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'total_goal', 'amount_earned', 'target_date']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_total_goal(self):
        total_goal = self.cleaned_data.get('total_goal')
        
        if total_goal is not None:
            if total_goal <= 0:
                self.add_error('total_goal', 'Total goal must be greater than 0.')
        return total_goal
    
    def clean_end_date(self):
        target_date = self.cleaned_data.get('target_date')
        
        if target_date is not None:
            if target_date < timezone.now().date():
                raise forms.ValidationError("End date cannot be before today's date.")
        return target_date

