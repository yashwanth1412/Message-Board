from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 100, blank=True)
    last_name = models.CharField(max_length = 100, blank=True)
    email = models.EmailField(max_length=100)
    profile_pic = models.ImageField(upload_to="profile_pics/", default="avatar.png")
    bio = models.TextField(default="No bio")
    linked_in = models.URLField(max_length=200, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile" 
