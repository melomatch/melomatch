# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models

from users.enums import UserRole
from web.models import Track


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, user_role=UserRole.USER, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, user_role=UserRole.SUPERUSER, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    yandex_id = models.IntegerField(unique=True, verbose_name="ID в Yandex")
    username = models.CharField(max_length=150, unique=True, verbose_name="Имя пользователя")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    email = models.EmailField(unique=True, max_length=254, verbose_name="E-mail")
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="Дата рождения")
    sex = models.CharField(max_length=1, verbose_name="Пол")
    profile_picture = models.URLField(max_length=511, verbose_name="URL фотографии пользователя")
    user_role = models.CharField(
        choices=UserRole.choices,
        max_length=20,
        default=UserRole.USER,
        verbose_name="Роль",
    )
    track = models.ManyToManyField(Track, verbose_name="Песня")

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    @property
    def is_superuser(self):
        return self.user_role == UserRole.SUPERUSER

    @property
    def is_staff(self):
        return self.user_role == UserRole.SUPERUSER

    def __str__(self):
        return self.username
