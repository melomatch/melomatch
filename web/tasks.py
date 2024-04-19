from datetime import datetime

import yandex_music
from celery import shared_task
from yandex_music import Album as YandexAlbum
from yandex_music import Artist as YandexArtist

from users.models import User
from web.models import Artist, Genre, Track


def get_track_artists(artists: list[YandexArtist]) -> list[Artist]:
    all_artists = []
    for artist in artists:
        try:
            artist_instance, _ = Artist.objects.get_or_create(
                yandex_id=artist.id,
                name=artist.name,
                avatar=f"https://{artist.cover.uri[:-2]}",
            )
            all_artists.append(artist_instance)
        except Exception:
            raise Exception("Artist bad information")
    return all_artists


def get_track_genres_track_release_date(albums: list[YandexAlbum]) -> (Genre, datetime):
    genres = []
    release_dates = []
    for album in albums:
        try:
            genre_instance, _ = Genre.objects.get_or_create(title=album.genre)
            genres.append(genre_instance)
            release_dates.append(datetime.fromisoformat(album.release_date))
        except Exception:
            raise Exception("Album bad information")
    return genres, min(release_dates)


@shared_task
def load_users_tracks(token: str, user_id: int) -> None:
    client = yandex_music.Client(token).init()
    tracks_from_yandex = client.users_likes_tracks().fetch_tracks()
    users_tracks = []
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
                    cover=f"https://{track.cover_uri[:-2]}",
                )

                track_instance.save()
                track_instance.artists.add(*track_artists)
                track_instance.genres.add(*track_genres)
                users_tracks.append(track_instance)
            except Exception as e:
                print(f"{e}")

    User.objects.get(id=user_id).tracks.add(*users_tracks)