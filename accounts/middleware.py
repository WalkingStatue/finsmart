from django.shortcuts import redirect
from django.urls import reverse
from .models import Account
from accounts import urls
class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.path.startswith('/accounts/'):
            accounts, created = Account.objects.get_or_create(user=request.user)
            if not accounts.profile_completed and not request.path.startswith(reverse('account:profile_update')):
                return redirect('account:profile_update')
        return self.get_response(request)
        return response

   
