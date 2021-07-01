from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_control
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Post, Comment, ClubPost
from .forms import PostForm, CommentForm, ClubForm

# Create your views here.
@login_required(login_url="users:login")
def index(request):
    posts =  Post.objects.filter(grp_name=None).order_by("-date_posted")

    return render(request, "post/index.html", {
        "posts" : posts,
        "message": "No posts yet!. Be the first one to post!!",
        "index" : True,
        "empty_msg" : "Add Post"
    })

@login_required(login_url="users:login")
def my_posts(request):
    posts =  request.user.posts.all().order_by("-date_posted")
    
    return render(request, "post/index.html", {
        "posts" : posts,
        "message": "You haven't posted anything yet. Add your first post!!",
        "index" : False,
        "empty_msg" : "Add Post" 
    })

@login_required(login_url="users:login")
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            x = form.save(commit=False)
            x.author = request.user
            x.save()
            messages.success(request, "Sucessfully added post")
            return redirect(reverse("post:index"))
        messages.error(request, "Error! adding post")
    else:
        form = PostForm()
    return render(request, "post/add_post.html", {
        "form" : form
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="users:login")
def view_post(request, post_id):
    post = Post.objects.all().filter(pk=post_id)
    if not len(post):
        messages.warning(request, "The post you are searching for has been deleted!")
        return redirect(reverse("post:index"))
    
    post = post[0]

    comments = post.comments.all().order_by("-commented_on")
    liked_users = post.liked_users.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            x = form.save(commit=False)
            x.user = request.user
            x.post = post
            x.save()
            messages.success(request, "Sucessfully added comment")
            return redirect(reverse("post:view_post", args=(post_id,)))
        messages.error(request, "Error! adding comment")

    else:
        form = CommentForm()

    return render(request, "post/view_post.html", {
        "post" : post,
        "comments" : comments,
        "form" : form ,
        "liked_users" : liked_users,
        "no_liked" : len(liked_users)
    })  

@login_required(login_url="users:login")
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post not in request.user.posts.all():
        raise PermissionDenied
    
    post.delete()
    messages.success(request, "Sucessfully deleted post")
    return redirect(reverse("post:index"))

@login_required(login_url="users:login")
def delete_comment(request, comment_id, post_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment not in request.user.comments.all():
        raise PermissionDenied

    comment.delete()
    messages.success(request, "Sucessfully deleted comment")
    return redirect(reverse("post:view_post", args=(post_id,)))

@login_required(login_url="users:login")
def ajax_posts(request):
    posts =  Post.objects.all().order_by("-date_posted")
    temp = loader.get_template('post/ajax_posts.html')
    context = {
        "posts" : posts
    }
    if request.is_ajax():
        return HttpResponse(temp.render(context, request), content_type='application/xhtml+xml')
    
    return redirect(reverse("post:index"))

@login_required(login_url="users:login")
def ajax_comments(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = post.comments.all().order_by("-commented_on")
    temp = loader.get_template('post/ajax_comments.html')
    context = {
        "post" : post,
        "comments" : comments
    }
    if request.is_ajax():
        return HttpResponse(temp.render(context, request), content_type='application/xhtml+xml')
    
    return redirect(reverse("post:view_post", args=(post_id,)))

@login_required(login_url="users:login")
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    liked = post.liked_users.all()
    
    if request.method == "POST":
        if(request.POST["type"]== 'like'):
            if request.user not in liked:
                post.liked_users.add(request.user)
        else:
            if request.user in liked:
                post.liked_users.remove(request.user)

        if request.is_ajax():
            liked = post.liked_users.all()
            temp = loader.get_template('post/ajax_like.html')
            context = {
                "post" : post,
                "no_liked" : len(liked),
                "liked_users" : liked 
            }
            return HttpResponse(temp.render(context, request))

          
    return redirect(reverse("post:view_post", args=(post_id,)))

@method_decorator(login_required, name='dispatch')
class LikedPostView(View):
    template_name = "post/index.html"
    def get(self, request, *args, **kwargs):
        posts =  request.user.liked_posts.all().order_by("-date_posted")
    
        return render(request, self.template_name, {
            "posts" : posts,
            "message": "You haven't liked any post yet!",
            "index" : False,
            "empty_btn_url" : "post:index",
            "empty_msg" : "Posts" 
        })

@method_decorator(login_required, name='dispatch')
class CreateClubView(View):
    form = ClubForm
    template_name = "post/add_club.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied

        return render(request, self.template_name, {
            "form" : self.form()
        })

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied

        form = self.form(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.created_by = request.user
            s.save()
            s.mbr_usrs.add(request.user)
            messages.success(request, f"Successfully created group {s.name}")
            return redirect(reverse("post:view_groups"))
        
        return render(request, self.template_name, {
            "form" : form
        })

@method_decorator(login_required, name='dispatch')
class ViewClubs(View):
    template_name = "post/view_grps.html"

    def get(self, request, *args, **kwargs):
        grps = ClubPost.objects.all()
        return render(request, self.template_name, {
            "groups" : grps
        })

@method_decorator(login_required, name='dispatch')
class ClubPage(View):
    template_name = "post/index.html"

    def get(self, request, club_name, *args, **kwargs):
        grp = get_object_or_404(ClubPost, name=club_name)
        posts = grp.group_posts.all().order_by("-date_posted")

        if request.user not in grp.mbr_usrs.all():
            messages.warning(request, "You need to join before you view the group!")
            return redirect(reverse("post:view_groups"))

        return render(request, self.template_name, {
            "posts" : posts,
            "message": "No one in the group posted anything yet. Add first post!!",
            "index" : False,
            "club_name" : grp.name,
            "empty_msg" : "Add Post"
        })

@method_decorator(login_required, name='dispatch')
class AddClubPostView(View):
    form = PostForm
    template_name = 'post/add_club_post.html'

    def get(self, request, club_name, *args, **kwargs):
        grp = get_object_or_404(ClubPost, name=club_name)
        if request.user not in grp.mbr_usrs.all():
            raise PermissionDenied

        return render(request, self.template_name, {
            "form" : self.form(),
            "club_name" : club_name
        })

    def post(self, request, club_name, *args, **kwargs):
        grp = get_object_or_404(ClubPost, name=club_name)
        form = self.form(request.POST)
        if request.user not in grp.mbr_usrs.all():
            raise PermissionDenied
        if form.is_valid():
            x = form.save(commit=False)
            x.author = request.user
            x.grp_name = grp
            x.save()
            messages.success(request, "Sucessfully added post")
            return redirect(reverse("post:view_club", args=(club_name,)))

        messages.error(request, "Error! adding post")
        return render(request, self.template_name, {
            "form" : self.form,
            "club_name" : club_name
        })

@method_decorator(login_required, name='dispatch')
class JoinLeaveClub(View):
    def get(self, request, club_name, *args, **kwargs):
        grp = get_object_or_404(ClubPost, name=club_name)
        members = grp.mbr_usrs.all()

        if request.user in members:
            grp.mbr_usrs.remove(request.user)
            messages.success(request, f"Successfully left {grp.name}")
            return redirect(reverse("post:index"))
        
        grp.mbr_usrs.add(request.user)
        messages.success(request, f"Successfully joined {grp.name}")
        return redirect(reverse("post:view_club", args=(grp.name,)))

@method_decorator(login_required, name='dispatch')
class DeleteClub(View):
    def get(self, request, club_name, *args, **kwargs):
        grp = get_object_or_404(ClubPost, name=club_name)
        if request.user == grp.created_by:
            grp.delete()
            messages.success(request, f"Successfully deleted {grp.name}")
            return redirect(reverse("post:index"))
        
        raise PermissionDenied

@method_decorator(login_required, name='dispatch')
class ClubMembersView(View):
    template_name = "post/club_members.html"
    
    def get(self, request, club_name, *args, **kwargs):
        grp = get_object_or_404(ClubPost, name=club_name)
        members = grp.mbr_usrs.all()

        return render(request, self.template_name, {
            "members" : members,
            "admin" : grp.created_by,
            "club_name" : grp.name
        })

@method_decorator(login_required, name='dispatch')
class AddRemoveMemberView(View):
    def get(self, request, club_name, user_id, *args, **kwargs):
        grp = get_object_or_404(ClubPost, name=club_name)
        mbr = User.objects.get(pk=user_id)
        if request.user != grp.created_by:
            raise PermissionDenied

        if mbr in grp.mbr_usrs.all():
            grp.mbr_usrs.remove(mbr)
            messages.success(request, f"Successfully removed {mbr.username} from {grp.name}")
        else:
            grp.mbr_usrs.add(mbr)
            messages.success(request, f"Successfully added {mbr.username} to {grp.name}")
        return redirect(reverse('post:view_club', args=(club_name,)))

@method_decorator(login_required, name='dispatch')
class AddUserToGroup(View):
    template_name = "post/add_members.html"
    def get(self, request, club_name, *args, **kwargs):
        grp = get_object_or_404(ClubPost, name=club_name)
        
        if request.user != grp.created_by:
            raise PermissionDenied
        
        add_mbr = User.objects.exclude(grps=grp)

        return render(request, self.template_name, {
            "members" : add_mbr,
            "club_name" : grp.name
        })