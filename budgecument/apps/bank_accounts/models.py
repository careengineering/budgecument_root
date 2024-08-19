from django.core.exceptions import ValidationError
from django.db import models

from ..common.models import AccountHolder, Currency, BankName, OtherHolder

import datetime
import uuid


# - Bank Account
class BankAccount(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    bank = models.ForeignKey(BankName, on_delete=models.CASCADE)
    account_holder = models.ForeignKey(AccountHolder, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    current_balance = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bank} {self.name} - {self.currency.code}"

    def delete(self, *args, **kwargs):
        if self.current_balance != 0:
            raise ValidationError("Hesap silinemez. Mevcut bakiye sıfır değil.")
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Banka Hesabı"
        verbose_name_plural = "Banka Hesapları"

    @property
    def has_transactions(self):
        return Transaction.objects.filter(source_account=self).exists() or Transaction.objects.filter(destination_account=self).exists()










# - Transaction
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Gelen'),
        ('withdraw', 'Giden'),
        ('transfer', 'Transfer'),
    ]

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    source_account = models.ForeignKey(BankAccount, related_name='transactions', on_delete=models.CASCADE)
    destination_account = models.ForeignKey(BankAccount, related_name='received_transactions', on_delete=models.CASCADE,
                                            null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.datetime.now)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    amount_after_transaction = models.DecimalField(max_digits=100, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.transaction_type == 'deposit':
            self.source_account.current_balance += self.amount
        elif self.transaction_type == 'withdraw':
            self.source_account.current_balance -= self.amount
        elif self.transaction_type == 'transfer':
            if self.destination_account:
                self.source_account.current_balance -= self.amount
                self.destination_account.current_balance += self.amount
                self.destination_account.save()
        self.amount_after_transaction = self.source_account.current_balance
        self.source_account.save()
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.source_account.name}"

    class Meta:
        verbose_name = "İşlem"
        verbose_name_plural = "İşlemler"
