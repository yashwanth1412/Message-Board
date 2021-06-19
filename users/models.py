from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pics/", default="avatar.png")
    bio = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s profile" 
