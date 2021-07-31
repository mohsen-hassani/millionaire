from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from question.models import Question, PossibleAnswer

# Create your views here.

@staff_member_required
def question_list(request):
    pass
