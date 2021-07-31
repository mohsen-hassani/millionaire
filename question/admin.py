from django.contrib import admin
from django.urls.converters import register_converter
from question.models import Question, PossibleAnswer

# Register your models here.
admin.site.register(Question)
admin.site.register(PossibleAnswer)
