import datetime
from typing import List

import yandex_music
from celery import shared_task
from yandex_music import Album
from yandex_music import Artist as YandexArtist

from web.models import Artist, Genre, Track


def get_track_artists(artists: List[YandexArtist]) -> List[Artist]:
    all_artists = []
    for artist in artists:
        try:
            artist_instance = Artist.objects.get_or_create(
                yandex_id=artist.id, name=artist.name, avatar=artist.cover
            )
            all_artists.append(artist_instance[0])
        except Exception:
            raise Exception("Artist bad information")
    return all_artists


def get_track_genres_track_release_date(albums: List[Album]) -> (Genre, datetime):
    genres = []
    release_dates = []
    for album in albums:
        try:
            genre_instance = Genre.objects.get_or_create(title=album.genre)
            genres.append(genre_instance[0])
            release_dates.append(datetime.datetime.fromisoformat(album.release_date))
        except Exception:
            raise Exception("Album bad information")
    return genres, min(release_dates)


@shared_task
def load_users_tracks(token: str) -> None:
    client = yandex_music.Client(token).init()
    tracks_from_yandex = client.users_likes_tracks().fetch_tracks()
    for track in tracks_from_yandex:
        if not Track.objects.filter(yandex_id=track.id).exists():
            try:
                track_yandex_id, track_title = track.id, track.title
                track_albums, track_artists = track.albums, track.artists

                if len(track_albums) == 0:
                    raise Exception("No albums...")

                track_artists = get_track_artists(track_artists)
                track_genres, track_release_date = get_track_genres_track_release_date(track_albums)
                track_instance = Track(
                    yandex_id=track_yandex_id,
                    title=track_title,
                    release_date=track_release_date,
                    cover=track.cover_uri.replace("%%", "400x400"),
                )

                track_instance.save()
                track_instance.artists.add(*track_artists)
                track_instance.genres.add(*track_genres)
            except Exception as e:
                print(f"{e}")
