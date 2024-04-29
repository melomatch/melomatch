import numpy as np
from django.db.models.query import QuerySet
from sklearn.metrics.pairwise import cosine_similarity

from users.models import User


class ModelMl:
    all_tracks: list = []

    def __init__(self, user_id_1, user_id_2):
        self.user_id_1 = user_id_1
        self.user_id_2 = user_id_2

    def tracks_to_vector(self, tracks: QuerySet) -> np.array:
        vector = np.zeros(len(self.all_tracks))
        for track in tracks:
            index = self.all_tracks.index(track)
            vector[index] = 1
        return vector

    def get_users_vectors(
        self, tracks_user_1: QuerySet, tracks_user_2: QuerySet
    ) -> tuple[np.array, np.array]:
        return self.tracks_to_vector(tracks_user_1), self.tracks_to_vector(tracks_user_2)

    def get_users_tracks(self) -> tuple[QuerySet, QuerySet]:
        tracks_user_1 = User.objects.get(id=self.user_id_1).tracks.all()
        tracks_user_2 = User.objects.get(id=self.user_id_2).tracks.all()
        self.all_tracks = list(set(list(tracks_user_1) + list(tracks_user_2)))
        return tracks_user_1, tracks_user_2

    def compare_tracks(self) -> list:
        tracks_user_1, tracks_user_2 = self.get_users_tracks()
        vector_user_1, vector_user_2 = self.get_users_vectors(tracks_user_1, tracks_user_2)
        return cosine_similarity([vector_user_1, vector_user_2])[0][1]
