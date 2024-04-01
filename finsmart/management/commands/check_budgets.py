from django.core.management.base import BaseCommand
from django.utils import timezone
from budgets.models import Budget


class Command(BaseCommand):
    help = 'Checks all budgets and resets or deletes them based on their end date and repetitiveness'

    def handle(self, *args, **options):
        for budget in Budget.objects.all():
            if budget.is_repetitive and budget.end_date and timezone.now().date() > budget.end_date:
                if budget.should_reset():
                    budget.reset_budget()
                else:
                    budget.delete()  # Be cautious with automatic deletion
            self.stdout.write(self.style.SUCCESS(f'Successfully checked budget: {budget.name}'))
