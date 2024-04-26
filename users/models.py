from django.contrib.auth.models import AbstractUser
from django.db import models

from users.enums import RefreshStatus, RefreshType, Service, Sex
from web.models import Track


class User(AbstractUser):
    yandex_id = models.IntegerField(
        null=True, blank=True, unique=True, verbose_name="идентификатор в Яндексе"
    )
    username = models.CharField(max_length=150, unique=True, verbose_name="имя пользователя")
    first_name = models.CharField(max_length=150, verbose_name="имя")
    last_name = models.CharField(max_length=150, verbose_name="фамилия")
    email = models.EmailField(unique=True, max_length=254, verbose_name="почта")
    birthday = models.DateField(null=True, blank=True, verbose_name="дата рождения")
    sex = models.CharField(max_length=1, choices=Sex.choices, blank=True, verbose_name="пол")
    avatar = models.URLField(max_length=511, verbose_name="фотография")
    tracks = models.ManyToManyField(Track, verbose_name="треки")
    is_private = models.BooleanField(default=False, verbose_name="скрыт в поиске?")
    is_active_link = models.BooleanField(
        default=True, verbose_name="включена ссылка с запросом на сравнение?"
    )

    def __str__(self):
        return self.username


class Token(models.Model):
    value = models.CharField(max_length=255, verbose_name="токен")
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="пользователь")
    service = models.CharField(
        max_length=15, choices=Service.choices, verbose_name="музыкальный сервис"
    )

    class Meta:
        unique_together = ("user", "service")

    def __str__(self):
        return f"Токен {self.user.username} от {self.service}: {self.value}"


class Refresh(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="пользователь")
    service = models.CharField(
        max_length=15, choices=Service.choices, verbose_name="музыкальный сервис"
    )
    type = models.CharField(
        max_length=7, choices=RefreshType.choices, verbose_name="способ обновления"
    )
    status = models.CharField(
        max_length=15,
        choices=RefreshStatus.choices,
        default=RefreshStatus.IN_PROCESS,
        verbose_name="статус обновления",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="начато в")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="изменено в")

    def __str__(self):
        return f"Обновление {self.user.username} от {self.created_at}"
