from typing import List, Dict, Tuple
import pandas as pd
import numpy as np

from .data_prep import load_raw_data, build_movie_text
from .content_model import ContentModel
from .cf_model import SimpleCFModel


class HybridRecommender:
    """Combine a simple CF model with a content model."""

    def __init__(self, alpha: float = 0.6):
        self.alpha = alpha
        self.movies: pd.DataFrame | None = None
        self.content_model: ContentModel | None = None
        self.cf_model: SimpleCFModel | None = None

    def fit(self):
        movies, ratings = load_raw_data()
        movies = build_movie_text(movies)
        self.movies = movies

        # content model
        cm = ContentModel()
        cm.fit(movies, text_column="text")
        self.content_model = cm

        # CF model
        cf = SimpleCFModel()
        cf.fit(ratings)
        self.cf_model = cf
        return self

    def recommend_for_user(self, user_id: int, top_k: int = 10) -> pd.DataFrame:
        if self.movies is None or self.content_model is None or self.cf_model is None:
            raise RuntimeError("Model not fitted. Call fit().")

        movies = self.movies
        # CF recommendations (movieId, score)
        cf_recs = self.cf_model.recommend_for_user(user_id, top_k=top_k * 3)
        if not cf_recs:
            # fallback: just popular movies
            popular = (
                movies[["movieId"]]
                .assign(score=1.0)
                .head(top_k)
            )
            return popular

        cf_movie_ids = [m for m, s in cf_recs]
        cf_scores = {m: s for m, s in cf_recs}

        # content‑based boost: for each candidate movie, compute similarity
        # to movies in cf list (approximate hybrid)
        sims = []
        for m_id in cf_movie_ids:
            try:
                sim_df = self.content_model.similar_movies(m_id, movies, top_k=1)
                sims.append((m_id, float(sim_df["similarity"].iloc[0])))
            except Exception:
                sims.append((m_id, 0.0))

        content_scores = {m: s for m, s in sims}

        # normalize scores
        def normalize(d: Dict[int, float]) -> Dict[int, float]:
            vals = np.array(list(d.values()))
            if (vals.max() - vals.min()) < 1e-8:
                return {k: 0.5 for k in d.keys()}
            norm_vals = (vals - vals.min()) / (vals.max() - vals.min())
            return {k: float(v) for k, v in zip(d.keys(), norm_vals)}

        cf_norm = normalize(cf_scores)
        content_norm = normalize(content_scores)

        # hybrid score
        hybrid_scores = {
            m: self.alpha * cf_norm.get(m, 0.0) + (1 - self.alpha) * content_norm.get(m, 0.0)
            for m in cf_movie_ids
        }

        ranked = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        rec_movie_ids = [m for m, s in ranked]
        rec_scores = {m: s for m, s in ranked}
        result = movies[movies["movieId"].isin(rec_movie_ids)].copy()
        result["score"] = result["movieId"].map(rec_scores)
        result = result.sort_values("score", ascending=False)
        return result

    def similar_movies(self, movie_id: int, top_k: int = 10):
        if self.movies is None or self.content_model is None:
            raise RuntimeError("Model not fitted. Call fit().")
        return self.content_model.similar_movies(movie_id, self.movies, top_k=top_k)
