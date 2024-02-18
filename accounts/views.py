from django.views.generic import ListView
from .models import Account
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, AccountForm

class HomePageView(ListView):
    model = Account
    template_name = 'accounts/homepage.html'
    context_object_name = 'accounts'
    queryset = Account.objects.all().order_by('user__username')



class ProfileUpdateView(LoginRequiredMixin, TemplateResponseMixin, View):
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