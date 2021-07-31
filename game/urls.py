from typing import Pattern
from django.urls import path, include
from django.views.generic.base import RedirectView
from game import views

app_name = 'game'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='game:home')),
    path('game/', views.home, name='home'),
    path('game/request/', views.request_game, name='request_game'),
    path('game/<int:game_id>/play/', views.play_game, name='play_game'),
    path('game/<int:game_id>/view/', views.view_game, name='view_game'),
]
