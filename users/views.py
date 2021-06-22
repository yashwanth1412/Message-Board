from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from .forms import ProfileForm, UserRegisterForm

# Create your views here.



@login_required(login_url="users:login")
def index(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        print(request.POST)
        form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
        
        if form.is_valid():
            edit = form.save(commit=False)
            edit.save()
            
            messages.success(request, "Sucessfully updated profile")
            return redirect(reverse("users:index"))
        else:
            messages.error(request, "Invalid profile")
            return render(request, 'users/index.html', {
                "form" : form
            })

    return render(request, 'users/index.html', {
        "form" : form
    })


def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse("post:index"))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("post:index"))
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect(reverse("users:login"))

    return render(request, 'users/login.html')

def register_user(request):
    if request.user.is_authenticated:
        return redirect(reverse("post:index"))

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sucessfully created account")
            return redirect(reverse("users:login"))
        
        else:
            return render(request, "users/register.html", {
                "form" : form
            })

    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {
        "form" : form
    })

def logout_user(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in")
        return redirect(reverse("users:login"))
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect(reverse("users:login"))
