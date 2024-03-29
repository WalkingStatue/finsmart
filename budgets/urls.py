from django.urls import path
from .views import BudgetListView, BudgetCreateView, BudgetUpdateView, BudgetDeleteView, BudgetTransactionsAPIView

app_name = 'budgets'

urlpatterns = [
    path('', BudgetListView.as_view(), name='budget_list'),
    path('create/', BudgetCreateView.as_view(), name='budget_create'),
    path('<int:pk>/update/', BudgetUpdateView.as_view(), name='budget_update'),
    path('<int:pk>/delete/', BudgetDeleteView.as_view(), name='budget_delete'),
    path('api/budgets/<int:pk>/transactions/', BudgetTransactionsAPIView.as_view(), name='budget-transactions-api'),
]