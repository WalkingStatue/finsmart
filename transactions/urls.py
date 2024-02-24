from .views import TransactionCreateView, TransactionUpdateView, TransactionDeleteView, UserTransactionsView
from .views import WalletCreateView, WalletUpdateView, WalletDeleteView, WalletListView
from django.urls import path

app_name='transactions'

urlpatterns = [
    path('', UserTransactionsView.as_view(), name='user_transactions'),
    path('add/', TransactionCreateView.as_view(), name='transaction_add'),
    path('<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction_edit'),
    path('<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
    path('wallet/', WalletListView.as_view(), name='wallet_list'),
    path('wallet/add/', WalletCreateView.as_view(), name='add_wallet'),
    path('wallet/<int:pk>/update/', WalletUpdateView.as_view(), name='update_wallet'),
    path('wallet/<int:pk>/delete/', WalletDeleteView.as_view(), name='delete_wallet'),
]
