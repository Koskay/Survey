from .models import *
from rest_framework import serializers

from .services import _possible_answer


class UserResultsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    total_sum = serializers.IntegerField()
    user_id = serializers.IntegerField()
    user_questions_count = serializers.IntegerField()
    questions_count = serializers.IntegerField()
    answer_count = serializers.IntegerField()
    user_answer_count = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff')


class StatisticSerializer(serializers.ModelSerializer):
    answer_id = serializers.SlugRelatedField(slug_field='input_name', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    question_id = serializers.SlugRelatedField(slug_field='question_name', read_only=True)

    class Meta:
        model = UserAnswer
        fields = ('question_id', 'answer_id', 'user', 'possible_user_answer', 'answer_text',)


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'

    def create(self, validated_data):
        user_answers = UserAnswer.objects.update_or_create(
            question_id=validated_data.get('question_id', None),
            user=validated_data.get('user', None),
            defaults={'answer_text': validated_data.get('answer_text')}
        )
        return user_answers


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class UserAnswersSerializer(serializers.ModelSerializer):
    answer_id = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all(), many=True)

    class Meta:
        model = UserAnswer
        fields = ('question_id', 'answer_id', 'user', 'possible_user_answer')

    def create(self, validated_data):
        UserAnswer.objects.filter(user=validated_data.get('user', None),
                                  question_id=validated_data.get('question_id', None)
                                  ).delete()
        answers = []
        true_answers_possible = Answer.objects.filter(question=validated_data['question_id'], possible_answer=1).count()
        for answer in validated_data['answer_id']:
            if not _possible_answer(answer.id) or len(validated_data['answer_id']) > true_answers_possible:
                user_answers = UserAnswer.objects.create(
                    question_id=validated_data.get('question_id', None),
                    user=validated_data.get('user', None),
                    answer_id=answer,
                    possible_user_answer=False
                    )
                answers.append(user_answers)
            else:
                user_answers = UserAnswer.objects.create(
                    question_id=validated_data.get('question_id', None),
                    user=validated_data.get('user', None),
                    answer_id=answer,
                )
                answers.append(user_answers)
        return answers

