from typing import Tuple, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class ContentModel:
    """Simple TF‑IDF based content‑similarity model for movies."""

    def __init__(self, max_features: int = 20000):
        self.vectorizer = TfidfVectorizer(max_features=max_features, stop_words="english")
        self.movie_embeddings = None
        self.movie_ids: np.ndarray | None = None

    def fit(self, movies: pd.DataFrame, text_column: str = "text"):
        self.movie_ids = movies["movieId"].values
        self.movie_embeddings = self.vectorizer.fit_transform(movies[text_column].values)
        return self

    def similar_movies(self, movie_id: int, movies: pd.DataFrame, top_k: int = 10) -> pd.DataFrame:
        if self.movie_embeddings is None or self.movie_ids is None:
            raise RuntimeError("Model not fitted. Call fit() first.")
        # find index of the movie
        matches = np.where(self.movie_ids == movie_id)[0]
        if len(matches) == 0:
            raise ValueError(f"Movie id {movie_id} not found in model.")
        idx = matches[0]
        sims = cosine_similarity(self.movie_embeddings[idx], self.movie_embeddings).ravel()
        # sort by similarity (exclude itself)
        order = sims.argsort()[::-1]
        order = [i for i in order if i != idx][:top_k]
        result = movies.iloc[order].copy()
        result["similarity"] = sims[order]
        return result
