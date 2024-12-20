# Generated by Django 5.0.6 on 2024-06-24 17:21

import datetime
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bank_accounts", "0003_alter_bankaccount_uid_banktransaction"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("deposit", "Deposit"),
                            ("withdraw", "Withdraw"),
                            ("transfer", "Transfer"),
                        ],
                        max_length=10,
                    ),
                ),
                ("description", models.CharField(max_length=255)),
                ("date", models.DateTimeField(default=datetime.datetime.now)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=100)),
                (
                    "amount_after_transaction",
                    models.DecimalField(decimal_places=2, max_digits=100),
                ),
                (
                    "destination_account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_transactions",
                        to="bank_accounts.bankaccount",
                    ),
                ),
                (
                    "source_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="bank_accounts.bankaccount",
                    ),
                ),
            ],
            options={"verbose_name": "İşlem", "verbose_name_plural": "İşlemler",},
        ),
        migrations.DeleteModel(name="BankTransaction",),
    ]
