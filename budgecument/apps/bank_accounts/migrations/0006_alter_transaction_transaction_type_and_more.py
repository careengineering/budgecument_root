# Generated by Django 5.0.6 on 2024-06-25 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_accounts', '0005_banktransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('deposit', 'Gelen'), ('withdraw', 'Giden'), ('transfer', 'Transfer')], max_length=10),
        ),
        migrations.DeleteModel(
            name='BankTransaction',
        ),
    ]
