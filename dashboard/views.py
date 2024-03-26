from django.shortcuts import render
from django.views.generic import TemplateView
from transactions.models import Transaction, Category
from budgets.models import Budget
from goals.models import Goal
from datetime import datetime
from django.db.models import Sum, Case, When, Value, DecimalField
import plotly.graph_objs as go
from plotly.offline import plot
from django.http import JsonResponse
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get budgets and goals associated with the current user
        context['budgets'] = Budget.objects.filter(account__user=self.request.user)
        context['goals'] = Goal.objects.filter(account__user=self.request.user)

        # Daily financial tips array
        financial_tips = [
        "Tip 1: Keep an emergency fund.",
        "Tip 2: Pay off your credit card balance every month.",
        "Tip 3: Invest in low-cost index funds.",
        "Tip 4: Save at least 10% of your income for retirement.",
        "Tip 5: Diversify your investments to manage risk.",
        "Tip 6: Check your credit report annually.",
        "Tip 7: Use credit cards wisely and pay off the balance each month.",
        "Tip 8: Consider low-cost index funds for long-term investments.",
        "Tip 9: Review your insurance policies annually.",
        "Tip 10: Keep your financial records organized.",
        "Tip 11: Automate savings to ensure you pay yourself first.",
        "Tip 12: Refinance high-interest loans if possible.",
        "Tip 13: Invest in your education and skills.",
        "Tip 14: Shop around before making major purchases.",
        "Tip 15: Avoid late fees by setting up automatic payments.",
        "Tip 16: Track your spending for better financial awareness.",
        "Tip 17: Make a plan to pay off student loans.",
        "Tip 18: Use tax-advantaged accounts for healthcare and retirement savings.",
        "Tip 19: Don’t withdraw from retirement accounts early to avoid penalties.",
        "Tip 20: Take advantage of employer matching for your retirement plan.",
        "Tip 21: Negotiate bills where possible, like insurance or cell phone plans.",
        "Tip 22: Practice conscious spending, prioritizing expenses that matter most.",
        "Tip 23: Set specific financial goals and timelines.",
        "Tip 24: Learn about investing to make informed decisions.",
        "Tip 25: Plan for taxes throughout the year to avoid surprises.",
        "Tip 26: Review your subscriptions and memberships regularly.",
        "Tip 27: Maintain a good credit score for better rates on loans.",
        "Tip 28: Use financial apps to help manage your money.",
        "Tip 29: Create a will to protect your assets and family.",
        "Tip 30: Learn about the power of compound interest.",
        "Tip 31: Avoid new debt if you’re currently paying off other loans.",
        "Tip 32: Save for your children’s education early.",
        "Tip 33: Set aside money for yearly expenses, like property taxes or holidays.",
        "Tip 34: Consider a side hustle for extra income.",
        "Tip 35: Protect your identity online and monitor for fraud.",
        "Tip 36: Regularly contribute to a retirement account, no matter your age.",
        "Tip 37: Use cashback and rewards programs wisely.",
        "Tip 38: Understand the fees you’re paying on investments and financial services.",
        "Tip 39: Balance saving for the future with enjoying the present.",
        "Tip 40: Educate your children about money and saving.",
        "Tip 41: Don't chase investment fads without doing your research.",
        "Tip 42: Prioritize high-interest savings for your emergency fund.",
        "Tip 43: Avoid using payday loans with high fees and interest rates.",
        "Tip 44: Take advantage of free financial resources and workshops.",
        "Tip 45: Review and understand your investment portfolio.",
        "Tip 46: Regularly update your financial goals as your life changes.",
        "Tip 47: Learn the basics of personal finance and economics.",
        "Tip 48: Don’t make emotional decisions with your investments.",
        "Tip 49: Plan for major life events like marriage, children, and retirement.",
        "Tip 50: Keep your financial portfolio balanced and aligned with your risk tolerance.",
        # ... Add more tips up to 100 as you like
        ]

        # Select a daily tip based on the day of the year
        day_of_year = datetime.now().timetuple().tm_yday
        tip_of_the_day = financial_tips[(day_of_year - 1) % len(financial_tips)]
        context['tip_of_the_day'] = tip_of_the_day

        # Fetch the most recent transactions for the current user
        recent_transactions = Transaction.objects.filter(account__user=self.request.user).order_by('-transaction_date')[:5]
        context['recent_transactions'] = recent_transactions

        # Aggregate total income and expenses for the current user
        income = Transaction.objects.filter(
            account__user=self.request.user,
            transaction_type='credit'
        ).aggregate(total_income=Sum('amount'))['total_income'] or 0

        expenses = Transaction.objects.filter(
            account__user=self.request.user,
            transaction_type='debit'
        ).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

        # Add total income and expenses to the context
        context['total_income'] = income
        context['total_expenses'] = expenses


        # This section aggregates total income and expenses by category
        categories = Category.objects.filter(
            transactions__account__user=self.request.user
        ).distinct()

        category_data = categories.annotate(
            total_income=Sum(
                Case(
                    When(transactions__transaction_type='credit', then='transactions__amount'),
                    default=Value(0),
                    output_field=DecimalField()
                )
            ),
            total_expenses=Sum(
                Case(
                    When(transactions__transaction_type='debit', then='transactions__amount'),
                    default=Value(0),
                    output_field=DecimalField()
                )
            )
        ).values('name', 'total_income', 'total_expenses').order_by('name')

        # These pie charts use the aggregated data to show the proportion of each category in total income and expenses

        # Create the income pie chart
        income_labels = [category['name'] for category in category_data if category['total_income'] > 0]
        income_values = [category['total_income'] for category in category_data if category['total_income'] > 0]

        income_pie = go.Pie(labels=income_labels, values=income_values, name="Income")
        income_layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=30, r=30, t=30, b=30)
        )
        income_fig = go.Figure(data=[income_pie], layout=income_layout)
        income_pie_div = plot(income_fig, output_type='div', include_plotlyjs=False)

        # Create the expenses pie chart
        expenses_labels = [category['name'] for category in category_data if category['total_expenses'] > 0]
        expenses_values = [category['total_expenses'] for category in category_data if category['total_expenses'] > 0]

        expenses_pie = go.Pie(labels=expenses_labels, values=expenses_values, name="Expenses")
        expenses_layout = go.Layout(
            #title="Expenses by Category",
            #titlefont=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=30, r=30, t=30, b=30)
        )
        expenses_fig = go.Figure(data=[expenses_pie], layout=expenses_layout)
        expenses_pie_div = plot(expenses_fig, output_type='div', include_plotlyjs=False)

        context['income_pie_div'] = income_pie_div
        context['expenses_pie_div'] = expenses_pie_div

        return context

def get_transactions(request):
    # Retrieve the user's selection from the request; default to daily if not provided
    range_type = request.GET.get('range_type', 'daily')
    
    # Map range_type to the corresponding Django Trunc function
    trunc_mappings = {
        'daily': TruncDay,
        'weekly': TruncWeek,
        'monthly': TruncMonth,
    }
    trunc_function = trunc_mappings.get(range_type, TruncDay)

    # Query for income
    income_by_range = Transaction.objects.filter(
        account__user=request.user,
        transaction_type='credit'
    ).annotate(period=trunc_function('transaction_date')).values('period').annotate(total=Sum('amount')).order_by('period')

    # Query for expenses
    expenses_by_range = Transaction.objects.filter(
        account__user=request.user,
        transaction_type='debit'
    ).annotate(period=trunc_function('transaction_date')).values('period').annotate(total=Sum('amount')).order_by('period')

    # Convert querysets to lists of dicts for JSON serialization
    income_data = list(income_by_range)
    expenses_data = list(expenses_by_range)

    # Return the data as JSON
    return JsonResponse({
        'income': income_data,
        'expenses': expenses_data,
    })