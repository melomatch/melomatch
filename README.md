## Локальный запуск

1. Склонировать репозиторий
`git clone https://github.com/melomatch/melomatch.git`
2. Создать базу данных для приложения
3. Установить библиотеки  
`poetry install`
4. Запустить скрипт  
   `python manage.py migrate`
5. Запустить веб сервер  
   `python manage.py runserver`