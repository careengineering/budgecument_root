from django.db import models
from ..common.models import AccountHolder, Currency, BankName, OtherHolder


class CreditCard(models.Model):
    name = models.CharField(max_length=200)
    bank = models.ForeignKey(BankName, on_delete=models.CASCADE)
    account_holder = models.ForeignKey(AccountHolder, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    cutoff_day = models.IntegerField()  # Hesap kesim günü
    pay_day = models.IntegerField()  # Ödeme günü
    limit = models.DecimalField(max_digits=100, decimal_places=2)  # Kart limiti

    def __str__(self):
        return f"{self.name} - {self.bank.name} ({self.currency.code})"


    class Meta:
        verbose_name = "Kredi Kartı"
        verbose_name_plural = "Kredi Kartları"

