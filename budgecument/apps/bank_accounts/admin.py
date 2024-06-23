from django.contrib import admin
from .models import BankAccount, AccountHolder, Currency

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_holder', 'currency', 'current_balance')
    search_fields = ('name', 'account_holder__user__username', 'currency__code')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(account_holder__user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.uid:
            obj.account_holder = AccountHolder.objects.get(user=request.user)
        super().save_model(request, obj, form, change)
