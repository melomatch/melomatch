from django.contrib.auth.models import AbstractUser
from django.db import models

from web.models import Track


class User(AbstractUser):
    yandex_id = models.IntegerField(null=True, blank=True, unique=True, verbose_name="ID в Yandex")
    username = models.CharField(max_length=150, unique=True, verbose_name="Имя пользователя")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    email = models.EmailField(unique=True, max_length=254, verbose_name="Почта")
    birthday = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    sex = models.CharField(max_length=1, verbose_name="Пол")
    avatar = models.URLField(max_length=511, verbose_name="URL фотографии пользователя")
    tracks = models.ManyToManyField(Track, verbose_name="Треки")

    def __str__(self):
        return self.username
