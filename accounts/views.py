from .forms import UserForm, AccountForm, UserUpdateForm, AccountUpdateForm
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView
from transactions.models import Wallet, Category
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .models import Account

class ProfileCompleteView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'accounts/complete_profile.html'
    user_form_class = UserForm
    account_form_class = AccountForm
    success_url = reverse_lazy('account:home')  # Adjust as needed

    def get(self, request, *args, **kwargs):
        user_form = self.user_form_class(instance=request.user)
        account, created = Account.objects.get_or_create(user=request.user)
        account_form = self.account_form_class(instance=account)
        return self.render_to_response({'user_form': user_form, 'account_form': account_form})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        account = form.save(commit=False)
        account.profile_completed = True
        account.save()
        return response

    def post(self, request, *args, **kwargs):
        user_form = self.user_form_class(request.POST, instance=request.user)
        account, created = Account.objects.get_or_create(user=request.user)
        account_form = self.account_form_class(request.POST, request.FILES, instance=account)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account = account_form.save(commit=False)
            account.profile_completed = True
            account.save()
            return redirect(self.success_url)

        return self.render_to_response({'user_form': user_form, 'account_form': account_form})

class ProfileSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_settings.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileSettingsView, self).get_context_data(**kwargs)
        user = self.request.user
        context['wallets'] = Wallet.objects.filter(account__user=user)
        context['categories'] = Category.objects.filter(account__user=user)
        
        # Add the forms to the context
        context['u_form'] = UserUpdateForm(instance=user)
        context['a_form'] = AccountUpdateForm(instance=user.account)
        
        return context

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        a_form = AccountUpdateForm(instance=request.user.account)

        context = {
            'u_form': u_form,
            'a_form': a_form,
        }

        return render(request, 'accounts/profile_update.html', context)

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)

        if u_form.is_valid() and a_form.is_valid():
            u_form.save()
            a_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile_settings')

        context = {
            'u_form': u_form,
            'a_form': a_form,
        }

        return render(request, 'accounts/profile_update.html', context)
