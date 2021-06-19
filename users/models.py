from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    profile_pic = models.ImageField(upload_to="profile_pics/", default="avatar.png")
    bio = models.TextField()
