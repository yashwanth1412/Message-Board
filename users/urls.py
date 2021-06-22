from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('login', views.login_user, name="login"),
    path('register', views.register_user, name="register"),
    path('logout', views.logout_user, name="logout"),
]