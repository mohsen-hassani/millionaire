from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from question.models import Question, PossibleAnswer
from question.manage.forms import QuestionForm, QuestionPossibleAnswerForm, PossibleAnswerForm
from question.formsets import BasePossibleAnswerFormSet


@staff_member_required
def question_list(request):
    ''' List of all questions '''
    questions = Question.objects.all()
    for question in questions:
        question.correct_answer = question.possible_answers.filter(is_correct=True).first()
    return render(request, 'question/question_list.html', {'questions': questions})


@staff_member_required
def question_add(request):
    ''' Create a question '''
    PossibleAnswerFormset = modelformset_factory(PossibleAnswer, form=QuestionPossibleAnswerForm, 
                                                    extra=4, formset=BasePossibleAnswerFormSet)
    formset = PossibleAnswerFormset(queryset=PossibleAnswer.objects.none())
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            formset = PossibleAnswerFormset(request.POST, form_kwargs={'question': question})
            if formset.is_valid():
                question.save()
                formset.save()
                return redirect('question:question_list')
    else:
        question_form = QuestionForm()
    return render(request, 'question/form.html', {'form': question_form, 'formset': formset})


@staff_member_required
def question_edit(request, id):
    ''' Edit a question'''
    question = get_object_or_404(Question, pk=id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question:question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'form.html', {'forms': [form]})


@staff_member_required
def question_delete(request, id):
    ''' Delete a question'''
    question = get_object_or_404(Question, id=id)
    question.delete()
    return redirect('question:question_list')


@staff_member_required
def question_possibleanswers_list(request, id):
    ''' List of all possible answers for a single question '''
    question = get_object_or_404(Question, id=id)
    answers = question.possible_answers.all()
    return render(request, 'question/answer_list.html', {'answers': answers, 'question': question})


@staff_member_required
def possible_answer_add(request, id):
    ''' Get a question and add a possible_answer object to it '''
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        form = PossibleAnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('question:question_possible_answer', id=question.id)
    else:
        form = PossibleAnswerForm()
    return render(request, 'form.html', {'forms': [form]})


@staff_member_required
def set_as_correct_answer(request, id):
    ''' Get a question, clear qeustion correct answers and set new answer'''
    answer = get_object_or_404(PossibleAnswer, id=id)
    question = answer.question

    # Clear quetsion.possible_answer
    ans = question.possible_answers.filter(is_correct=True).first()
    if ans:
        ans.is_correct = False
        ans.save()

    # Set new answer
    answer.is_correct = True
    answer.save()

    return redirect('question:question_possible_answer', id=question.id)

@staff_member_required
def possible_answer_edit(request, id):
    answer = get_object_or_404(PossibleAnswer, id=id)
    if request.method == 'POST':
        form = PossibleAnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect('question:question_possible_answer', id=answer.question.id)
    else:
        form = PossibleAnswerForm(instance=answer)
    return render(request, 'form.html', {'forms': [form]})


@staff_member_required
def possible_answer_delete(request, id):
    answer = get_object_or_404(PossibleAnswer, id=id)
    answer.delete()
    return redirect('question:question_possible_answer', id=answer.question.id)

