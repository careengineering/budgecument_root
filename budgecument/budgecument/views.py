from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')
