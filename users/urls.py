from django.urls import path
from django.contrib.auth.views import PasswordChangeView

from . import views

app_name = "users"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('login', views.LoginView.as_view(), name="login"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('logout', views.LogOutView.as_view(), name="logout"),
    path('change_password', PasswordChangeView.as_view(
            template_name = "users/change_password.html",
            success_url = "/"
        ), name="change_password")
]