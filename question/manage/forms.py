from django import forms
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.utils.translation import ugettext as _
from question.models import Question, PossibleAnswer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('body', 'rating')


class QuestionPossibleAnswerForm(forms.ModelForm):
    class Meta:
        model = PossibleAnswer
        fields = ('body', 'is_correct', )

    def __init__(self, question=None, *args, **kwargs):
        super(QuestionPossibleAnswerForm, self).__init__(*args, **kwargs)
        self._question = question

    def clean(self):
        data = self.cleaned_data
        question = self._question
        if data.get('is_correct') and question and question.possible_answers.filter(is_correct=True).exists():
            raise ValidationError(
                _('This version of Millionaire game, only support one\
                    correct answer for each question. Maybe you can\
                    do this in future releases!'))
        return self.cleaned_data


    def save(self, commit=True):
        possible_answer = PossibleAnswer(**self.cleaned_data, question=self._question)
        if commit:
            possible_answer.save()
        return possible_answer


class PossibleAnswerForm(forms.ModelForm):
    class Meta:
        model = PossibleAnswer
        fields = ('body', )
