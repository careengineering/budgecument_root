from django.urls import path
from . import views

urlpatterns = [
    # Bank Account URL
    path('', views.BankAccountListView.as_view(), name='bank_account_list'),
    path('detail/<uuid:uid>/', views.BankAccountDetailView.as_view(), name='bank_account_detail'),
    path('new/', views.BankAccountCreateView.as_view(), name='bank_account_create'),
    path('edit/<uuid:uid>/', views.BankAccountUpdateView.as_view(), name='bank_account_edit'),
    path('delete/<uuid:uid>/', views.BankAccountDeleteView.as_view(), name='bank_account_delete'),

    # Inactive Bank Account URL
    path('inactive/', views.InactiveBankAccountListView.as_view(), name='inactive_bank_account_list'),

    # Transaction URL
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/new/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/<uuid:transaction_uid>/', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('transactions/update/<uuid:transaction_uid>/', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('transactions/delete/<uuid:transaction_uid>/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
]
