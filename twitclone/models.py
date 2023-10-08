from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import time

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_user")
    follows = models.ManyToManyField("self", 
        related_name="followed_by",
        symmetrical=False,
        blank=True)

    def __str__(self):
        return self.user.username 

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        new_profile = Profile(user=instance)
        new_profile.save()
        new_profile.follows.add(instance.profile.id)
        new_profile.save()

class Post(models.Model):
    post = models.CharField(max_length=300)
    post_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile,
        related_name="likes",
        blank=True)
    poster = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.poster} "
            f"({self.post_time:%I:%M %p %m-%d-%Y})"
        )
