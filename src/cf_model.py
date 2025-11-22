from typing import Dict, Tuple, List
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class SimpleCFModel:
    """Very small user‑based collaborative filtering model.

    This is NOT production‑grade but is great for a portfolio project.
    It builds a user‑item rating matrix and uses cosine similarity between
    user rows to recommend new items.
    """

    def __init__(self):
        self.user_index: Dict[int, int] = {}
        self.item_index: Dict[int, int] = {}
        self.index_user: Dict[int, int] = {}
        self.index_item: Dict[int, int] = {}
        self.ratings_matrix: np.ndarray | None = None

    def fit(self, ratings: pd.DataFrame):
        # create index mappings
        unique_users = ratings["userId"].unique()
        unique_items = ratings["movieId"].unique()
        self.user_index = {u: i for i, u in enumerate(unique_users)}
        self.item_index = {m: i for i, m in enumerate(unique_items)}
        self.index_user = {i: u for u, i in self.user_index.items()}
        self.index_item = {i: m for m, i in self.item_index.items()}

        n_users = len(unique_users)
        n_items = len(unique_items)
        mat = np.zeros((n_users, n_items), dtype=float)

        for _, row in ratings.iterrows():
            u = self.user_index[row["userId"]]
            m = self.item_index[row["movieId"]]
            mat[u, m] = float(row["rating"])

        self.ratings_matrix = mat
        return self

    def recommend_for_user(self, user_id: int, top_k: int = 10, min_rating: float = 3.0) -> List[Tuple[int, float]]:
        if self.ratings_matrix is None:
            raise RuntimeError("Model not fitted.")
        if user_id not in self.user_index:
            raise ValueError(f"Unknown user id {user_id}")

        u_idx = self.user_index[user_id]
        user_vector = self.ratings_matrix[u_idx].reshape(1, -1)

        # compute similarity to all other users
        sims = cosine_similarity(user_vector, self.ratings_matrix).ravel()
        sims[u_idx] = 0  # ignore self

        # weighted sum of ratings from similar users
        weights = sims.reshape(-1, 1)
        weighted_ratings = (self.ratings_matrix * weights).sum(axis=0)
        sim_sums = np.where(weights.sum(axis=0) == 0, 1e-8, weights.sum(axis=0))
        scores = weighted_ratings / sim_sums

        # don't recommend items the user has already rated
        already_rated = self.ratings_matrix[u_idx] > 0
        scores[already_rated] = -1

        # pick top‑k
        idxs = scores.argsort()[::-1][:top_k]
        recs = [(self.index_item[i], float(scores[i])) for i in idxs if scores[i] > 0]
        return recs
