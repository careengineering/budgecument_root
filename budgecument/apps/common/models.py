from django.db import models
from django.contrib.auth.models import User

class AccountHolder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Hesap Sahibi"
        verbose_name_plural = "Hesap Sahipleri"

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)  # ISO 4217 code
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Para Birimi"
        verbose_name_plural = "Para Birimleri"


class BankName(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, default="#efefef")


    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Banka Adı"
        verbose_name_plural = "Banka Adları"


class OtherHolder(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=5)
    account_holder = models.ForeignKey(AccountHolder, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Diğer İşlem Sahibi"
        verbose_name_plural = "Diğer İşlem Sahipleri"