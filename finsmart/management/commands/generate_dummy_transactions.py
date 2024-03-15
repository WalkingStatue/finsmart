from django.core.management.base import BaseCommand
from faker import Faker
from transactions.models import Transaction, Wallet, Category
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Generates dummy transactions'

    def handle(self, *args, **options):
        fake = Faker()
        users = User.objects.all()
        wallets = Wallet.objects.all()
        categories = Category.objects.all()
        
        for _ in range(100):  # Generate 100 dummy transactions
            transaction_type = random.choice(['debit', 'credit'])
            user = random.choice(users)
            wallet = random.choice(wallets.filter(account__user=user))
            category = random.choice(categories.filter(account__user=user))
            amount = random.uniform(10.0, 50000.0)  # Adjust the range as necessary
            description = fake.sentence(nb_words=4)
            transaction_date = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
            
            Transaction.objects.create(
                account=user.account,
                wallet=wallet,
                transaction_type=transaction_type,
                amount=amount,
                description=description,
                category=category,
                transaction_date=transaction_date
                # Omit budget and goal for simplicity; add if needed
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated dummy transactions'))
