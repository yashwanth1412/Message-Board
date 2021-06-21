from django.forms import ModelForm, CharField, TextInput, Textarea
from .models import Post, Comment

class PostForm(ModelForm):
    title = CharField(widget=TextInput(attrs={'class': "form-control"}))
    content = CharField(widget=Textarea(attrs={'class': "form-control"}))
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(ModelForm):
    message = CharField(widget=TextInput(attrs={'class': "form-control"}))
    class Meta:
        model = Comment
        fields = ['message']
