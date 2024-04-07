import json

from django.core.management import BaseCommand

from web.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("web/management/commands/genres-yandex.json", encoding="utf-8") as f:
            obj = json.load(f)
        genres = [Genre(title=genre_info["id"]) for genre_info in obj["genres"]]
        Genre.objects.bulk_create(
            genres, update_conflicts=True, update_fields=["title"], unique_fields=["title"]
        )
        print("Жанры добавлены в таблицу Genre")
