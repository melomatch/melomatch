from datetime import datetime, timedelta, timezone

from yandex_music import Artist as YandexArtist
from yandex_music import Track as YandexTrack

from web.models import Artist, Genre, Track


def prepare_artist(artist: YandexArtist) -> Artist:
    # Аватар может быть null, например у "Llord" (на момент 21.05.2024)
    avatar = getattr(
        artist.cover, "uri", "storage.yandexcloud.net/melomatch/default-artist-cover/%%"
    )

    return Artist(
        yandex_id=artist.id,
        name=artist.name,
        avatar=f"https://{avatar[:-3]}",
    )


def prepare_track(track: YandexTrack) -> tuple[Track | None, Genre | None, list[Artist] | None]:
    # Обычно у подкастов поле `remember_position == True`, а у треков `remember_position == False`.
    if track.remember_position:
        return None, None, None

    # Если трек удалён с площадки, то он всё равно остаётся в списке,
    # но все его поля, кроме id, равны null или [], например у id=52140954
    if track.title is None:
        return None, None, None

    album = track.albums[0]

    release_date = album.release_date or album.year
    # Дата и год выпуска альбома могут быть null, например у "Musica Francese" (id=12809165)
    if release_date:
        release_date = (
            datetime(release_date, 1, 1, tzinfo=timezone(timedelta(hours=3)))
            if isinstance(release_date, int)
            else datetime.fromisoformat(release_date)
        )

    # Жанр альбома может быть null, например у "From the Dust" (id=9310192)
    genre = album.genre or "other"
    genre = Genre(title=genre)

    artists = list(map(prepare_artist, track.artists))
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
        if track is None:
            continue

        tracks_list.append(track)
        genres_list.append(genre)
        artists_list += artists
        track_artists_map.append((track, artists))
    return tracks_list, genres_list, artists_list, track_artists_map
