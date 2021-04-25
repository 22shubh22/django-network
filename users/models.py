from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    connected_users = models.ManyToManyField("Profile", blank=True)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_posts")
    title = models.CharField(max_length=100) 
    text = models.TextField(max_length=500)
    image = models.ImageField(upload_to='post_image', blank=True)
    allowed_profiles = models.ManyToManyField(Profile, blank=True)
    def __str__(self):
        return self.title