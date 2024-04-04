from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import Budget
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import BudgetForm  
from django.utils import timezone
from django.views import View
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    context_object_name = 'budgets'
    template_name = 'budgets/budget_list.html'

    def get_queryset(self):
        today = timezone.now().date()
        queryset = Budget.objects.filter(account__user=self.request.user).prefetch_related('transactions')

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
            # Attach the transactions to the budget object
            budget.transactions_list = budget.transactions.all()
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

class BudgetTransactionsAPIView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Get the budget by pk provided in the URL
        budget = get_object_or_404(Budget, pk=kwargs['pk'], account__user=request.user)

        # Get the transactions related to the budget
        transactions = budget.transactions.filter(transaction_type='debit').order_by('-transaction_date')


        # Prepare the transactions for the template
        transactions_data = [{
            'description': transaction.description,
            'transaction_type': transaction.get_transaction_type_display(),  # Use get_FOO_display() for human-readable name
            'category_name': transaction.category.name if transaction.category else 'N/A',
            'transaction_date': transaction.transaction_date.strftime('%Y-%m-%d'),  # Adjusted for full datetime
            'amount': transaction.amount
        } for transaction in transactions]


        # Render the transactions template
        html = render_to_string('budgets/budget_transactions.html', {'transactions': transactions_data})

        return HttpResponse(html)