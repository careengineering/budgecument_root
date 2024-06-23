"""
URL configuration for budgecument project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name='index'),
    path("admin/", admin.site.urls),
    path("user_accounts/", include('apps.user_accounts.urls')),
    path("bank_accounts/", include('apps.bank_accounts.urls')),
    path("credit_cards/", include('apps.credit_cards.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
]
