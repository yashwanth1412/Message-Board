from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
@login_required(login_url="users:login")
def index(request):
    posts =  Post.objects.all().order_by("-date_posted")
    
    return render(request, "post/index.html", {
        "posts" : posts,
        "message": "No posts yet!. Be the first one to post!!",
        "index": True
    })

@login_required(login_url="users:login")
def my_posts(request):
    posts =  request.user.posts.all().order_by("-date_posted")
    
    return render(request, "post/index.html", {
        "posts" : posts,
        "message": "You haven't posted anything yet. Add your first post!!",
        "index": False
    })

@login_required(login_url="users:login")
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            x = form.save(commit=False)
            x.author = request.user
            x.save()
            return redirect(reverse("post:index"))
    
    else:
        form = PostForm()
    return render(request, "post/add_post.html", {
        "form" : form
    })

@login_required(login_url="users:login")
def view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all().order_by("-commented_on")

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            x = form.save(commit=False)
            x.user = request.user
            x.post = post
            x.save()
            return redirect(reverse("post:view_post", args=(post_id,)))

    else:
        form = CommentForm()

    return render(request, "post/view_post.html", {
        "post" : post,
        "comments" : comments,
        "form" : form 
    })  

@login_required(login_url="users:login")
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post not in request.user.posts.all():
        raise PermissionDenied
    
    post.delete()
    return redirect(reverse("post:index"))

@login_required(login_url="users:login")
def delete_comment(request, comment_id, post_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment not in request.user.comments.all():
        raise PermissionDenied

    
    comment.delete()
    return redirect(reverse("post:view_post", args=(post_id,)))