
import csv
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction as db_transaction
from django.utils.dateparse import parse_datetime
from .forms import CSVUploadForm
from transactions.models import Transaction, Wallet, Category 
from budgets.models import Budget
from goals.models import Goal
from accounts.models import Account
from django.utils import timezone

class ImportTransactionsView(View):
    template_name = 'import_transactions/import.html'
    form_class = CSVUploadForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['csv_file']
            self.process_csv(file, request.user)
            messages.success(request, "Transactions imported successfully!")
            return redirect(reverse_lazy('transactions:user_transactions'))  # Adjust as needed
        return render(request, self.template_name, {'form': form})

    def process_csv(self, file, user):
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        with db_transaction.atomic():  # Ensures atomicity of the batch operation
            for row in reader:
                wallet_name = row.get('Wallet')
                category_name = row.get('Category')
                budget_name = row.get('Budget')
                goal_name = row.get('Goal')
                
                # Directly access the user's account
                account = Account.objects.get(user=user)  # Using get() since OneToOneField guarantees uniqueness
                
                # Similarly fetch the Wallet, Category, Budget, and Goal
                # Ensure these models are linked to the User directly or indirectly to enforce access control
                wallet = Wallet.objects.filter(account=account, name=wallet_name).first()
                category = Category.objects.filter(account=account, name=category_name).first()
                budget = Budget.objects.filter(account=account, name=budget_name).first()
                goal = Goal.objects.filter(account=account, name=goal_name).first()
                
                if not wallet:
                    # Handle missing wallet appropriately, e.g., skip or log error
                    continue
                
                transaction_date = parse_datetime(row.get('Transaction Date')) or timezone.now()
                
                Transaction.objects.create(
                    account=account,
                    wallet=wallet,
                    transaction_type=row.get('Transaction Type').lower(),
                    amount=row.get('Amount'),
                    description=row.get('Description'),
                    category=category,
                    transaction_date=transaction_date,
                    budget=budget,
                    goal=goal,
                )

