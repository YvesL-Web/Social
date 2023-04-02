from django.db import models
from users.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    bio=models.TextField(blank=True, null=True)
    profile_img=models.ImageField(upload_to='profile_images', default='default.jpg')
    location=models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
