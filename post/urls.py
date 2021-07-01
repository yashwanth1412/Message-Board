from django.urls import path

from . import views

app_name = "post"

urlpatterns = [
    path("", views.index, name="index"),
    path("ajax/posts", views.ajax_posts, name="ajax_getPosts"),
    path("my_posts", views.my_posts, name="my_posts"),
    path("add", views.add_post, name="add_post"),
    path("<int:post_id>", views.view_post, name="view_post"),
    path("like/<int:post_id>", views.like_post, name="like_post"),
    path("<int:post_id>/ajax/comments", views.ajax_comments, name="ajax_getComments"),
    path("delete/<int:post_id>", views.delete_post, name="delete_post"),
    path("delete/comment/<int:comment_id>/<int:post_id>", views.delete_comment, name="delete_comment"),
    path("liked_posts", views.LikedPostView.as_view(), name="liked_posts"),
    path("add_club", views.CreateClubView.as_view(), name="create_club"),
    path("view_grps", views.ViewClubs.as_view(), name="view_groups"),
    path("club/<str:club_name>", views.ClubPage.as_view(), name="view_club"),
    path("add_post/<str:club_name>", views.AddClubPostView.as_view(), name="add_club_post"),
    path("join_leave/<str:club_name>", views.JoinLeaveClub.as_view(), name="join_leave"),
    path("delete/<str:club_name>", views.DeleteClub.as_view(), name="delete_club"),
    path("members/<str:club_name>", views.ClubMembersView.as_view(), name="club_members"),
    path("remove_mbr/<str:club_name>/<int:user_id>", views.AddRemoveMemberView.as_view(), name="add_remove_user"),
    path("add_mbr/<str:club_name>", views.AddUserToGroup.as_view(), name="add_user")
]