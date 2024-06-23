from django.urls import path, include
from . import views

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('register/', views.register_user, name='register'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('login', views.login_user,name="login"),
    path('logout', views.logout_user, name="logout"),
]
