from django.urls import path
from .views import ExportTransactionsView, ExportTransactionsPDFView

app_name = 'export'

urlpatterns = [
    path('export-csv/', ExportTransactionsView.as_view(), name='export_csv'),
    path('export-pdf/', ExportTransactionsPDFView.as_view(), name='export_pdf'),
]
