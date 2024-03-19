from django.urls import path
from .views import CashFlowChartView, AnalysisView, WalletsOverviewView, SpendingTrendsView, Budget_Utilization


app_name = 'analysis'


urlpatterns = [
  path('api/cash-flow-chart/', CashFlowChartView.as_view(), name='cash_flow_chart'),
  path('api/wallets-overview/', WalletsOverviewView.as_view(), name='wallets_overview'),
  path('api/spending-trends/', SpendingTrendsView.as_view(), name='spending_trends'),
  path('api/budget-utilization/', Budget_Utilization.as_view(), name='budget_utilization'),
  path('', AnalysisView.as_view(), name='analysis'),
]