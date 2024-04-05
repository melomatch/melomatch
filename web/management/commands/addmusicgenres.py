import json

from django.core.management import BaseCommand
from django.utils.translation import gettext_lazy as _

from web.models import Genre

json_obj = {
    "genres": [
        {
            "id": "rusrap",
            "title": "Русский рэп",
            "color": "#59cd9c",
            "cover": "avatars.yandex.net/get-music-misc/34161/rotor-genre-rusrap-icon/%%",
            "liked": True,
        },
        {
            "id": "rap",
            "title": "Рэп и хип-хоп",
            "color": "#59cd9c",
            "cover": "avatars.yandex.net/get-music-misc/34161/rotor-genre-rusrap-icon/%%",
            "liked": True,
        },
    ]
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        Genre.objects.all().delete()
        with open("genres-yandex.json", encoding="utf-8") as f:
            info = f.read()
            obj = json.loads(info)
        genres = [Genre(title=genre_info["title"]) for genre_info in obj["genres"]]
        Genre.objects.bulk_create(genres)
        print(_("Жанры добавлены в таблицу Genre"))
