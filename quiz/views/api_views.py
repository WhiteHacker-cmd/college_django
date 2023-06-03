from rest_framework.views import APIView
from rest_framework import viewsets
from quiz.serializers import (UserSerializer, GameSerializer)
from rest_framework.response import Response
from quiz.models import (Game, Quiz)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model

User = get_user_model()



class CurrentUserView(APIView):
 
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
 
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class PlayerGameViewSet(viewsets.ViewSet):
    """
    API endpoint for player games
    """
 
    def list(self, request):
        queryset = Game.get_game_of_user(self.request.user)
        serializer = GameSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class AvailableGameViewSet(viewsets.ViewSet):
    """
    API endpoint for available/open games
    """

    def list(self, request):
        queryset = Game.objects.filter(opponent=None)
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)


class SingleGameViewSet(APIView):
    """
    Get all data for a game: Game Details, Squares
    """
 
    def get(self, request, **kwargs):
        game = Game.get_game_by_hash(kwargs['game_hash'])
        game_serializer = GameSerializer(game)
        return Response(game_serializer.data)

 