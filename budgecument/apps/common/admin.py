from django.contrib import admin
from .models import Currency, BankName, OtherHolder, AccountHolder


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "symbol")
    search_fields = ("code", "name", "symbol")


class BankNameAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(BankName, BankNameAdmin)
