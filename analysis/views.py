from django.views import View
from django.http import JsonResponse
from django.utils.timezone import now
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db.models import Sum,F
from transactions.models import Transaction,Wallet
from django.views.generic import TemplateView
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin


class CashFlowChartView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        date_range = request.GET.get('date_range', 'daily')
        user = request.user
        end_date = now()

        # Truncate and filter based on the date range
        if date_range == 'weekly':
            trunc_date = TruncWeek('transaction_date')
            start_date = end_date - timedelta(weeks=1)
        elif date_range == 'monthly':
            trunc_date = TruncMonth('transaction_date')
            start_date = end_date - timedelta(days=30)  # Roughly a month
        else:  # daily
            trunc_date = TruncDay('transaction_date')
            start_date = end_date - timedelta(days=1)
        
        # Aggregate income and expenses within the time frame
        income_data = Transaction.objects.filter(
            account__user=self.request.user,
            transaction_date__gte=start_date,
            transaction_type='credit'
        ).annotate(period=trunc_date).values('period').annotate(total=Sum('amount')).order_by('period')
        
        expenses_data = Transaction.objects.filter(
            account__user=self.request.user,
            transaction_date__gte=start_date,
            transaction_type='debit'
        ).annotate(period=trunc_date).values('period').annotate(total=Sum('amount')).order_by('period')

        return JsonResponse({
            'income': list(income_data),
            'expenses': list(expenses_data)
        })

class AnalysisView(LoginRequiredMixin,TemplateView):
    template_name = 'analysis/analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class WalletsOverviewView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        wallets = Wallet.objects.filter(account__user=self.request.user).annotate(label=F('name'), value=F('balance'))
        data = list(wallets.values('label', 'value'))
        total_balance = sum(item['value'] for item in data)
        return JsonResponse({
            'wallets': data,
            'total_balance': total_balance
        })
