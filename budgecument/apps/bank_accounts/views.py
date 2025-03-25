from itertools import groupby
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction as db_transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import BankAccount, Transaction
from .forms import TransactionForm, BankAccountForm





def get_destination_accounts(request, source_account_uid):
    # Kaynak hesabı uid'ye göre bul
    source_account = get_object_or_404(BankAccount, uid=source_account_uid)
    
    # Aynı para birimine sahip hesapları filtreleyin
    destination_accounts = BankAccount.objects.filter(
        account_holder=source_account.account_holder,
        currency=source_account.currency,
        is_active=True
    ).exclude(uid=source_account_uid).values('uid', 'name', 'currency__code')

    return JsonResponse(list(destination_accounts), safe=False)


####################################################################################
# - Bank Account
class BankAccountListView(LoginRequiredMixin, ListView):
    model = BankAccount
    template_name = 'bank_accounts/bank_account_list.html'

    def get_queryset(self):
        account_holder = self.request.user.accountholder
        return BankAccount.objects.filter(account_holder=account_holder).order_by('bank__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bank_accounts = self.get_queryset()

        # Aktif ve pasif hesapları ayırıyoruz
        active_accounts = bank_accounts.filter(is_active=True)
        inactive_accounts = bank_accounts.filter(is_active=False)

        # Aktif hesapları banka adına göre grupluyoruz
        grouped_active_accounts = []
        for key, group in groupby(active_accounts, key=lambda x: x.bank):
            grouped_active_accounts.append((key, list(group)))

        # Pasif hesapları banka adına göre grupluyoruz
        grouped_inactive_accounts = []
        for key, group in groupby(inactive_accounts, key=lambda x: x.bank):
            grouped_inactive_accounts.append((key, list(group)))

        # Context'e ekliyoruz
        context['grouped_active_accounts'] = grouped_active_accounts
        context['grouped_inactive_accounts'] = grouped_inactive_accounts
        
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
    
    def form_invalid(self, form):
        print(form.errors)  # Form hatalarını gör
        return super().form_invalid(form)



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
            with db_transaction.atomic():
                self.object = self.get_object()
                self.object.delete()
                messages.success(self.request, "Hesap başarıyla silindi.")
        except PermissionDenied as e:
            messages.error(self.request, str(e))
            return redirect(self.object.get_absolute_url())
        except Exception as e:
            messages.error(self.request, f"Bir hata oluştu: {str(e)}")
            return redirect(self.object.get_absolute_url())
            
        return HttpResponseRedirect(self.success_url)

    def get_object(self, queryset=None):
        uid = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(
            BankAccount,
            uid=uid,
            account_holder=getattr(self.request.user, 'accountholder', None)
        )







####################################################################################
# Transactions
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        account_holder = getattr(self.request.user, 'accountholder', None)
        return Transaction.objects.filter(
            Q(source_account__account_holder=account_holder) |
            Q(destination_account__account_holder=account_holder)
        ).select_related(
            'source_account', 
            'destination_account',
            'source_account__currency',
            'destination_account__currency'
        ).order_by('-date')

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # İşlemi yapanı kaydet
        response = super().form_valid(form)
        messages.success(self.request, "İşlem başarıyla oluşturuldu")
        return response


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')
    pk_url_kwarg = 'transaction_uid'

    def get_object(self):
        uid = self.kwargs.get('transaction_uid')
        return get_object_or_404(
            Transaction,
            uid=uid,
            source_account__account_holder=getattr(self.request.user, 'accountholder', None)
        )

    @db_transaction.atomic
    def form_valid(self, form):
        try:
            old_transaction = Transaction.objects.get(pk=self.object.pk)
            old_transaction.reverse_transaction()  # Models.py'de reverse işlemi için metod eklenmeli
            
            new_transaction = form.save(commit=False)
            new_transaction.pk = None  # Yeni bir transaction oluştur
            new_transaction.save()
            
            self.object = new_transaction
            messages.success(self.request, "İşlem başarıyla güncellendi")
            return HttpResponseRedirect(self.get_success_url())
            
        except Exception as e:
            messages.error(self.request, f"Güncelleme hatası: {str(e)}")
            return self.form_invalid(form)

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')
    pk_url_kwarg = 'transaction_uid'

    @db_transaction.atomic
    def post(self, request, *args, **kwargs):
        transaction = self.get_object()
        try:
            transaction.reverse_transaction()
            transaction.delete()
            messages.success(request, "İşlem başarıyla silindi")
        except Exception as e:
            messages.error(request, f"Silme hatası: {str(e)}")
            return redirect(transaction.get_absolute_url())
            
        return HttpResponseRedirect(self.success_url)

    def get_object(self):
        uid = self.kwargs.get('transaction_uid')
        user_accountholder = getattr(self.request.user, 'accountholder', None)
        return get_object_or_404(
            Transaction,
            Q(uid=uid) & (
                Q(source_account__account_holder=user_accountholder) |
                Q(destination_account__account_holder=user_accountholder)
            )
        )