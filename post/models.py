from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class ClubPost(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_groups")
    mbr_usrs = models.ManyToManyField(User, related_name="grps")

    def __str__(self):
        return f"'{self.name}' is created by {self.created_by.first_name}"

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name="posts")
    liked_users = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    grp_name = models.ForeignKey(ClubPost, related_name="group_posts", null=True, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"'{self.title}' posted by {self.author.first_name}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    message = models.CharField(max_length=200)
    commented_on = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return f"'{self.user.first_name}' commented '{self.message}' on post '{self.post.title}'"