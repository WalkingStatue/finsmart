# Generated by Django 5.0.2 on 2024-03-13 14:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0003_budget_end_date_budget_period_budget_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
