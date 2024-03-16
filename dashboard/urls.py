from django.urls import path
from .views import DashboardView, get_transactions


app_name = 'dashboard'


urlpatterns = [
    path('', DashboardView.as_view(), name='user_dashboard'),
    path('transactions/date-range/', get_transactions, name='transactions_date_range'),
]
