from django.views.generic import ListView
from .models import Account

class HomePageView(ListView):
    model = Account
    template_name = 'accounts/homepage.html'
    context_object_name = 'accounts'
    queryset = Account.objects.all().order_by('user__username')
