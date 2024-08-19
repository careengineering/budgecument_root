from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import BankAccount, Transaction
from .forms import TransactionForm,BankAccountForm

from itertools import groupby
from operator import itemgetter


####################################################################################
# - Bank Account
class BankAccountListView(LoginRequiredMixin, ListView):
    model = BankAccount
    template_name = 'bank_accounts/bank_account_list.html'

    def get_queryset(self):
        account_holder = self.request.user.accountholder
        return BankAccount.objects.filter(account_holder=account_holder, is_active=True).order_by('bank__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bank_accounts = self.get_queryset()
        grouped_accounts = []
        for key, group in groupby(bank_accounts, key=lambda x: x.bank):
            grouped_accounts.append((key, list(group)))
        context['grouped_accounts'] = grouped_accounts
        return context


class BankAccountDetailView(LoginRequiredMixin, DetailView):
    model = BankAccount
    template_name = 'bank_accounts/bank_account_detail.html'
    context_object_name = 'bank_account'
    pk_url_kwarg = 'uid'

    def get_object(self):
        uid = self.kwargs.get('uid')
        return get_object_or_404(BankAccount, uid=uid, account_holder=self.request.user.accountholder)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bank_account = self.get_object()
        context['transactions'] = Transaction.objects.filter(
            source_account=bank_account
        ) | Transaction.objects.filter(
            destination_account=bank_account
        )
        return context


class BankAccountCreateView(LoginRequiredMixin, CreateView):
    model = BankAccount
    form_class = BankAccountForm
    template_name = 'bank_accounts/bank_account_form.html'
    success_url = reverse_lazy('bank_account_list')

    def form_valid(self, form):
        form.instance.account_holder = self.request.user.accountholder
        return super().form_valid(form)


class BankAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = BankAccount
    form_class = BankAccountForm
    template_name = 'bank_accounts/bank_account_form.html'
    success_url = reverse_lazy('bank_account_list')

    def form_valid(self, form):
        form.instance.account_holder = self.request.user.accountholder
        return super().form_valid(form)

    def get_object(self):
        uid = self.kwargs.get('uid')
        return get_object_or_404(BankAccount, uid=uid, account_holder=self.request.user.accountholder)


class BankAccountDeleteView(LoginRequiredMixin, DeleteView):
    model = BankAccount
    template_name = 'bank_accounts/bank_account_confirm_delete.html'
    success_url = reverse_lazy('bank_account_list')
    pk_url_kwarg = 'uid'

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, "Hesap başarıyla silindi.")
            return HttpResponseRedirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, e.message)
            return redirect(self.request.META.get('HTTP_REFERER'))

    def get_object(self, queryset=None):
        uid = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(BankAccount, uid=uid, account_holder=self.request.user.accountholder)


class InactiveBankAccountListView(LoginRequiredMixin, ListView):
    model = BankAccount
    template_name = 'bank_accounts/inactive_bank_account_list.html'
    context_object_name = 'inactive_bank_accounts'

    def get_queryset(self):
        account_holder = self.request.user.accountholder
        queryset = BankAccount.objects.filter(account_holder=account_holder, is_active=False).order_by('bank__name')
        return queryset





####################################################################################
# Transactions
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(source_account__account_holder=self.request.user.accountholder)


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'transaction'
    pk_url_kwarg = 'transaction_uid'

    def get_object(self):
        uid = self.kwargs.get('transaction_uid')
        return get_object_or_404(Transaction, uid=uid, source_account__account_holder=self.request.user.accountholder)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def get_form(self, form_class=None):
        form = super(TransactionCreateView, self).get_form(form_class)
        form.fields['source_account'].queryset = BankAccount.objects.filter(
            account_holder=self.request.user.accountholder)
        form.fields['destination_account'].queryset = BankAccount.objects.filter(
            account_holder=self.request.user.accountholder)
        return form

    def form_valid(self, form):
        form.instance.source_account = form.cleaned_data['source_account']
        form.instance.transaction_type = form.cleaned_data['transaction_type']
        form.instance.description = form.cleaned_data['description']
        form.instance.amount = form.cleaned_data['amount']
        form.instance.date = form.cleaned_data['date']

        if form.cleaned_data['transaction_type'] == 'transfer':
            form.instance.destination_account = form.cleaned_data['destination_account']

        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')
    pk_url_kwarg = 'transaction_uid'

    def get_object(self):
        uid = self.kwargs.get('transaction_uid')
        return get_object_or_404(Transaction, uid=uid, source_account__account_holder=self.request.user.accountholder)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')
    pk_url_kwarg = 'transaction_uid'

    def get_object(self):
        uid = self.kwargs.get('transaction_uid')
        return get_object_or_404(Transaction, uid=uid, source_account__account_holder=self.request.user.accountholder)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Get the source account of the transaction
        source_account = self.object.source_account

        # Update current_balance of the source account
        if self.object.transaction_type == 'deposit':
            source_account.current_balance -= self.object.amount
        elif self.object.transaction_type == 'withdraw':
            source_account.current_balance += self.object.amount
        elif self.object.transaction_type == 'transfer':
            source_account.current_balance += self.object.amount

            # If it's a transfer, also update the destination account's balance
            destination_account = self.object.destination_account
            destination_account.current_balance -= self.object.amount
            destination_account.save()

        source_account.save()

        # Delete the transaction object
        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())
