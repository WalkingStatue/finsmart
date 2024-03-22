from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import GoalForm
from datetime import date
from .models import Goal
from django.views import View
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    context_object_name = 'goals'
    template_name = 'goals/goal_list.html'

    def get_queryset(self):
        # Get the current user's goals
        queryset = Goal.objects.filter(account__user=self.request.user)
        today = timezone.now().date()
        for goal in queryset:
            # Calculate days remaining only if target_date is set
            if goal.target_date:
                delta = goal.target_date - today
                goal.days_remaining = max(delta.days, 0)  # Ensuring it doesn't go negative
            else:
                goal.days_remaining = None
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goals/goal_form.html'
    success_url = reverse_lazy('goals:goal_list')

    def form_valid(self, form):
        form.instance.account = self.request.user.account
        return super().form_valid(form)

class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goals/goal_form.html'
    success_url = reverse_lazy('goals:goal_list')

    def get_queryset(self):
        return super().get_queryset().filter(account__user=self.request.user)

class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = 'goals/goal_confirm_delete.html'
    success_url = reverse_lazy('goals:goal_list')

    def get_queryset(self):
        return super().get_queryset().filter(account__user=self.request.user)

class GoalTransactionsAPIView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Get the budget by pk provided in the URL
        goal = get_object_or_404(Goal, pk=kwargs['pk'], account__user=request.user)

        # Get the transactions related to the budget
        transactions = goal.transactions.filter(transaction_type='credit').order_by('-transaction_date')


        # Prepare the transactions for the template
        transactions_data = [{
            'description': transaction.description,
            'transaction_type': transaction.get_transaction_type_display(),  # Use get_FOO_display() for human-readable name
            'category_name': transaction.category.name if transaction.category else 'N/A',
            'transaction_date': transaction.transaction_date.strftime('%Y-%m-%d'),  # Adjusted for full datetime
            'amount': transaction.amount
        } for transaction in transactions]


        # Render the transactions template
        html = render_to_string('goals/goal_transactions.html', {'transactions': transactions_data})

        return HttpResponse(html)