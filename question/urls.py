from django.urls import path, include
from question import views


app_name = 'question'
urlpatterns = [
    path('manage/', include('question.manage.urls')),
]

