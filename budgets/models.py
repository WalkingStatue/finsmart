from django.db import models
from accounts.models import Account
from django.db.models import Sum
from decimal import Decimal
from datetime import timedelta
from dateutil.relativedelta import relativedelta 
from django.utils import timezone

class Budget(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=100)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)  # Nullable for custom period
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')

    def save(self, *args, **kwargs):
        if not self.end_date or self.period != 'custom':
            self.end_date = self.calculate_end_date()
        self.amount_remaining = self.total_budget - self.amount_spent
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('account', 'name')

    def calculate_end_date(self):
        if self.period == 'daily':
            return self.start_date + timedelta(days=1)
        elif self.period == 'weekly':
            return self.start_date + timedelta(weeks=1)
        elif self.period == 'monthly':
            return self.start_date + relativedelta(months=+1)  # Use relativedelta for accurate month addition
        elif self.period == 'yearly':
            return self.start_date + relativedelta(years=+1)  # Use relativedelta for accurate year addition
        # If custom and end_date is manually set, this method won't be used to calculate end_date
        return self.end_date

    def update_amount_spent(self):
        debit_transactions_total = self.transactions.filter(
            transaction_type='debit',
            transaction_date__range=[self.start_date, self.end_date]  # Changed 'date' to 'transaction_date'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        self.amount_spent = debit_transactions_total
        self.amount_remaining = self.total_budget - self.amount_spent
        self.save()

    @property
    def remaining_budget_percentage(self):
        if self.total_budget <= 0:
            return 0  # Prevent division by zero
        percentage = (self.amount_remaining / self.total_budget) * 100
        return max(0, percentage)  # Ensure percentage is not negative
