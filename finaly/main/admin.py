from django.contrib import admin
from .models import *


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('sur_name', 's_types', 'start', 'finish',)
    list_display_links = ('sur_name', )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('input_name', 'point', 'question', )
    list_editable = ('point',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_name',  'types',)




