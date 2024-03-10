from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import Budget
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import BudgetForm  # If you're using a custom form

class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    context_object_name = 'budgets'
    template_name = 'budgets/budget_list.html'

    def get_queryset(self):
    # Filter budgets to only include those associated with the logged-in user's account
        queryset = Budget.objects.filter(account__user=self.request.user)
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
    form_class = BudgetForm  # or fields = ['name', 'total_budget', 'amount_spent']
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