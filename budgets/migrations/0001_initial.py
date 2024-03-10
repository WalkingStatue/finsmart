# Generated by Django 5.0.2 on 2024-03-10 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('total_budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_spent', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('amount_remaining', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
            ],
        ),
    ]
