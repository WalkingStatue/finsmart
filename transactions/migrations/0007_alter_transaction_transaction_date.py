# Generated by Django 5.0.2 on 2024-03-15 17:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_transaction_goal_alter_transaction_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
