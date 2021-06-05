from django.urls import path

from . import views

app_name = "post"

urlpatterns = [
    path("", views.index, name="index"),
    path("my_posts", views.my_posts, name="my_posts"),
    path("add", views.add_post, name="add_post"),
    path("<int:post_id>", views.view_post, name="view_post"),
    path("delete/<int:post_id>", views.delete_post, name="delete_post"),
    path("delete/comment/<int:comment_id>/<int:post_id>", views.delete_comment, name="delete_comment")
]