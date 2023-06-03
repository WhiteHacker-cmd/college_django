from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from quiz.models import Game, Quiz
from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from django.contrib import messages
from django.views.decorators.cache import never_cache

class HomeView(TemplateView):
    template_name = 'home.html'



class LobbyView(TemplateView):
    template_name = 'components/lobby/lobby.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LobbyView, self).dispatch(request, *args, **kwargs)
 
    def get_context_data(self, **kwargs):
        context = super(LobbyView, self).get_context_data(**kwargs)
        # get current open games to prepopulate the list
 
        # we're creating a list of games that contains just the id (for the link) and the creator
        # available_games = [{'creator': game.creator.username, 'id': game.pk} for game in Game.get_available_games()]
        # # for the player's games, we're returning a list of games with the opponent and id
        # player_games = Game.get_games_for_player(self.request.user)
 
        return context


from django.views.generic.edit import FormView
from quiz.form import GameForm
# class GameView(FormView):
#     template_name = 'game_creation.html'
#     form_class = GameForm
#     success_url = '/'

def game_view(request):
    form = GameForm(request.POST or None)
    if form.is_valid():
        obj = form.save()
        obj.add_quiz()
    return render(request, 'game_creation.html', {'form': form})


decorators = [never_cache, login_required]
@method_decorator(decorators, name="dispatch")
class GameView(TemplateView):
    template_name = 'components/game/game.html'
    game = None

    # @method_decorator(login_required, never_cache)
    def dispatch(self, request, *args, **kwargs):
        # get the game by the id
        self.game = Game.get_game_by_hash(kwargs['game_hash'])
        user = get_user(request)
        # check to see if the game is open and available for this user
        # if this player is the creator, just return
         

        if self.game.creator == user or self.game.opponent == user:

            if user == self.game.creator:
                if self.game.creator_page_visit_count == 0:
                    self.game.creator_page_visit_count += 1
                    self.game.save(update_fields=["creator_page_visit_count"])
                    return super(GameView, self).dispatch(request, *args, **kwargs)
                else:
                    messages.add_message(request, messages.ERROR, 'Sorry, You banned from the game.')
                    return redirect('/lobby/')

            elif user == self.game.opponent:
                if self.game.opponent_page_visit_count == 0:
                    self.game.opponent_page_visit_count += 1
                    self.game.save(update_fields=["opponent_page_visit_count"])
                    return super(GameView, self).dispatch(request, *args, **kwargs)
                else:
                    messages.add_message(request, messages.ERROR, 'Sorry, You banned from the game.')
                    return redirect('/lobby/')



        # if there is no opponent and the game is not yet completed,
        # set the opponent as this user
        # if not self.game.opponent and self.game.completed==False:
        #     self.game.opponent = user
        #     self.game.save()
        #     return super(GameView, self).dispatch(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, 'Sorry, the selected game is not available.')
            return redirect('/lobby/')

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        context['game'] = self.game

        return context

decorators = [never_cache, login_required]
@method_decorator(decorators, name="dispatch")
class WinnerView(TemplateView):
    template_name = "winner/winner.html"
    winner = None
    
    
    def dispatch(self, request, *args, **kwargs):
        game = Game.get_game_by_hash(kwargs["game_hash"])
        self.winner = game.winner
        return super(WinnerView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(WinnerView, self).get_context_data(**kwargs)
        context["winner"] = self.winner

        return context