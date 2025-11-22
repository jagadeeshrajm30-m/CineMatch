import sys
from pathlib import Path
from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.hybrid_recommender import HybridRecommender
from src.data_prep import load_raw_data

app = FastAPI(title="CineMatch API")

model = HybridRecommender(alpha=0.6)
model.fit()
movies, ratings = load_raw_data()

@app.get("/")
def root():
    return {"message": "CineMatch API is running."}

@app.get("/recommend/user/{user_id}")
def recommend_user(user_id: int, k: int = 10):
    recs = model.recommend_for_user(user_id, top_k=k)
    return {
        "user_id": user_id,
        "recommendations": recs[["movieId", "title", "genres", "score"]].to_dict(orient="records"),
    }

@app.get("/similar/{movie_id}")
def similar_movies(movie_id: int, k: int = 10):
    sims = model.similar_movies(movie_id, top_k=k)
    return {
        "movie_id": movie_id,
        "similar": sims[["movieId", "title", "genres", "similarity"]].to_dict(orient="records"),
    }
