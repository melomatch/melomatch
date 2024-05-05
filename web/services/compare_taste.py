import numpy as np
from django.db.models.query import QuerySet
from sklearn.metrics.pairwise import cosine_similarity


class CompareTasteModel:
    all_tracks: list = []

    def __init__(self, comparer, compared_to):
        self.comparer = comparer
        self.compared_to = compared_to

    def _tracks_to_vector(self, tracks: QuerySet) -> np.array:
        vector = np.zeros(len(self.all_tracks))
        for track in tracks:
            index = self.all_tracks.index(track)
            vector[index] = 1
        return vector

    def _get_users_vectors(
        self, comparer_tracks: QuerySet, compared_to_tracks: QuerySet
    ) -> tuple[np.array, np.array]:
        return self._tracks_to_vector(comparer_tracks), self._tracks_to_vector(compared_to_tracks)

    def _get_users_tracks(self) -> tuple[QuerySet, QuerySet]:
        comparer_tracks = self.comparer.tracks.all()
        compared_to_tracks = self.compared_to.tracks.all()
        self.all_tracks = list(set(list(comparer_tracks) + list(compared_to_tracks)))
        return comparer_tracks, compared_to_tracks

    def evaluate(self) -> int:
        comparer_tracks, compared_to_tracks = self._get_users_tracks()
        comparer_vector, compared_to_vector = self._get_users_vectors(
            comparer_tracks, compared_to_tracks
        )
        similarity = cosine_similarity([comparer_vector], [compared_to_vector])[0]
        return int(similarity * 100)
