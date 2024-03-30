
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
            self.process_csv(request, file, self.request.user)
            messages.success(request, "Transactions imported successfully!", extra_tags='import_transactions')
            return redirect(reverse_lazy('transactions:user_transactions')) 
        else:
            return render(request, self.template_name, {'form': form})

    def process_csv(self,request,file, user):
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        skipped_records = 0 
        
        with db_transaction.atomic():
            for row in reader:
                wallet_name = row.get('Wallet')
                transaction_type = row.get('Transaction Type')
                transaction_date_str = row.get('Transaction Date')
                
               
                if not wallet_name or not transaction_type or not transaction_date_str:
                    skipped_records += 1
                    continue
                
                transaction_date = parse_datetime(transaction_date_str) or timezone.now()
                
                account = Account.objects.get(user=user)  
                wallet = Wallet.objects.filter(account=account, name=wallet_name).first()
                
                if not wallet:
                    skipped_records += 1
                    continue
                
                category_name = row.get('Category')
                budget_name = row.get('Budget')
                goal_name = row.get('Goal')
                category = Category.objects.filter(account=account, name=category_name).first()
                budget = Budget.objects.filter(account=account, name=budget_name).first()
                goal = Goal.objects.filter(account=account, name=goal_name).first()
                    
                Transaction.objects.create(
                    account=account,
                    wallet=wallet,
                    transaction_type=transaction_type.lower(),
                    amount=row.get('Amount'),
                    description=row.get('Description'),
                    category=category,
                    transaction_date=transaction_date,
                    budget=budget,
                    goal=goal,
                )
        if skipped_records > 0:
            messages.warning(request, f"{skipped_records} records were skipped due to missing required fields.", extra_tags='import_transactions')
            print(f"{skipped_records} records were skipped due to missing wallet, transaction type, or transaction date.")
