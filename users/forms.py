from django.forms import ModelForm, CharField, Textarea, TextInput, EmailField, EmailInput, URLField, PasswordInput, fields
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    username = CharField(widget=TextInput(attrs={'class': "form-control"}))
    email = EmailField(widget=EmailInput(attrs={'class': "form-control"}))
    password1 = CharField(widget=PasswordInput(attrs={'class': "form-control"}))
    password2 = CharField(widget=PasswordInput(attrs={'class': "form-control"}))

    class Meta:
        model =  User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(ModelForm):
    first_name = CharField(widget=TextInput(attrs={'class': "form-control"}))
    last_name = CharField(widget=TextInput(attrs={'class': "form-control", 'required' : False}))
    email = EmailField(widget=EmailInput(attrs={'class': "form-control"}))
    bio = CharField(widget=Textarea(attrs={'class': "form-control", 'spellcheck': "false"}))
    linked_in = URLField(widget=TextInput(attrs={'class': "form-control", 'required' : False}))
    class Meta:
        model =  Profile
        fields = ['profile_pic', 'first_name', 'last_name', 'email', 'bio', 'linked_in']

