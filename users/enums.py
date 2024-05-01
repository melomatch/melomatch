from django.db import models


class Sex(models.TextChoices):
    MALE = "M", "Мужской"
    FEMALE = "F", "Женский"
    EMPTY = "", "Не указано"


class Service(models.TextChoices):
    VK = "VK", "ВКонтакте"
    YANDEX = "Yandex", "Яндекс"


class RefreshType(models.TextChoices):
    AUTO = "auto", "автоматически"
    MANUAL = "manual", "вручную"


class RefreshStatus(models.TextChoices):
    IN_PROCESS = "in_process", "в процессе"
    FINISHED = "finished", "завершено"
