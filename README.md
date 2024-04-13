## Локальный запуск

1. Склонировать репозиторий  
`git clone https://github.com/melomatch/melomatch.git`
2. Поднять базу данных для приложения  
`docker-compose up -d`
3. Войти в виртуальное окружение  
`poetry shell`
4. Установить библиотеки  
`poetry install`
5. Установить git-хуки  
`pre-commit install`
6. Выполнить миграции в БД  
`python manage.py migrate`
7. Запустить веб-сервер  
`python manage.py runserver`

---

Ручной запуск линтера: `ruff check --fix`

Ручной запуск линтера для HTML шаблонов: `djlint . --extension=html --reformat --lint`

Ручной запуск pre-commit хуков: `pre-commit run`