from django.contrib.auth.models import AbstractUser
from django.db import models

from users.enums import Sex
from web.models import Track


class User(AbstractUser):
    yandex_id = models.IntegerField(
        null=True, blank=True, unique=True, verbose_name="идентификатор в Яндексе"
    )
    username = models.CharField(max_length=150, unique=True, verbose_name="никнейм")
    first_name = models.CharField(max_length=150, verbose_name="имя")
    last_name = models.CharField(max_length=150, verbose_name="фамилия")
    email = models.EmailField(unique=True, max_length=254, verbose_name="почта")
    birthday = models.DateField(null=True, blank=True, verbose_name="дата рождения")
    sex = models.CharField(max_length=1, choices=Sex.choices, blank=True, verbose_name="пол")
    avatar = models.URLField(max_length=511, verbose_name="фотография")
    tracks = models.ManyToManyField(Track, verbose_name="треки")
    is_private = models.BooleanField(default=False, verbose_name="виден в поиске?")
    is_active_link = models.BooleanField(
        default=True, verbose_name="включена ссылка с запросом на сравнение?"
    )

    def __str__(self):
        return self.username
