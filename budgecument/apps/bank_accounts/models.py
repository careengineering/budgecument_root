from django.db import models
from django.db import transaction as db_transaction
from ..common.models import AccountHolder, Currency, BankName, OtherHolder
import uuid
import datetime


class BankAccount(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    bank = models.ForeignKey(BankName, on_delete=models.CASCADE)
    account_holder = models.ForeignKey(AccountHolder, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    current_balance = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.currency.code}"

    class Meta:
        verbose_name = "Banka Hesabı"
        verbose_name_plural = "Banka Hesapları"


class BankTransaction(models.Model):
    DEPOSIT = 1
    WITHDRAWAL = 0
    TRANSFER = 2

    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Gelen'),
        (WITHDRAWAL, 'Giden'),
        (TRANSFER, 'Transfer'),
    ]

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    source_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='source_transactions')
    destination_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE,
                                            related_name='destination_transactions', null=True, blank=True)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE_CHOICES)
    transaction_person = models.ForeignKey(OtherHolder, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=500)
    date = models.DateField(default=datetime.date.today)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_after_transaction = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Start an atomic transaction
        with db_transaction.atomic():
            if self.transaction_type == self.WITHDRAWAL:
                self.amount = -abs(self.amount)  # Ensure amount is negative
                self.amount_after_transaction = self.source_account.current_balance + self.amount
                if self.amount_after_transaction < 0:
                    raise ValueError("Insufficient funds for withdrawal.")
                self.source_account.current_balance = self.amount_after_transaction
                self.source_account.save()

            elif self.transaction_type == self.DEPOSIT:
                self.amount = abs(self.amount)  # Ensure amount is positive
                self.amount_after_transaction = self.source_account.current_balance + self.amount
                self.source_account.current_balance = self.amount_after_transaction
                self.source_account.save()

            elif self.transaction_type == self.TRANSFER:
                if not self.destination_account:
                    raise ValueError("Destination account must be set for transfer transactions.")
                if self.source_account.current_balance < self.amount:
                    raise ValueError("Insufficient funds for transfer.")

                # Decrease balance from source account
                self.source_account.current_balance -= self.amount
                self.source_account.save()

                # Increase balance in destination account
                self.destination_account.current_balance += self.amount
                self.destination_account.save()

                # Set description for the transfer
                self.description = f'Transfer to {self.destination_account.name}'
                super(BankTransaction, self).save(*args, **kwargs)

                # Create the reverse transaction for the destination account
                destination_transaction = BankTransaction(
                    source_account=self.destination_account,
                    destination_account=self.source_account,
                    transaction_type=self.DEPOSIT,
                    transaction_person=self.transaction_person,
                    description=f'Transfer from {self.source_account.name}',
                    date=self.date,
                    amount=self.amount,
                    amount_after_transaction=self.destination_account.current_balance
                )
                destination_transaction.save()

                return

            super(BankTransaction, self).save(*args, **kwargs)