from django.urls import path
from .views import *


urlpatterns = [
    path('surveyList/', SurveyListApi.as_view()),
    path('questions/<int:pk>/', QuestionApi.as_view()),
    path('answers/', AnswerApi.as_view()),
    path('user-answers/', AddUserAnswer.as_view()),
    path('results/<int:pk>/', ResultsApi.as_view()),
    path('user-answer-input/', AnswerInputApi.as_view()),
    path('statistic/<int:pk>/', StatisticApi.as_view()),
    path('users/', UserListAll.as_view()),
    path('user-results/<int:pk>/', UserPoints.as_view())
]
