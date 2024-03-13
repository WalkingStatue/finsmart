from django.db import models
from accounts.models import Account
from django.db.models import Sum, Q
from decimal import Decimal

class Goal(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='goals')
    name = models.CharField(max_length=100)
    total_goal = models.DecimalField(max_digits=10, decimal_places=2)
    amount_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    target_date = models.DateField(null=True, blank=True)
    def save(self, *args, **kwargs):
        self.amount_remaining = self.total_goal - self.amount_earned
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def update_amount_earned(self):
        credit_transactions_total = self.transactions.filter(
            transaction_type='credit'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00') 

        self.amount_earned = credit_transactions_total
        self.amount_remaining = self.total_goal - self.amount_earned
        self.save()

