import uuid
from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post
from users.models import User
# User=get_user_model()

# Create your models here.
class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
