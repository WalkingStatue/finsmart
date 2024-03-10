from django.db import models
from accounts.models import Account
from django.db.models import Sum, Q
from decimal import Decimal

class Budget(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=100)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.amount_remaining = self.total_budget - self.amount_spent
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def update_amount_spent(self):
        debit_transactions_total = self.transactions.filter(
            transaction_type='debit'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00') 

        self.amount_spent = debit_transactions_total
        self.amount_remaining = self.total_budget - self.amount_spent
        self.save()

