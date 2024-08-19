from django import forms
from django.db.models import Q

from .models import BankAccount, Transaction

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name', 'bank', 'currency', 'current_balance', 'is_active']
        labels = {
            'name': 'Hesap Adı',
            'bank': 'Banka Adı',
            'currency': 'Para Birimi',
            'current_balance': 'Mevcut Bakiye',
            'is_active': 'Aktif',
        }

    def __init__(self, *args, **kwargs):
        super(BankAccountForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # Check if instance has a primary key
            if self.instance.current_balance != 0:
                self.fields['is_active'].disabled = True
            if self.instance.current_balance != 0 or self.instance.has_transactions:
                self.fields['bank'].disabled = True
                self.fields['currency'].disabled = True
                self.fields['current_balance'].disabled = True
            for field in self.fields:
                if field not in ['name', 'is_active']:
                    self.fields[field].disabled = True





class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'source_account', 'destination_account', 'description', 'amount','date']

        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_transaction_type'}),
            'source_account': forms.Select(attrs={'class': 'form-control', 'id': 'id_source_account'}),
            'destination_account': forms.Select(attrs={'class': 'form-control', 'id': 'id_destination_account'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['destination_account'].queryset = BankAccount.objects.none()  # Initially empty queryset




