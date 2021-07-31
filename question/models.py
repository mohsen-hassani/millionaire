from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Question(models.Model):
    '''
    The Question model contains the question body and a 
    foreign key to the user who posted it.
    '''
    body = models.TextField(_('Question'))
    created_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5, verbose_name=_('Rating'), validators=[
                                 MaxValueValidator(20), MinValueValidator(5)])

    def __str__(self):
        return self.body

    def is_correct(self, answer):
        correct_answers = self.possible_answers.filter(is_correct=True)
        return answer in correct_answers


class PossibleAnswer(models.Model):
    '''
    The PossibleAnsewr model contains the answer body for a question
    and if this answer is correct or not, and user who posted it.
    '''
    body = models.CharField(_('Answer'), max_length=500)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 verbose_name=_('Question'), related_name='possible_answers')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Date'))

    def __str__(self):
        return self.body
