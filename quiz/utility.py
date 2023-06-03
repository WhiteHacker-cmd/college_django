
import random
from quiz.models import Game


def random_hash_generator(length=7):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)])for _ in range(length))



def unique_game_hash_generator(instance, new_game_hash=None):
    if new_game_hash is not None:
        game_hash = new_game_hash
    else:
        game_hash = random_hash_generator()
        qs_exists = Game.objects.filter(game_hash=game_hash).exists()
        if qs_exists:
            return unique_game_hash_generator(instance, new_game_hash=game_hash)
        return game_hash
