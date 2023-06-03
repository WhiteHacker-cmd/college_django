
from django.urls import re_path, path
from .views.views import (HomeView, LobbyView, game_view, GameView, WinnerView)
from rest_framework.routers import DefaultRouter
from .views.api_views import (PlayerGameViewSet, CurrentUserView, AvailableGameViewSet, SingleGameViewSet)


urlpatterns = [
    re_path(r'^$', HomeView.as_view()),
    re_path(r'^lobby/$', LobbyView.as_view()),
    # path('gamecreation/', game_view),
    re_path(r'^current-user/', CurrentUserView.as_view()),
    #TODO: regular expression needed
   
    re_path(r'game/(?P<game_hash>[\w.@+-]+)/$', GameView.as_view()),
    re_path(r'game-from-id/(?P<game_hash>[\w.@+-]+)/$', SingleGameViewSet.as_view()),
    re_path(r'winner-from-hash/(?P<game_hash>[\w.@+-]+)/$', WinnerView.as_view())


]

router = DefaultRouter()
router.register(r'player-games', PlayerGameViewSet, 'player_games')
router.register(r'available-games', AvailableGameViewSet, 'available_games')
urlpatterns += router.urls


# re_path(r'^game/(?P<game_id>\d+)/$', GameView.as_view()),
# re_path(r'^game-from-id/(?P<game_id>\d+)/$', SingleGameViewSet.as_view())



# path('game/<slug:game_id>/', GameView.as_view()),
# path('game-from-id/<slug:game_id>/', SingleGameViewSet.as_view())