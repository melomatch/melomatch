# Create your models here.
from django.db import models


class Track(models.Model):
    yandex_id = models.IntegerField(unique=True, verbose_name="ID в Yandex")
    title = models.CharField(verbose_name="Название")
    release_date = models.DateTimeField(max_length=255, verbose_name="Дата выхода")
    cover = models.URLField(max_length=511, verbose_name="URL обложки")
    genre = models.ManyToManyField("Genre", verbose_name="Жанр")
    artist = models.ManyToManyField("Artist", verbose_name="Артист")

    class Meta:
        verbose_name = "песня"
        verbose_name_plural = "песни"

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(unique=True, max_length=63, verbose_name="Жанр")

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"

    def __str__(self):
        return self.title


class Artist(models.Model):
    yandex_id = models.IntegerField(unique=True, verbose_name="ID в Yandex")
    name = models.CharField(max_length=255, verbose_name="Имя")
    avatar = models.CharField(max_length=511, verbose_name="URL фотографии профиля")

    class Meta:
        verbose_name = "артист"
        verbose_name_plural = "артисты"

    def __str__(self):
        return self.name
