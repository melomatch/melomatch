from django.db import models


class UserRole(models.TextChoices):
    SUPERUSER = "superuser", "Суперпользователь"
    USER = "user", "Пользователь"
