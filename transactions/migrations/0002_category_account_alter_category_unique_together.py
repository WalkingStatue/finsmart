# Generated by Django 5.0.2 on 2024-02-22 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_profile_completed'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Categories', to='accounts.account'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name', 'account')},
        ),
    ]
