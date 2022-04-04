from django.db.models import Sum

from .models import Answer, UserAnswer, Question


def _possible_answer(answer_id):
    answer = Answer.objects.get(pk=answer_id)
    if answer.possible_answer == 1:
        return True
    else:
        return False


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


def _all_points_in_survey(survey_id):
    answers_point = Answer.objects.filter(question__question_in_survey=survey_id)
    answers_total_sum = answers_point.aggregate(total_sum=Sum('point'))
    return answers_total_sum['total_sum']
