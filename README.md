#2Проект можно посмотреть тут:
http://45.136.180.68

#3Логин(пользователь с правами): 
-devuser
#3Пароль: 
-prostouser1234

Логин(обычный пользователь): devuser2

Пароль: prostouser1234

Админ понель
45.136.180.68/admin

Логин: admin

Пароль: prostoadmin1234

Для развертывания проета на локальной машине требуется:

- клонировать проект.
- выполнить команду docker-compose up
- выполнить docker exec -it {id контейнера с именем 'web'} sh
- внутри контейнера выполнить 2 команды: python manage.py migrate и python manage.py loaddata data.json

Для развертывания на вм:

- клонировать проект.
- перейти в finaly/settings.py и добавить адрес хоста в CORS_ORIGIN_WHITELIST
- выполнить команду docker-compose up
- выполнить docker exec -it {id контейнера с именем 'web'} sh
- внутри контейнера выполнить 2 команды: python manage.py migrate и python manage.py loaddata data.json

В приложении обычным пользователям можно:
- проходить опросы/тесты 
- смотреть статистику по конкретному тесту/опросу 

В приложении пользователям с правами можно:
- проходить опросы/тесты 
- смотреть статистику по конкретному тесту/опросу всех пользователей 
- отслеживать прогресс 
- учитывать ответы на опросы

Создание/удаление пользавателей и раздачи им прав возможно через админ панель,
так же и создание/удаление опросов,тестов,вопросов

Тест/опрос невозможно проходить до даты 'начала' или после того даты 'окончания'
