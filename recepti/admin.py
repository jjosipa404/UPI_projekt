from django.contrib import admin
from .models import Post, Comment

# Register your models here.
admin.site.register(Post)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'approved', 'created')
    list_filter = ('aproved', 'created')
    search_fields = ('user', 'email', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved = True)

admin.site.register(Comment)