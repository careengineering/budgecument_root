from django import forms
from .models import BankAccount, Transaction


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name', 'bank', 'currency', 'current_balance']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'source_account', 'destination_account', 'description', 'amount','date']
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'source_account': forms.Select(attrs={'class': 'form-control'}),
            'destination_account': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['destination_account'].required = False
