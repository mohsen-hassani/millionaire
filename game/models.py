from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import constraints
from django.utils.translation import ugettext_lazy as _
from account.models import Profile
from question.models import Question, PossibleAnswer

# Create your models here.

class Game(models.Model):
    ''' A game with 5 questions related for a user who participated in the game '''
    participant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_(
                                    'Participant'), related_name='games')
    created_date = models.DateTimeField(_('Created Date'), auto_now=False, auto_now_add=True)
    finished_date = models.DateTimeField(_('Finished Date'), null=True)

    @property
    def get_score(self):
        return self.questions.aggregate(result=Sum('final_score')).get('result')

    def __str__(self):
        return f'{self.participant.username} game created in {self.created_date}'

class GameQuestion(models.Model):
    ''' Store question and user_selected_answer for each game'''
    class Meta:
        constraints = [constraints.UniqueConstraint(fields=['game', 'question'], 
                                                    name='unique_game_quesions')]
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name=_('Game'),
                             related_name='questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_(
                                    'Question'), related_name='game_questions')
    user_answer = models.ForeignKey(PossibleAnswer, on_delete=models.CASCADE, verbose_name=_(
                                    'User answer'), related_name='game_questions', null=True)
    final_score = models.IntegerField(default=0, verbose_name=_('Final Score'), validators=[
                                 MaxValueValidator(20), MinValueValidator(0)])
