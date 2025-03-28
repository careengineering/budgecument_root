from django import forms
from django.db.models import Q
from django.forms import Select
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
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.disable_fields_based_on_balance()

    def disable_fields_based_on_balance(self):
        """Hesap özelliklerini bakiye ve işlem durumuna göre kilitle"""
        if self.instance.has_transactions or self.instance.current_balance != 0:
            lock_fields = ['bank', 'currency', 'current_balance']
            for field in lock_fields:
                self.fields[field].disabled = True
                self.fields[field].help_text = "Değiştirilemez (hesapta işlem veya bakiye var)"

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'source_account', 'destination_account', 'description', 'amount', 'date']
        labels = {
            'transaction_type': 'İşlem Türü',
            'source_account': 'Kaynak Hesap',
            'destination_account': 'Hedef Hesap',
            'description': 'Açıklama',
            'amount': 'Tutar',
            'date': 'Tarih',
        }
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control', 'style': 'min-width: 200px;'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        # Varsayılan işlem türü 'deposit' (Gelen) olsun.
        kwargs['initial'].setdefault('transaction_type', 'deposit')
        
        super().__init__(*args, **kwargs)
        
        # Aktif hesapları filtrele
        active_accounts = BankAccount.objects.filter(is_active=True)
        if self.user and hasattr(self.user, 'accountholder'):
            active_accounts = active_accounts.filter(account_holder=self.user.accountholder)

        self.fields['source_account'].queryset = active_accounts
        self.fields['destination_account'].queryset = active_accounts

        # İlk yüklemede alanları dinamik olarak ayarla
        self.adjust_fields_based_on_type()

    def adjust_fields_based_on_type(self):
        # İşlem türü; POST verisi, initial ya da instance üzerinden alınır.
        transaction_type = (
            self.data.get('transaction_type') or 
            self.initial.get('transaction_type') or 
            (self.instance.transaction_type if self.instance and self.instance.pk else None)
        )
        
        if transaction_type == 'deposit':
            # Deposit: Kaynak hesap gizlenecek, hedef hesap normal görünsün.
            self.fields['source_account'].widget = forms.HiddenInput()
            self.fields['destination_account'].widget = forms.Select(attrs={'class': 'form-control'})
            self.fields['destination_account'].required = True
        elif transaction_type == 'withdraw':
            # Withdraw: Hedef hesap gizlenecek, kaynak hesap normal görünsün.
            self.fields['destination_account'].widget = forms.HiddenInput()
            self.fields['source_account'].widget = forms.Select(attrs={'class': 'form-control'})
            self.fields['source_account'].required = True
        elif transaction_type == 'transfer':
            # Transfer: Her iki alan da normal
            self.fields['source_account'].widget = forms.Select(attrs={'class': 'form-control'})
            self.fields['destination_account'].widget = forms.Select(attrs={'class': 'form-control'})
            self.fields['source_account'].required = True
            self.fields['destination_account'].required = True

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        amount = cleaned_data.get('amount')
        source = cleaned_data.get('source_account')
        destination = cleaned_data.get('destination_account')

        # Para birimi kontrolleri (transfer için)
        if transaction_type == 'transfer' and source and destination:
            if source.currency != destination.currency:
                self.add_error('destination_account', "Hesaplar farklı para birimlerine sahip")
                
        # Bakiye kontrolleri (withdraw ve transfer için)
        if transaction_type in ['withdraw', 'transfer'] and source:
            if source.current_balance < amount:
                self.add_error('amount', "Yetersiz bakiye")
                
        # Transfer için aynı hesaba gönderme kontrolü
        if transaction_type == 'transfer' and source == destination:
            self.add_error('destination_account', "Aynı hesaba transfer yapılamaz")
            
        return cleaned_data

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Tutar 0'dan büyük olmalı")
        return amount