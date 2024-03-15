from django.core.management.base import BaseCommand
from faker import Faker
from transactions.models import Transaction, Wallet, Category
from django.contrib.auth.models import User
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generates dummy transactions'

    def handle(self, *args, **options):
        fake = Faker()
        users = User.objects.all()
        wallets = Wallet.objects.all()
        categories = Category.objects.all()

        for _ in range(100):  # Generate 100 dummy transactions
            user = random.choice(users)
            wallet = random.choice(wallets.filter(account__user=user))
            category = random.choice(categories.filter(account__user=user))
            amount = random.uniform(10.0, 2000.0)
            description = fake.sentence(nb_words=4)
            
            # Generate a random transaction date in the past year
            days_in_past = random.randint(1, 365)
            transaction_date = datetime.now() - timedelta(days=days_in_past)

            Transaction.objects.create(
                account=user.account,
                wallet=wallet,
                transaction_type=random.choice(['debit', 'credit']),
                amount=amount,
                description=description,
                category=category,
                transaction_date=transaction_date  # Override the default value
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated dummy transactions'))
