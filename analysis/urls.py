from django.urls import path
from .views import CashFlowChartView, AnalysisView, WalletsOverviewView


app_name = 'analysis'


urlpatterns = [
  path('api/cash-flow-chart/', CashFlowChartView.as_view(), name='cash_flow_chart'),
  path('api/wallets-overview/', WalletsOverviewView.as_view(), name='wallets_overview'),
  path('', AnalysisView.as_view(), name='analysis'),
]