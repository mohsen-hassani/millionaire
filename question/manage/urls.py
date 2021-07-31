from django.urls import path, include
from question.manage import views


urlpatterns = [
    path('questions/', views.question_list, name='question_list'),
    path('questions/add/', views.question_add, name='question_add'),
    path('questions/<int:id>/edit/', views.question_edit, name='question_edit'),
    path('questions/<int:id>/delete/', views.question_delete, name='question_delete'),
    path('questions/<int:id>/answers/', views.question_possibleanswers_list, name='question_possible_answer'),
    path('questions/<int:id>/answers/add/', views.possible_answer_add, name='possible_answer_add'),
    path('possible-answer/<int:id>/set-correct-answer/', views.set_as_correct_answer, name='set_as_correct_answer'),
    path('possible-answer/<int:id>/edit/', views.possible_answer_edit, name='possible_answer_edit'),
    path('possible-answer/<int:id>/delete/', views.possible_answer_delete, name='possible_answer_delete'),
]

