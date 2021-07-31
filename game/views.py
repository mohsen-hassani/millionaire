import random
from datetime import datetime
from django.db.models.aggregates import Sum
from django.forms.formsets import formset_factory
from question.models import Question
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.contrib import messages
from game.models import Game, GameQuestion
from game.forms import QuestionForm


# Create your views here.
def home(request):
    scores = Game.objects.values('participant__profile__surname').annotate(score=Sum('questions__final_score')).order_by('-score')[:5]
    return render(request, 'game/home.html', {'score_table': scores})


@login_required
def request_game(request):
    user = request.user

    questions_id_list = Question.objects.all().values_list('id', flat=True)
    if len(questions_id_list) < 5:
        messages.error(request, _(
            'Not enough questions available. At least 5 question needed.'), extra_tags='danger')
        return redirect('game:home')

    # Each user only can have one game in this version, but you can always extend this limitation
    # by Creating a new game for each request
    game, created = Game.objects.get_or_create(participant=user)
    if not created:
        messages.error(request, _(
            'You can only have one game in this version. Try again in future versions!'), extra_tags='danger')
        return redirect('game:home')


    random_questions_id_list = random.sample(list(questions_id_list), 5)
    random_questions = Question.objects.filter(id__in=random_questions_id_list)
    bulk_list = [GameQuestion(game=game, question=rq) for rq in random_questions]
    GameQuestion.objects.bulk_create(bulk_list)
    messages.success(request, _(
        'Your Game created successfully.'), extra_tags='success')
    return redirect('game:home')


@login_required
def play_game(request, game_id):
    game = get_object_or_404(Game, id=game_id, participant=request.user)
    if game.finished_date:
        messages.error(request, _(
            'You Finished this game and cannot enter it again. Try viewing it instead.'), extra_tags='danger')
        return redirect('game:home')
    questions = game.questions.all()
    forms = []
    if request.method == 'POST':
        for question in questions:
            form = QuestionForm( question, request.POST, prefix=question.id)
            if form.is_valid():
                form.save()
        game.finished_date = datetime.now()
        game.save()
        return redirect('game:view_game', game_id=game.id)
    else:
        for question in questions:
            form = QuestionForm(question, prefix=question.id)
            forms.append(form)
    return render(request, 'game/quiz_form.html', {'forms': forms})
    
@login_required
def view_game(request, game_id):
    game = get_object_or_404(Game, id=game_id, participant=request.user)
    if not game.finished_date:
        messages.error(request, _(
            'You haven\'t Finished this game and cannot view it. Try playing it instead.'), extra_tags='danger')
        return redirect('game:home')
    return render(request, 'game/view.html', {'game': game})
