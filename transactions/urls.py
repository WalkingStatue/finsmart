from .views import TransactionCreateView, TransactionUpdateView, TransactionDeleteView, UserTransactionsView
from django.urls import path

app_name='transactions'

urlpatterns = [
    path('', UserTransactionsView.as_view(), name='user_transactions'),
    path('add/', TransactionCreateView.as_view(), name='transaction_add'),
    path('<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction_edit'),
    path('<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
]
