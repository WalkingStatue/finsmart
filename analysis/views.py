from django.views import View
from django.http import JsonResponse
from django.utils.timezone import now
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db.models import Sum,F
from transactions.models import Transaction,Wallet,Category
from budgets.models import Budget
from django.views.generic import TemplateView
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal 


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


class SpendingTrendsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        time_period = request.GET.get('time_period', 'monthly')
        category_ids = request.GET.get('category_ids', None)
    
        if category_ids:
            categories = Category.objects.filter(account__user=self.request.user, id__in=category_ids.split(','))
        else:
            categories = Category.objects.filter(account__user=self.request.user)
             # Define the truncation and filtering based on the time period
        if time_period == 'weekly':
            trunc_date = TruncWeek('transaction_date')
        else:  # Default to monthly
            trunc_date = TruncMonth('transaction_date')

        trends_data = []
        for category in categories:
            transactions = Transaction.objects.filter(
                account__user=self.request.user,
                category=category
            ).annotate(period=trunc_date).values('period').annotate(total=Sum('amount')).order_by('period')

            # Convert QuerySet to a list of dictionaries
            data = [{'period': entry['period'], 'total': entry['total']} for entry in transactions]
            trends_data.append({
                'category': category.name,
                'trends': data
            })

        return JsonResponse({'trends_data': trends_data})



class Budget_Utilization(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        budgets = Budget.objects.filter(account__user=request.user)
        budget_data = []

        for budget in budgets:
            transactions = Transaction.objects.filter(
                account=budget.account,
                transaction_date__gte=budget.start_date,
                transaction_date__lte=budget.end_date or timezone.now()
            )
            
            total_spent = transactions.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            
            # If total_budget is 0, set utilization to 0 to avoid division by zero
            utilization = (budget.amount_spent / budget.total_budget * 100) if budget.total_budget else Decimal('0.00')
            
            budget_data.append({
                'name': budget.name,
                'total_budget': str(budget.total_budget),
                'amount_spent': str(budget.amount_spent),
                'utilization': str(utilization)  # Convert Decimal to string for JSON serialization
            })

        return JsonResponse({'budget_data': budget_data})

