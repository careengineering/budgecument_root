from django.contrib import admin
from .models import CreditCard, AccountHolder, Currency, BankName


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'bank', 'account_holder', 'currency', 'limit', 'cutoff_day', 'pay_day')
    search_fields = ('name', 'bank__name', 'account_holder__user__username', 'currency__code')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(account_holder__user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.account_holder = AccountHolder.objects.get(user=request.user)
        super().save_model(request, obj, form, change)
