from django.contrib import admin
from .models import Post, Comment, ClubPost
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'author')
    list_filter = ['date_posted']
    search_fields = ['title']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(ClubPost)