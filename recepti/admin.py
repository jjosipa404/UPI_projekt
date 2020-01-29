from django.contrib import admin
from .models import Post, Comment

# Register your models here.
admin.site.register(Post)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'created')
    list_filter = ('created')
    search_fields = ('user', 'email', 'content')


    

admin.site.register(Comment)