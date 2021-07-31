from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.forms import BaseModelFormSet

class BasePossibleAnswerFormSet(BaseModelFormSet):
    def clean(self):
        '''Checks there is only one correct possible answer.'''

        if any(self.errors):
            return

        hit_is_correct_count = 0
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            is_correct = form.cleaned_data.get('is_correct')
            hit_is_correct_count += 1 if is_correct else 0
            if hit_is_correct_count > 1:
                raise ValidationError(
                    _('This version of Millionaire game, only support one\
                        correct answer for each question. Maybe you can\
                        do this in future releases!'))