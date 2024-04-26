from celery import shared_task
from yandex_music import Client

from users.models import User
from web.models import Artist, Genre, Track
from web.services import (
    get_saved_instances_by_unsaved_and_unique_saved,
    get_unique_model_instances,
    prepare_tracks_genres_artists_lists,
)


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
