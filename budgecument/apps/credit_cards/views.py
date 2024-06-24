# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import CreditCard, AccountHolder
#
# @login_required(login_url='login_user')
# def credit_card_list(request):
#     account_holder = get_object_or_404(AccountHolder, user=request.user)
#     credit_cards = CreditCard.objects.filter(account_holder=account_holder)
#     return render(request, 'credit_card_list.html', {'credit_cards': credit_cards})
#
# @login_required(login_url='login_user')
# def credit_card_detail(request, pk):
#     account_holder = get_object_or_404(AccountHolder, user=request.user)
#     credit_card = get_object_or_404(CreditCard, pk=pk, account_holder=account_holder)
#     return render(request, 'credit_card_detail.html', {'credit_card': credit_card})
#
# @login_required(login_url='login_user')
# def create_credit_card(request):
#     if request.method == 'POST':
#         # Form işleme kodu
#         pass
#     else:
#         # Boş form gösterimi kodu
#         pass
#     return render(request, 'create_credit_card.html')
