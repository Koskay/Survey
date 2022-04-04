# Generated by Django 4.0 on 2021-12-15 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_name', models.CharField(max_length=255, verbose_name='Текст ответа')),
                ('possible_answer', models.SmallIntegerField(choices=[(2, 'Неверен'), (1, 'Верен')], default=1, verbose_name='Вариант ответа')),
                ('point', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Баллы за ответ')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.SmallIntegerField(choices=[(1, 'Один правильный ответ'), (3, 'Ввести свой ответ'), (2, 'Несколько правильных ответов')], verbose_name='Тип вопроса')),
                ('question_name', models.TextField(verbose_name='Название вопроса')),
                ('image', models.ImageField(blank=True, upload_to='photo/%Y/%m/%d', verbose_name='Изображение')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=255, verbose_name='текст ответа пользователя')),
                ('possible_user_answer', models.BooleanField(default=True)),
                ('answer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answer', to='main.answer')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_question', to='main.question')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sur_name', models.CharField(max_length=100, verbose_name='Название опроса')),
                ('start', models.DateTimeField(blank=True, verbose_name='Начало опроса')),
                ('finish', models.DateTimeField(blank=True, verbose_name='Окончание опроса')),
                ('questions', models.ManyToManyField(blank=True, null=True, related_name='question_in_survey', to='main.Question', verbose_name='Вопрос')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_in_question', to='main.question', verbose_name='Вопрос'),
        ),
    ]