# Generated by Django 4.0 on 2022-01-11 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_survey_s_types_alter_question_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='types',
            field=models.SmallIntegerField(choices=[(3, 'Ввести свой ответ'), (1, 'Один правильный ответ'), (2, 'Несколько правильных ответов')], verbose_name='Тип вопроса'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='s_types',
            field=models.SmallIntegerField(choices=[(1, 'Тест'), (2, 'Опрос')], null=True, verbose_name='Тип опроса'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='answer_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_answer', to='main.answer'),
        ),
    ]