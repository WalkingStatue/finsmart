from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'
    def ready(self):
        import transactions.signals  # Adjust the import path according to your project structure
