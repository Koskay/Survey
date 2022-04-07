from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    """Модель опроса"""
    sur_type = {
        (1, 'Тест'),
        (2, 'Опрос')
    }
    s_types = models.SmallIntegerField(choices=sur_type, null=True, verbose_name='Тип опроса')
    sur_name = models.CharField(max_length=100, verbose_name='Название опроса')
    start = models.DateTimeField(blank=True, verbose_name='Начало опроса')
    finish = models.DateTimeField(blank=True, verbose_name='Окончание опроса')
    questions = models.ManyToManyField('Question', blank=True, null=True,
                                       related_name='question_in_survey', verbose_name='Вопрос')

    def __str__(self):
        return self.sur_name

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['s_types']


class Question(models.Model):
    """Модель вопроса"""
    q_type = {
        (1, 'Один правильный ответ'),
        (2, 'Несколько правильных ответов'),
        (3, 'Ввести свой ответ')
    }
    types = models.SmallIntegerField(choices=q_type, verbose_name='Тип вопроса')
    question_name = models.TextField(verbose_name='Название вопроса')
    image = models.ImageField(upload_to='photo/%Y/%m/%d', blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.question_name

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    """Модель ответа"""
    answer_flag = {
        (1, 'Верен'),
        (2, 'Неверен')
    }
    input_name = models.CharField(max_length=255, verbose_name='Текст ответа')
    possible_answer = models.SmallIntegerField(choices=answer_flag, default=1, verbose_name='Вариант ответа')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='answer_in_question', verbose_name='Вопрос')
    point = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Баллы за ответ')

    def __str__(self):
        return self.input_name

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-point']


class UserAnswer(models.Model):
    """Модель ответа пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_question')
    answer_id = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE, related_name='user_answer')
    answer_text = models.CharField(max_length=255, blank=True, null=True, verbose_name='текст ответа пользователя')
    possible_user_answer = models.BooleanField(default=True)

