from django import forms
from .models import BankAccount, BankTransaction

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name', 'bank', 'currency', 'current_balance']

class BankTransactionForm(forms.ModelForm):
    class Meta:
        model = BankTransaction
        fields = ['source_account', 'destination_account', 'transaction_type', 'description', 'amount', 'date','account_holder']
