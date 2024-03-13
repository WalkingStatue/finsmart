from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import GoalForm
from datetime import date
from .models import Goal

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