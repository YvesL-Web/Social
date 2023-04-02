from django.contrib.auth import get_user_model
from django.db import models
import uuid
from datetime import datetime
from users.models import User

# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.IntegerField(default=0)


   
# class Likes(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
