from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import (Player, LoggedinUser)

User = get_user_model()


def player_creator(sender, created, instance, **kwargs):
    if created:
        Player.objects.create(user=instance, mode="F", is_online=True)
        



post_save.connect(player_creator, sender=User)


@receiver(user_logged_in)
def on_user_logged_in(sender, **kwargs):
    LoggedinUser.objects.get_or_create(user=kwargs.get("user"))



@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedinUser.objects.filter(user=kwargs.get("user")).delete()