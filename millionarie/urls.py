from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls', namespace='game')),
    path('', include('account.urls', namespace='account')),
    path('', include('question.urls', namespace='question')),
]
