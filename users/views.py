from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from .forms import ProfileForm, UserRegisterForm


# Create your views here.
class RegisterView(View):
    form = UserRegisterForm
    template_name = "users/register.html"
    reverse_url = "post:index"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.reverse_url))

        return render(request, self.template_name, {
            "form" : self.form()
        })

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.reverse_url))
        
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sucessfully created account")
            return redirect(reverse("users:login"))
        
        else:
            return render(request, self.template_name, {
                "form" : form
            })

class LoginView(View):
    template_name = 'users/login.html'
    reverse_url = "post:index"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.reverse_url))

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully logged in as {username}")
            return redirect(reverse(self.reverse_url))

        messages.error(request, 'Invalid Username or Password')
        return redirect(reverse("users:login"))

@method_decorator(login_required, name='dispatch')
class IndexView(View):
    form = ProfileForm
    template_name = 'users/index.html'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        form = self.form(instance=profile)

        return render(request, self.template_name, {
            "form" : form
        })

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = self.form(request.POST or None, request.FILES or None, instance=profile)

        if form.is_valid():
            edit = form.save(commit=False)
            edit.save()
            
            messages.success(request, "Sucessfully updated profile")
            return redirect(reverse("users:index"))

        else:
            messages.error(request, "Invalid profile")
            return render(request, self.template_name, {
                "form" : form
            })

class LogOutView(View):
    redirect_url = "users:login"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You are not logged in")
            return redirect(reverse(self.redirect_url))

        logout(request)

        messages.success(request, "Successfully logged out")
        return redirect(reverse(self.redirect_url))