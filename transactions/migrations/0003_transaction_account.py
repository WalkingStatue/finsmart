# Generated by Django 5.0.2 on 2024-02-22 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_profile_completed'),
        ('transactions', '0002_category_account_alter_category_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.account'),
            preserve_default=False,
        ),
    ]