from django.db import models
from django.dispatch import receiver
from users.models import User
from django.db.models.signals import post_save
# Create your models here.

def user_director_path(instance, filename):
    return 'profile_images/user_{0}/{1}'.format(instance.user.username, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    bio=models.TextField(blank=True, null=True)
    profile_img=models.ImageField(upload_to=user_director_path, default='default.jpg')
    location=models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Signal 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
