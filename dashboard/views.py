from django.shortcuts import render
from django.views.generic import TemplateView
from transactions.models import Transaction, Wallet, Category
from budgets.models import Budget
from goals.models import Goal
from datetime import datetime
from django.db.models import Sum, Case, When, Value, CharField
import plotly.graph_objs as go
from plotly.offline import plot
from django.db.models.functions import TruncDay

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filter budgets by logged-in user
        context['budgets'] = Budget.objects.filter(account__user=self.request.user)
        context['goals'] = Goal.objects.filter(account__user=self.request.user)

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

        # Choose a tip based on the day of the year
        day_of_year = datetime.now().timetuple().tm_yday
        tip_of_the_day = financial_tips[(day_of_year - 1) % len(financial_tips)]
        context['tip_of_the_day'] = tip_of_the_day

        recent_transactions = Transaction.objects.filter(account__user=self.request.user).order_by('-transaction_date')[:5]
        context['recent_transactions'] = recent_transactions

        income = Transaction.objects.filter(
            account__user=self.request.user,
            transaction_type='credit'
        ).aggregate(total_income=Sum('amount'))['total_income'] or 0

        expenses = Transaction.objects.filter(
            account__user=self.request.user,
            transaction_type='debit'
        ).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

        context['total_income'] = income
        context['total_expenses'] = expenses

        income_by_day = Transaction.objects.filter(
            account__user=self.request.user,
            transaction_type='credit'
        ).annotate(day=TruncDay('transaction_date')).values('day').annotate(total=Sum('amount')).order_by('day')

        expenses_by_day = Transaction.objects.filter(
            account__user=self.request.user,
            transaction_type='debit'
        ).annotate(day=TruncDay('transaction_date')).values('day').annotate(total=Sum('amount')).order_by('day')

        context['income'] = income_by_day
        context['expenses'] = expenses_by_day

         # Plotly: Create line chart data for income and expenses
        income_trace = go.Scatter(
            x=[item['day'] for item in income_by_day],
            y=[item['total'] for item in income_by_day],
            fill='tozeroy',  # for area chart
            mode='lines',  # for line chart, change to 'lines+markers' if you want points
            name='Income',
            stackgroup='one'  # for area chart
        )
        expenses_trace = go.Scatter(
            x=[item['day'] for item in expenses_by_day],
            y=[item['total'] for item in expenses_by_day],
            fill='tozeroy',  # for area chart
            mode='lines',  # for line chart, change to 'lines+markers' if you want points
            name='Expenses',
            stackgroup='two'  # for area chart
        )

        data = [income_trace, expenses_trace]

        layout = go.Layout(
            title='Income and Expenses Over Time',
            titlefont=dict(
                size=22,
                color='rgba(255,255,255, 0.9)',  # White with a bit of transparency
            ),
            xaxis=dict(
                title='Date',
                titlefont=dict(
                    size=18,
                    color='rgba(255,255,255, 0.9)'
                ),
                tickfont=dict(
                    color='rgba(255,255,255, 0.7)'
                ),
                gridcolor='rgba(255,255,255, 0.3)'
            ),
            yaxis=dict(
                title='Amount',
                titlefont=dict(
                    size=18,
                    color='rgba(255,255,255, 0.9)'
                ),
                tickfont=dict(
                    color='rgba(255,255,255, 0.7)'
                ),
                gridcolor='rgba(255,255,255, 0.3)'
            ),
            
            width=1020,  # Width in pixels
            height=500,  # Height in pixels
            margin=dict(l=50, r=50, t=50, b=50),
            paper_bgcolor='rgba(0,0,0,0)',  # Fully transparent
            plot_bgcolor='rgba(0,0,0,0)',   # Fully transparent
            legend=dict(
                font=dict(
                    color='rgba(255,255,255, 0.8)'
                )
            ),
            
        )

        fig = go.Figure(data=data, layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)

        context['plot_div'] = plot_div

        ## Pie Chart For Categories
        categories = Category.objects.filter(
            transactions_category__account__user=self.request.user
        ).distinct()

        # Aggregate income and expenses by category
        category_data = categories.annotate(
            total_income=Sum(
                Case(
                    When(transactions_category__transaction_type='credit', then='transactions_category__amount'),
                    default=Value(0),
                    output_field=CharField()
                )
            ),
            total_expenses=Sum(
                Case(
                    When(transactions_category__transaction_type='debit', then='transactions_category__amount'),
                    default=Value(0),
                    output_field=CharField()
                )
            )
        ).values('name', 'total_income', 'total_expenses').order_by('name')

        context['category_data'] = list(category_data)
        income_trace = go.Bar(
            name='Income',
            x=[category['name'] for category in context['category_data']],
            y=[category['total_income'] for category in context['category_data']],
            marker=dict(color='green'),
        )
        expenses_trace = go.Bar(
            name='Expenses',
            x=[category['name'] for category in context['category_data']],
            y=[category['total_expenses'] for category in context['category_data']],
            marker=dict(color='red'),
        )

        data = [income_trace, expenses_trace]
        layout = go.Layout(
            title='Income and Expenses by Category',
            barmode='stack',
            margin=dict(l=30, r=30, t=30, b=30)
        )

        fig = go.Figure(data=data, layout=layout)
        stacked_bar_plot_div = plot(fig, output_type='div', include_plotlyjs=False)

        context['stacked_bar_plot_div'] = stacked_bar_plot_div
        return context
