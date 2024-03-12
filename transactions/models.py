from django.db import models
from django.conf import settings
from accounts.models import Account
from django.core.exceptions import ValidationError
from django.utils import timezone
from budgets.models import Budget
from goals.models import Goal

now = timezone.now()  # This is timezone-aware and set to 'Asia/Kolkata'


class Wallet(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='wallets')
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} - {self.account.user.username}"

class Category(models.Model):
    name = models.CharField(max_length=255)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="Categories")

    def __str__(self):
        return f"{self.name} - {self.account.user.username}"
    
    class Meta:
        unique_together = ('name', 'account',)


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_account')
    wallet = models.ForeignKey(Wallet, related_name='transactions_wallet', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='transactions_category', on_delete=models.SET_NULL, null=True, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    budget = models.ForeignKey(Budget, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')

    def __str__(self):
        return f"{self.wallet} - {self.amount} - {self.description}"

    def clone(self):
        """Create a clone of the current transaction instance, used for comparison."""
        return Transaction(account=self.account, wallet=self.wallet, transaction_type=self.transaction_type, amount=self.amount)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.budget:
            self.budget.update_amount_spent()
        if self.goal:
            self.goal.update_amount_earned()