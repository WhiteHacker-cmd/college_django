import re
import logging
from channels import Group
from channels.sessions import channel_session
from .models import Game
from channels.auth import channel_session_user
from channels.generic.websockets import JsonWebsocketConsumer
log = logging.getLogger(__name__)


from quiz.serializers import GameSerializer, QuizSerializer
import json

class LobbyConsumer(JsonWebsocketConsumer):

    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["lobby"]

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
    
        user = self.message.user
        if user.player.is_online == False:
            user.player.is_online = True
            user.player.save(update_fields=["is_online"])
        elif user.player.mode == "J":
            user.player.mode = "F"
            user.player.save(update_fields=["mode"])
        game = Game.objects.filter(creator=self.message.user ,completed=False, winner=None, opponent=None).last()
        if game:
            game.delete()
        
        self.message.reply_channel.send({"accept": True})
        pass

    def receive(self, content, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        channel_session_user = True
 
        # get the action that's coming in
        action = content['action']
        if action == 'create':
            player = self.message.user.player
            player.mode = "J"
            player.save(update_fields=["mode"])
            
            # create a new game using the part of the channel name
          
            
            game = Game.create_new_game(self.message.user)
            game.add_quiz()
            
            game_serializer = GameSerializer(game)
            if game.opponent:
                Group('lobby').send({'text': json.dumps(game_serializer.data)})
        elif(action == "join"):
            player = self.message.user.player
            player.mode = "J"
            player.save(update_fields=["mode"])

            game = Game.objects.filter(completed=False, opponent=None, winner=None).first()
            if game:
                game.opponent = self.message.user
                game.save(update_fields=["opponent"])
                game_serializer = GameSerializer(game)
                Group('lobby').send({'text': json.dumps(game_serializer.data)})

        elif(action == "exit"):
            if self.message.user.player.mode == "J":
                self.message.user.player.mode = "F"
                game = Game.objects.filter(creator=self.message.user ,completed=False, winner=None, opponent=None).last()
            
                if game:
                    game.delete()
                self.message.user.player.save(update_fields=["mode"])

        else:
            pass
        



    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        user = self.message.user
        if user.player.is_online == True:
            user.player.is_online = False
            user.player.save(update_fields=["is_online"])
        pass




def iterator(query):
    for i in query:
        yield i



class GameConsumer(JsonWebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True
    # strict_ordering = True
    

    def connection_groups(self, **kwargs):

      
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        # this sets the game group name, so we can communicate directly with
        # those channels in the game
        return [f"game-{kwargs['game_hash']}"]

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        idk = Game.objects.get(game_hash=kwargs["game_hash"])
        qs = idk.quiz.all()[1:10]
        data = QuizSerializer(qs, many=True)
        
        
        global quizes
        quizes = iterator(data.data)


        self.message.reply_channel.send({"accept": True})

        
        pass
    

    def receive(self, content, **kwargs):

    
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        # include the Django user in the request 
        channel_session_user = True
        action = content['action']

        # handle based on the specific action called
        if action == "next":
           
            try:
                
               
                game = Game.get_game_by_hash(kwargs['game_hash'])
                
                
                
                if game.creator != self.message.user:
                   
                    self.send({'text': "nothing"})
                
                

                else:
                    quiz = next(quizes)
                    Group("game-{0}".format(kwargs['game_hash'])).send({'text': json.dumps({"game": quiz})})
                    
               
                
            except StopIteration:
                game.game_completion()
                Group("game-{0}".format(kwargs['game_hash'])).send({'text': json.dumps("stop")})

        else:
            game = Game.get_game_by_hash(kwargs['game_hash'])
            game.calculate_score(self.message.user, content['answer'], content["quiz_id"])
            game_serializer = GameSerializer(game)
          
            Group("game-{0}".format(kwargs['game_hash'])).send({'text': json.dumps({"action": "answer", "data":game_serializer.data})})
            
        

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        user = self.message.user
        if user.player.is_online == True:
            user.player.is_online = False
        elif user.player.mode == "J":
            user.player.mode = "F"
        user.player.save(update_fields=["mode", "is_online"])
        Group("game-{0}".format(kwargs['game_hash'])).send({'text': json.dumps({"action": "close", "data":f"{user} is offline"})})
        pass