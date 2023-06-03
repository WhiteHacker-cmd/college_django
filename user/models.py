from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# from django.contrib.auth.models import AbstractUser

# Create your models here.


# class User(AbstractUser):
#     username = models.CharField(max_length=50, default='Anonymaous')
#     email = models.EmailField(max_length=254, unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)



class Player(models.Model):
    MODE_CHOICES = (("J", "joined"), ("F", "free"))
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    is_online = models.BooleanField(default=False ,blank=True)
    mode = models.CharField(max_length=1, choices=MODE_CHOICES, blank=True)

    def __str__(self):
        return self.user.username


class LoggedinUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="logged_in_user", on_delete=models.CASCADE, blank=True)
    session_key = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username