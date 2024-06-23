from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BankAccount, BankTransaction
from .forms import BankAccountForm, BankTransactionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


# - Bank Account
class BankAccountListView(LoginRequiredMixin, ListView):
    model = BankAccount
    template_name = 'bank_accounts/bank_account_list.html'

    def get_queryset(self):
        return BankAccount.objects.filter(account_holder=self.request.user.accountholder)


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
        context['transactions'] = BankTransaction.objects.filter(
            source_account=bank_account
        ) | BankTransaction.objects.filter(
            destination_account=bank_account
        )
        return context


class BankAccountCreateView(LoginRequiredMixin, CreateView):
    model = BankAccount
    fields = ['name', 'bank', 'currency', 'current_balance']
    template_name = 'bank_accounts/bank_account_form.html'
    success_url = reverse_lazy('bank_account_list')

    def form_valid(self, form):
        form.instance.account_holder = self.request.user.accountholder
        return super().form_valid(form)


class BankAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = BankAccount
    fields = ['name', 'bank', 'currency', 'current_balance']
    template_name = 'bank_accounts/bank_account_form.html'
    success_url = reverse_lazy('bank_account_list')

    def get_object(self):
        uid = self.kwargs.get('uid')
        return get_object_or_404(BankAccount, uid=uid, account_holder=self.request.user.accountholder)


class BankAccountDeleteView(LoginRequiredMixin, DeleteView):
    model = BankAccount
    template_name = 'bank_accounts/bank_account_confirm_delete.html'
    success_url = reverse_lazy('bank_account_list')

    def get_object(self):
        uid = self.kwargs.get('uid')
        return get_object_or_404(BankAccount, uid=uid, account_holder=self.request.user.accountholder)


# - Bank Transaction

class BankTransactionListView(LoginRequiredMixin, ListView):
    model = BankTransaction
    template_name = 'bank_accounts/bank_transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return BankTransaction.objects.filter(source_account__account_holder=self.request.user.accountholder) | \
               BankTransaction.objects.filter(destination_account__account_holder=self.request.user.accountholder)


class BankTransactionCreateView(LoginRequiredMixin, CreateView):
    model = BankTransaction
    form_class = BankTransactionForm
    template_name = 'bank_transaction_form.html'

    def get_initial(self):
        initial = super().get_initial()
        account_holder = get_object_or_404(AccountHolder, user=self.request.user)
        if account_holder.default_bank_account:
            initial['source_account'] = account_holder.default_bank_account
        return initial

    def form_valid(self, form):
        form.instance.transaction_person = self.request.user.account_holder  # Assuming you have a one-to-one relation with User and AccountHolder
        return super().form_valid(form)

class BankTransactionDetailView(LoginRequiredMixin, DetailView):
    model = BankTransaction
    template_name = 'bank_accounts/bank_transaction_detail.html'
    context_object_name = 'transaction'
    pk_url_kwarg = 'transaction_uid'

class BankTransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = BankTransaction
    form_class = BankTransactionForm
    template_name = 'bank_accounts/bank_transaction_form.html'
    success_url = reverse_lazy('bank_transaction_list')
    pk_url_kwarg = 'transaction_uid'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['source_account'].queryset = BankAccount.objects.filter(account_holder=self.request.user.accountholder)
        form.fields['destination_account'].queryset = BankAccount.objects.filter(account_holder=self.request.user.accountholder)
        return form

class BankTransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = BankTransaction
    template_name = 'bank_accounts/bank_transaction_confirm_delete.html'
    success_url = reverse_lazy('bank_transaction_list')
    pk_url_kwarg = 'transaction_uid'