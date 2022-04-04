from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SurveySerializer, QuestionsSerializer, AnswerSerializer, UserAnswersSerializer, \
    AnswerInputSerializer, StatisticSerializer, UserSerializer, UserResultsSerializer

from .models import *

from .services import _all_points_in_survey, _user_points_in_survey


class SurveyListApi(ListAPIView):
    """Отдает список всех опросов и тестов"""
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticated]


class UserListAll(ListAPIView):
    """Отдает список всех зарегистрированных пользователей"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AnswerApi(ListAPIView):
    """Отдает список всех ответов на вопросы"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class StatisticApi(APIView):
    """Отдает список ответов пользователей на конкретный опрос/тест"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user_answers = UserAnswer.objects.filter(question_id__question_in_survey=pk)
        serializer = StatisticSerializer(user_answers, many=True)
        return Response(serializer.data)


class UserPoints(APIView):
    """Отдает кол-во баллов,вопросов и правильных ответов на конкретный тест, для всех пользоваетелей"""

    def get(self, request, pk):
        users = User.objects.all()
        all_user_state = []
        questions = Question.objects.filter(question_in_survey=pk)
        for use in users:
            count_user_questions = 0
            count_answer_possible = 0
            user_answer_possible = 0
            result = UserAnswer.objects.filter(user=use.id, question_id__question_in_survey=pk)
            for ques in questions:
                res = result.filter(user=use.id, question_id=ques.id)
                answers = Answer.objects.filter(question=ques.id, possible_answer=1).count()
                count_answer_possible += answers
                user_answer_possible = result.filter(possible_user_answer=True).count()
                if res:
                    count_user_questions += 1
            if result:
                user_answer_possible = result.filter(possible_user_answer=True).count()
            all_user_state.append({'user_id': use.id,
                                   'total': _user_points_in_survey(use.id, pk),
                                   'total_sum': _all_points_in_survey(pk),
                                   'user_questions_count': count_user_questions,
                                   'questions_count': len(questions),
                                   'answer_count': count_answer_possible,
                                   'user_answer_count': user_answer_possible
                                   })
        serializer = UserResultsSerializer(all_user_state, many=True)
        return Response(serializer.data)


class ResultsApi(APIView):
    """Отдает кол-во баллов на конкретный тест для конкретного пользователя"""
    def get(self, request, pk):
        user_id = request.user.id
        results = {'total': _user_points_in_survey(user_id, pk),
                   'total_sum': _all_points_in_survey(pk)}
        return Response(results)


class AnswerInputApi(APIView):
    """Сохранет или обновляет ответ пользователя на конкрентый опрос"""
    def post(self, request):
        serializer = AnswerInputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)


class QuestionApi(APIView):
    """Отдает весь список вопросов"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        questions = Question.objects.filter(question_in_survey=pk)
        serializer = QuestionsSerializer(questions, many=True, ) #context={'request': request})
        return Response(serializer.data)


class AddUserAnswer(APIView):
    """Сохраняет в бд ответ конкретного пользователя на конкретный тест"""
    def post(self, request):
        serializer = UserAnswersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            print(serializer.errors)
            return Response(status=400)

