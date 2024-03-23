from django.urls import path
from .views import ExportTransactionsView

app_name = 'export'

urlpatterns = [
    path('export-csv/', ExportTransactionsView.as_view(), name='export_csv'),
]
