from django.db.models.signals import post_save, pre_save
from .models import (Quiz, Game)
from .utility import unique_game_hash_generator


def game_hash_add(sender, created, instance, **kwargs):
    if created:
        instance.game_hash = unique_game_hash_generator(instance)
        instance.game_url = f"http://127.0.0.1:8080/game/{instance.game_hash}/"
    else:
        pass
        



post_save.connect(game_hash_add, sender=Game)


# def url_add(sender, instance, created, **kwargs):
#     if created:
#         instance.game_url = f"http://127.0.0.1:8080/game/{instance.id}/"
#         instance.save()






# post_save.connect(url_add, sender=Game)