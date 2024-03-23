from django.db import models


class Sex(models.TextChoices):
    MALE = "M", "Мужской"
    FEMALE = "F", "Женский"
    EMPTY = "", "Не указано"
