from django.core.exceptions import ValidationError
from .models import Wallet,Category,Transaction
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from accounts.models import Account

@receiver(post_save, sender=Account)
def create_default_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(account=instance, name='Cash', balance=0)


@receiver(post_save, sender=Account)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        default_categories_names = ['Groceries', 'Rent', 'Utilities', 'Entertainment','Bills', 'Other']
        default_categories = [Category(name=name, account=instance) for name in default_categories_names]
        Category.objects.bulk_create(default_categories)

@receiver(pre_save, sender=Transaction)
def handle_transaction_update(sender, instance, **kwargs):
    if instance.pk:
        # Transaction is being updated, not created
        original_instance = Transaction.objects.get(pk=instance.pk)
        instance._original_instance = original_instance.clone()

@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):
    if created:
        # Logic for new transactions
        if instance.transaction_type == 'credit':
            instance.wallet.balance += instance.amount
        else:  # 'debit'
            instance.wallet.balance -= instance.amount
        instance.wallet.save()
    else:
        # Handle updates
        original = instance._original_instance
        if original.transaction_type == 'credit':
            instance.wallet.balance -= original.amount
        else:  # 'debit'
            instance.wallet.balance += original.amount
        
        # Apply the new transaction details
        if instance.transaction_type == 'credit':
            instance.wallet.balance += instance.amount
        else:  # 'debit'
            instance.wallet.balance -= instance.amount
        instance.wallet.save()

@receiver(pre_delete, sender=Transaction)
def update_wallet_balance_on_delete(sender, instance, **kwargs):
    # Calculate the new balance to check if it would go negative
    new_balance = instance.wallet.balance - instance.amount if instance.transaction_type == 'credit' else instance.wallet.balance + instance.amount

    # Check if the new balance would be negative
    if new_balance < 0:
        # Prevent the deletion by raising an error
        raise ValidationError("Deleting this transaction would result in a negative wallet balance.")

    # If the balance check passes, proceed to update the wallet balance
    instance.wallet.balance = new_balance
    instance.wallet.save()