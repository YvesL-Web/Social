from django.contrib import admin
from .models import Post
# Register your models here.

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display=['user','created_at']

# @admin.register(Likes)
# class LikesPost(admin.ModelAdmin):
#     list_display=['user','post']