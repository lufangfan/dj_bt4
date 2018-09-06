
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


from accounts.utils import get_avatar_path


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to=get_avatar_path, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username




    