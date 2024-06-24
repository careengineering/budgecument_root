from django.urls import path
from . import views

urlpatterns = [
# Bank Account URLs
    path('', views.BankAccountListView.as_view(), name='bank_account_list'),
    path('detail/<uuid:uid>/', views.BankAccountDetailView.as_view(), name='bank_account_detail'),
    path('new/', views.BankAccountCreateView.as_view(), name='bank_account_create'),
    path('edit/<uuid:uid>/', views.BankAccountUpdateView.as_view(), name='bank_account_edit'),
    path('delete/<uuid:uid>/', views.BankAccountDeleteView.as_view(), name='bank_account_delete'),

    # Bank Transaction URLs
    path('transactions/', views.BankTransactionListView.as_view(), name='bank_transaction_list'),
    path('transactions/create/', views.BankTransactionCreateView.as_view(), name='bank_transaction_create'),
    path('transactions/<uuid:transaction_uid>/', views.BankTransactionDetailView.as_view(), name='bank_transaction_detail'),
    path('transactions/update/<uuid:transaction_uid>/', views.BankTransactionUpdateView.as_view(),
         name='bank_transaction_update'),
    path('transactions/delete/<uuid:transaction_uid>/', views.BankTransactionDeleteView.as_view(),
         name='bank_transaction_delete'),

    path('btransactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('btransactions/new/', views.TransactionCreateView.as_view(), name='transaction-create'),

]