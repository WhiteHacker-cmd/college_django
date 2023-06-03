from django.contrib.auth.models import User
from .models import Game, Quiz
from rest_framework import serializers
 
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'question', 'option1', 'option2', 'option3', 'option4')

        depth = 1
 
 
class GameSerializer(serializers.ModelSerializer):
    creator_username = serializers.SerializerMethodField()
    opponent_username = serializers.SerializerMethodField()
    class Meta:
        model = Game
        fields = ('id', 'game_hash', 'winner', 'creator_username', 'opponent_username', 'score_of_current_user',
                  'score_of_opponent', 'created_time', "quiz", "game_url")
        depth = 1

    def get_creator_username(self, obj):
        return obj.creator.username

    def get_opponent_username(self, obj):
        if obj.opponent:
            return obj.opponent.username
        return None