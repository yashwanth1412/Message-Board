from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('login', views.LoginView.as_view(), name="login"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('logout', views.LogOutView.as_view(), name="logout"),
]