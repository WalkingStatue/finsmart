from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from urllib.parse import quote
from .forms import DateRangeForm
from transactions.models import Transaction
import csv

class ExportTransactionsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = DateRangeForm()
        return render(request, 'export/export.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = DateRangeForm(request.POST)
        if form.is_valid():
            print("Form is valid, processing data...")

            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            transactions = Transaction.objects.filter(
                account__user=self.request.user, 
                transaction_date__date__range=(start_date, end_date))

            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': f'attachment; filename={quote("transactions.csv")}'}
            )

            writer = csv.writer(response)
            writer.writerow(['Account', 'Wallet', 'Transaction Type', 'Amount', 'Description', 'Category', 'Transaction Date', 'Budget', 'Goal'])

            for transaction in transactions:
                writer.writerow([
                    transaction.account,
                    transaction.wallet,
                    transaction.transaction_type,
                    transaction.amount,
                    transaction.description,
                    transaction.category,
                    transaction.transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
                    transaction.budget,
                    transaction.goal,
                ])

            return response
        else:
            print(f"Form errors: {form.errors}")
        return render(request, 'export/export.html', {'form': form})
