from django.core.exceptions import ValidationError, PermissionDenied
from django.db import models, transaction
from django.utils import timezone
from django.db.models import F

from ..common.models import AccountHolder, Currency, BankName

import uuid

class BankAccount(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    bank = models.ForeignKey(BankName, on_delete=models.CASCADE)
    account_holder = models.ForeignKey(AccountHolder, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bank} {self.name} - {self.currency.code} (Bakiye: {self.current_balance} {self.currency.symbol})"

    def delete(self, *args, **kwargs):
        if self.current_balance != 0:
            raise PermissionDenied("Hesap silinemez. Mevcut bakiye sıfır değil.")
        if self.has_transactions:
            raise PermissionDenied("Hesap silinemez. İlişkili işlemler bulunuyor.")
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Banka Hesabı"
        verbose_name_plural = "Banka Hesapları"

    @property
    def has_transactions(self):
        return self.transactions.exists() or self.received_transactions.exists()

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Gelen'),
        ('withdraw', 'Giden'),
        ('transfer', 'Transfer'),
    ]

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    source_account = models.ForeignKey(
        BankAccount, 
        related_name='transactions', 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    destination_account = models.ForeignKey(
        BankAccount, 
        related_name='received_transactions', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_after_transaction = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def clean(self):
        # Transfer validations
        if self.transaction_type == 'transfer':
            if not self.destination_account:
                raise ValidationError("Transfer işlemleri için hedef hesap gereklidir.")
            if self.source_account.currency != self.destination_account.currency:
                raise ValidationError("Transferler yalnızca aynı para birimine sahip hesaplar arasında yapılabilir.")

        # Account validations
        if self.transaction_type in ['withdraw', 'transfer'] and self.source_account:
            if self.source_account.current_balance < self.amount:
                raise ValidationError("Yetersiz bakiye.")

        # Transaction type specific account requirements
        if self.transaction_type == 'deposit' and not self.destination_account:
            raise ValidationError("Para yatırma işlemi için hedef hesap gereklidir.")
        if self.transaction_type == 'withdraw' and not self.source_account:
            raise ValidationError("Para çekme işlemi için kaynak hesap gereklidir.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Önce validasyonları çalıştır

        with transaction.atomic():
            if self.transaction_type == 'deposit':
                self.destination_account.current_balance = F('current_balance') + self.amount
                self.destination_account.save(update_fields=['current_balance'])
                self.destination_account.refresh_from_db()
                self.amount_after_transaction = self.destination_account.current_balance
                self.source_account = None  # Depositler için kaynak hesap yok

            elif self.transaction_type == 'withdraw':
                self.source_account.current_balance = F('current_balance') - self.amount
                self.source_account.save(update_fields=['current_balance'])
                self.source_account.refresh_from_db()
                self.amount_after_transaction = self.source_account.current_balance
                self.destination_account = None  # Withdrawlar için hedef hesap yok

            elif self.transaction_type == 'transfer':
                self.source_account.current_balance = F('current_balance') - self.amount
                self.destination_account.current_balance = F('current_balance') + self.amount
                
                self.source_account.save(update_fields=['current_balance'])
                self.destination_account.save(update_fields=['current_balance'])
                
                self.source_account.refresh_from_db()
                self.amount_after_transaction = self.source_account.current_balance

            super().save(*args, **kwargs)

    def reverse_transaction(self):
        with transaction.atomic():
            if self.transaction_type == 'deposit':
                self.source_account.current_balance -= self.amount
            elif self.transaction_type == 'withdraw':
                self.source_account.current_balance += self.amount
            elif self.transaction_type == 'transfer':
                self.source_account.current_balance += self.amount
                if self.destination_account:
                    self.destination_account.current_balance -= self.amount
            
            self.source_account.save()
            if self.destination_account:
                self.destination_account.save()

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.description}"

    class Meta:
        verbose_name = "İşlem"
        verbose_name_plural = "İşlemler"