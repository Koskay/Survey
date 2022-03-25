from django.db.models import Sum
from rest_framework import permissions
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SurveySerializer, QuestionsSerializer, AnswerSerializer, UserAnswersSerializer, \
    AnswerInputSerializer, StatisticSerializer, UserSerializer, UserResultsSerializer

from .models import *


# def answer_save(ans_id_array, user, question):
#     """Сохраняет ответ на тест в бд если он верен, иначе игнорирует"""
#     UserAnswer.objects.filter(question_id=question,
#                               user=user).exclude(answer_id__in=ans_id_array).delete()
#     for answer in ans_id_array:
#         if UserAnswer.objects.filter(question_id=question,
#                                      answer_id=answer,
#                                      user=user).exists():
#             pass
#         else:
#             ans = Answer.objects.get(pk=answer.id)
#             if ans.possible_answer == 1:
#                 UserAnswer.objects.create(question_id=question,
#                                           answer_id=answer,
#                                           user=user)
#             else:
#                 answer = Answer.objects.filter(question=question).filter(possible_answer=1).count()
#                 if len(ans_id_array) > answer:
#                     UserAnswer.objects.filter(question_id=question,
#                                               user=user).delete()
#                     break


class SurveyListApi(ListAPIView):
    """Отдает список всех опросов и тестов"""
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticated]


class UserListAll(ListAPIView):
    """Отдает список всех зарегистрированных пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AnswerApi(ListAPIView):
    """Отдает список всех ответов на вопросы"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class StatisticApi(APIView):
    """Отдает список ответов пользователей на конкретный опрос/тест"""
    def get(self, request, pk):
        user_answers = UserAnswer.objects.filter(question_id__question_in_survey=pk)
        serializer = StatisticSerializer(user_answers, many=True)
        return Response(serializer.data)


# class UserPoints(APIView):
#     """Отдает кол-во баллов на конкретный тест, для всех пользоваетелей"""
#     def get(self, request, pk):
#         users = User.objects.all()
#         all_user_state = []
#         count = 0
#         user_input=0
#         questions = Question.objects.filter(question_in_survey=pk)
#         for use in users:
#             result = UserAnswer.objects.filter(user=use.id)
#             results = result.filter(question_id__question_in_survey=pk)
#             sur = len(Question.objects.filter(question_in_survey=pk))
#             for ques in questions:
#                 res = results.filter(user=use.id, question_id=ques)
#                 print(len(res))
#                 user_input=len(res)
#             if results.exists():
#                 res = results.aggregate(total=Sum('answer_id__point'))
#                 answers_point = Answer.objects.filter(question__question_in_survey=pk)
#                 answers_total_sum = answers_point.aggregate(total_sum=Sum('point'))
#                 all_user_state.append({'user_id': use.id,
#                                        'total': res['total'],
#                                        'total_sum': answers_total_sum['total_sum'],
#                                        'user_count': user_input,
#                                        'questions_count': sur
#                                        })
#             else:
#                 answers_point = Answer.objects.filter(question__question_in_survey=pk)
#                 answers_total_sum = answers_point.aggregate(total_sum=Sum('point'))
#                 all_user_state.append({'user_id': use.id,
#                                        'total': 0,
#                                        'total_sum': answers_total_sum['total_sum'],
#                                        'user_count': user_input,
#                                        'questions_count': sur
#                                        })
#
#         serializer = UserResultsSerializer(all_user_state, many=True)
#         return Response(serializer.data)


def _all_points_in_survey(survey_id):
    answers_point = Answer.objects.filter(question__question_in_survey=survey_id)
    answers_total_sum = answers_point.aggregate(total_sum=Sum('point'))
    return answers_total_sum['total_sum']


def _user_points_in_survey(user_id, survey_id):
    total = 0
    questions = Question.objects.filter(question_in_survey=survey_id)
    for question in questions:
        result = UserAnswer.objects.filter(user=user_id).filter(question_id=question.pk)
        answers = Answer.objects.filter(question=question.pk).filter(possible_answer=1).count()
        sum_result = result.aggregate(total=Sum('answer_id__point'))
        if sum_result['total'] and len(result) <= answers:
            total += sum_result['total']
    return total


class UserPoints(APIView):
    """Отдает кол-во баллов на конкретный тест, для всех пользоваетелей"""
    def get(self, request, pk):
        users = User.objects.all()
        all_user_state = []
        questions = Question.objects.filter(question_in_survey=pk)
        for use in users:
            #total_point = 0
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
                #res = result.aggregate(total=Sum('answer_id__point'))
                user_answer_possible = result.filter(possible_user_answer=True).count()
                #total_point = res['total']
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



# class ResultsApi(APIView):
#     """Отдает кол-во баллов на конкретный тест для конкретного пользователя"""
#     def get(self, request, pk):
#         survey = Survey.objects.get(pk=pk)
#         result = UserAnswer.objects.filter(user=request.user.id)
#         results = result.filter(question_id__question_in_survey=pk)
#         if survey.s_types == 2:
#             sur = len(Question.objects.filter(question_in_survey=pk))
#             user_input = len(results)
#             return Response({'user_count': user_input,
#                              'questions_count': sur})
#         else:
#             var = results.filter(possible_user_answer=True)
#             res = results.aggregate(total=Sum('answer_id__point'))
#             answers_point = Answer.objects.filter(question__question_in_survey=pk)
#             answers_total_sum = answers_point.aggregate(total_sum=Sum('point'))
#             ques = Question.objects.filter(question_in_survey=pk)
#             for e in ques:
#                 print(res['total'])
#                 answer = Answer.objects.filter(question=e.pk).filter(possible_answer=1).count()
#                 if results.exists() and len(results) <= answer:
#                     return Response({'total': res['total'],
#                                      'total_sum': answers_total_sum['total_sum']})
#                 else:
#                     return Response({'total': 0,
#                                      'total_sum': answers_total_sum['total_sum']})


class ResultsApi(APIView):
    """Отдает кол-во баллов на конкретный тест для конкретного пользователя"""
    def get(self, request, pk):
        user_id = request.user.id
        results = {'total': _user_points_in_survey(user_id, pk),
                   'total_sum': _all_points_in_survey(pk)}
        return Response(results)



# class AnswerInputApi(APIView):
#     """Сохраняет в бд ответ на конкретный опрос конкретного пользователя, если ранее он не был сохранен """
#     def post(self, request):
#         serializer = AnswerInputSerializer(data=request.data)
#         if serializer.is_valid():
#             s = UserAnswer.objects.filter(question_id=serializer.validated_data['question_id'],
#                                          user=serializer.validated_data['user'])
#             if s.exists():
#                 s.update(
#                                           answer_text=serializer.validated_data['answer_text'])
#                 return Response(status=204)
#             else:
#                 serializer.save()
#                 return Response(status=201)
#         else:
#             print(serializer.errors)
#             return Response(status=401)


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
        serializer = QuestionsSerializer(questions, many=True,  context={'request': request})
        return Response(serializer.data)


class AddUserAnswer(APIView):
    """Сохраняет в бд ответ конкретного пользователя на конкретный тест"""
    def post(self, request):
        serializer = UserAnswersSerializer(data=request.data)
        if serializer.is_valid():
            # ans_id_array = serializer.validated_data['answer_id']
            # user = serializer.validated_data['user']
            # question = serializer.validated_data['question_id']
            # # проверяет и сохраняет ответы в бд
            # answer_save(ans_id_array, user, question)
            serializer.save()
            return Response(status=201)
        else:
            print(serializer.errors)
            return Response(status=400)

