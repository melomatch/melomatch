from django.db import models


class Track(models.Model):
    yandex_id = models.BigIntegerField(unique=True, verbose_name="идентификатор в Яндексе")
    title = models.CharField(max_length=255, verbose_name="название")
    release_date = models.DateTimeField(blank=True, null=True, verbose_name="дата выхода")
    cover = models.URLField(max_length=511, verbose_name="обложка")
    genre = models.ForeignKey(
        "Genre", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="жанр"
    )
    artists = models.ManyToManyField("Artist", verbose_name="артисты")

    class Meta:
        verbose_name = "трек"
        verbose_name_plural = "треки"

    def __str__(self):
        artists = (artist.name for artist in self.artists.all())
        return f"{self.title} - {", ".join(artists)}"


class Genre(models.Model):
    title = models.CharField(unique=True, max_length=63, verbose_name="название")

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"

    def __str__(self):
        return self.title


class Artist(models.Model):
    yandex_id = models.BigIntegerField(unique=True, verbose_name="идентификатор в Яндексе")
    name = models.CharField(max_length=255, verbose_name="имя")
    avatar = models.URLField(max_length=511, verbose_name="фотография")

    class Meta:
        verbose_name = "артист"
        verbose_name_plural = "артисты"

    def __str__(self):
        return self.name
