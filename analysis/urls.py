from django.urls import path
from .views import CashFlowChartView, AnalysisView


app_name = 'analysis'


urlpatterns = [
  path('api/cash-flow-chart/', CashFlowChartView.as_view(), name='cash_flow_chart'),
  path('', AnalysisView.as_view(), name='analysis'),
]