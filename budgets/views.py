from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import Budget
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import BudgetForm  
from django.utils import timezone
class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    context_object_name = 'budgets'
    template_name = 'budgets/budget_list.html'

    def get_queryset(self):
        today = timezone.now().date()
        queryset = Budget.objects.filter(account__user=self.request.user)

        for budget in queryset:
            # Calculate the number of days remaining in the budget period
            if budget.end_date and budget.end_date >= today:
                days_remaining = (budget.end_date - today).days
            else:
                days_remaining = 0  # or however you want to handle past budget periods
            
            # Calculate how much can be spent each day
            if days_remaining > 0:
                daily_spendable = budget.amount_remaining / days_remaining
            else:
                daily_spendable = budget.amount_remaining  # or set to 0 if the period has ended
            
            # Attach the calculations to the budget object
            budget.days_remaining = days_remaining
            budget.daily_spendable = daily_spendable
        
        return queryset


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm  # Use this if you defined a custom form
    # fields = ['name', 'total_budget', 'amount_spent']  # Use this instead of form_class if you're not using a custom form
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budgets:budget_list')

    def form_valid(self, form):
        form.instance.account = self.request.user.account
        return super().form_valid(form)

class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budgets:budget_list')

    def get_queryset(self):
        return super().get_queryset().filter(account__user=self.request.user)

class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'budgets/budget_confirm_delete.html'
    success_url = reverse_lazy('budgets:budget_list')

    def get_queryset(self):
        return super().get_queryset().filter(account__user=self.request.user)