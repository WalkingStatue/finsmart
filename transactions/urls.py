from .views import TransactionCreateView, TransactionUpdateView, TransactionDeleteView, UserTransactionsView
from .views import WalletCreateView, WalletUpdateView, WalletDeleteView, WalletListView
from .views import CategoryCreateView, CategoryUpdateView, CategoryDeleteView ,CategoryListView
from django.urls import path

app_name='transactions'

urlpatterns = [
    path('', UserTransactionsView.as_view(), name='user_transactions'),
    path('add/', TransactionCreateView.as_view(), name='transaction_add'),
    path('<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction_edit'),
    path('<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
    path('wallet/', WalletListView.as_view(), name='wallet_list'),
    path('wallet/<int:pk>/', UserTransactionsView.as_view(), name='wallet_transactions'),
    path('wallet/add/', WalletCreateView.as_view(), name='add_wallet'),
    path('wallet/<int:pk>/update/', WalletUpdateView.as_view(), name='update_wallet'),
    path('wallet/<int:pk>/delete/', WalletDeleteView.as_view(), name='delete_wallet'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='add_category'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='update_category'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='delete_category'),
]
