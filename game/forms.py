from django import forms
from game.models import Game, GameQuestion
from question.models import Question, PossibleAnswer


class QuestionForm(forms.Form):
    possible_answers = forms.ModelChoiceField(queryset=None, required=True, widget=forms.RadioSelect())

    def __init__(self, game_question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self._game_question = game_question
        self.fields.get('possible_answers').label = game_question.question.body
        self.fields.get('possible_answers').queryset = game_question.question.possible_answers.all()

    def save(self):
        game_question = self._game_question
        selected_answer = self.cleaned_data.get('possible_answers')
        question = game_question.question
        question_score = question.rating
        score = 0
        if question.is_correct(selected_answer):
            score = question_score
        game_question.user_answer = selected_answer
        game_question.final_score = score
        game_question.save()

    