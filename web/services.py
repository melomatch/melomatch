from datetime import datetime

from yandex_music import Artist as YandexArtist
from yandex_music import Track as YandexTrack

from web.models import Artist, Genre, Track


def get_unique_model_instances[T](instances_list: list[T], unique_field: str) -> list[T]:
    unique_instances = {}
    for instance in instances_list:
        unique_instances[getattr(instance, unique_field)] = instance

    return list(unique_instances.values())


def get_saved_instances_by_unsaved_and_unique_saved[T](
    saved_instances: list[T], unsaved_instances: list[T], unique_field: str
) -> list[T]:
    saved_instances_by_unique_field = {}
    for instance in saved_instances:
        saved_instances_by_unique_field[getattr(instance, unique_field)] = instance

    saved_instances = []
    for instance in unsaved_instances:
        saved_instances.append(saved_instances_by_unique_field[getattr(instance, unique_field)])
    return saved_instances


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
    tracks_list, genres_list, artists_list, track_artists_map = [], [], [], []
    for track, genre, artists in map(prepare_track, tracks):
        tracks_list.append(track)
        genres_list.append(genre)
        artists_list += artists
        track_artists_map.append((track, artists))
    return tracks_list, genres_list, artists_list, track_artists_map
