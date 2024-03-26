from django.urls import path
from .views import ImportTransactionsView

app_name = 'import'

urlpatterns = [
    path('import-csv/', ImportTransactionsView.as_view(), name='import_csv'),
]