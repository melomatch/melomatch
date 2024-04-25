from datetime import datetime

from celery import shared_task
from yandex_music import Artist as YandexArtist
from yandex_music import Client
from yandex_music import Track as YandexTrack

from users.models import User
from web.models import Artist, Genre, Track
from web.services import get_saved_instances_by_unsaved_and_unique_saved, get_unique_model_instances


@shared_task
def load_user_tracks(token: str, user_id: int) -> None:
    client = Client(token).init()
    tracks_from_yandex = client.users_likes_tracks().fetch_tracks()
    tracks, genres, artists, track_artists_map = prepare_tracks_genres_artists_lists(
        tracks_from_yandex
    )

    saved_genres = Genre.objects.bulk_create(
        get_unique_model_instances(genres, "title"),
        update_conflicts=True,
        unique_fields=["title"],
        update_fields=["title"],
    )
    saved_artists = Artist.objects.bulk_create(
        get_unique_model_instances(artists, "yandex_id"),
        update_conflicts=True,
        unique_fields=["yandex_id"],
        update_fields=["name", "avatar"],
    )

    saved_genres = get_saved_instances_by_unsaved_and_unique_saved(saved_genres, genres, "title")
    for track, genre in zip(tracks, saved_genres, strict=False):
        track.genre = genre

    saved_tracks = Track.objects.bulk_create(
        tracks,
        update_conflicts=True,
        unique_fields=["yandex_id"],
        update_fields=["title", "release_date", "cover"],
    )

    saved_artists = get_saved_instances_by_unsaved_and_unique_saved(
        saved_artists, artists, "yandex_id"
    )
    artists_processed = 0
    track_artists = []
    for track, artists in track_artists_map:
        track_artists_count = len(artists)
        track_artists += [
            Track.artists.through(track_id=track.id, artist_id=artist.id)
            for artist in saved_artists[artists_processed : artists_processed + track_artists_count]
        ]
        artists_processed += track_artists_count
    Track.artists.through.objects.bulk_create(track_artists, ignore_conflicts=True)

    User.objects.get(id=user_id).tracks.add(*saved_tracks)


def prepare_artist(artist: YandexArtist) -> Artist:
    return Artist(
        yandex_id=artist.id,
        name=artist.name,
        avatar=f"https://{artist.cover.uri[:-3]}",
    )


def prepare_track(track: YandexTrack) -> tuple[Track | None, Genre | None, list[Artist] | None]:
    # Обычно у подкастов поле `remember_position == True`, а у треков `remember_position == False`.
    if track.remember_position:
        return None, None, None

    album = track.albums[0]

    release_date = album.release_date or album.year
    release_date = (
        datetime(album.year, 1, 1)
        if isinstance(release_date, int)
        else datetime.fromisoformat(release_date)
    )

    artists = [artist for artist in map(prepare_artist, track.artists) if artist]
    genre = Genre(title=album.genre)
    track = Track(
        yandex_id=track.id,
        title=track.title,
        release_date=release_date,
        cover=f"https://{track.cover_uri[:-3]}",
    )
    return track, genre, artists


def prepare_tracks_genres_artists_lists(
    tracks: list[Track],
) -> tuple[list[Track], list[Genre], list[Artist], list[tuple[Track, list[Artist]]]]:
    tracks_list, genres_list, artists_list, track_genre_map, track_artists_map = [], [], [], [], []
    for track, genre, artists in map(prepare_track, tracks):
        tracks_list.append(track)
        genres_list.append(genre)
        artists_list += artists
        track_genre_map.append((track, genre))
        track_artists_map.append((track, artists))
    return tracks_list, genres_list, artists_list, track_artists_map
