from django.db import models
from django.contrib.auth.models import User
from user.models import Player

# Create your models here.

# this model is for make quiz

class Quiz(models.Model):
    subject = models.CharField(max_length=50, null=True)
    question = models.CharField(max_length=200)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject}-{self.question}"

# this is the model for collecting game data
class Game(models.Model):

    creator_page_visit_count = models.IntegerField(default=0, null=True, blank=True)
    opponent_page_visit_count = models.IntegerField(default=0, null=True, blank=True)
    game_hash = models.CharField(null=True, blank=True, max_length=8, unique=True)
    quiz = models.ManyToManyField(Quiz, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.SET_NULL, null=True, blank=True)
    opponent = models.ForeignKey(User, related_name="opponent", on_delete=models.SET_NULL, null=True, blank=True)
    score_of_current_user = models.IntegerField(default=0)
    score_of_opponent = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    winner = models.CharField(max_length=250, null=True, blank=True)
    game_url = models.SlugField(max_length=75, blank=True, null=True)
    

    def game_completion(self):
        self.completed = True
        if self.score_of_current_user > self.score_of_opponent:
            self.winner = self.creator.username
        elif self.score_of_opponent > self.score_of_current_user:
            self.winner = self.opponent.username
        else:
            self.winner = "DRAW!!!"

        self.save(update_fields=["completed", "winner"])



    @staticmethod
    def get_game_of_user(user):
        return Game.objects.filter(creator=user)


    @staticmethod
    def get_game_by_hash(game_hash):
        try:
            return Game.objects.get(game_hash=game_hash)
        except: 
            # TODO: handle this exception
            pass

    @staticmethod
    def get_game_by_id(id):
        try:
            return Game.objects.get(pk=id)
        except:
            # TODO: Handle this Exception
            pass
    



    def add_quiz(self):
        from quiz.models import Quiz
        quizes = Quiz.objects.all()[:10]
        for i in quizes:
            self.quiz.add(i)
        self.save()


    @staticmethod
    def create_new_game(user):
        
        p = Player.objects.filter(is_online=True, mode="J").exclude(user=user).first()
        if p:
            new_game = Game(creator=user, opponent=p.user)
            new_game.save()
            return new_game

        new_game = Game(creator=user)
        new_game.save()
        return new_game




    def calculate_score(self, user, answer, quiz_id):
        if self.creator == user:
            quiz = Quiz.objects.get(id=quiz_id)
            if quiz.answer == answer:
                self.score_of_current_user += 10
                self.save(update_fields=["score_of_current_user"])
        elif self.opponent == user:
            quiz = Quiz.objects.get(id=quiz_id)
            if quiz.answer == answer:
                self.score_of_opponent += 10
                self.save(update_fields=["score_of_opponent"])
        else:
            raise "error"
            
        


    def __str__(self):
        return f"{self.pk}"
