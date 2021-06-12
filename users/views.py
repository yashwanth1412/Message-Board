from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
@login_required(login_url="users:login")
def index(request):
    return render(request, 'users/index.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse("users:index"))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("users:index"))
        else:
            messages.warning(request, 'Invalid credentials')
            return render(request, 'users/login.html')

    return render(request, 'users/login.html')

@login_required(login_url="users:login")
def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect(reverse("users:login"))
