from pathlib import Path
from typing import Tuple
import pandas as pd
from .config import MOVIES_PATH, RATINGS_PATH

def load_raw_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load movies and ratings from the raw data directory."""
    movies = pd.read_csv(MOVIES_PATH)
    ratings = pd.read_csv(RATINGS_PATH)
    return movies, ratings

def build_movie_text(movies: pd.DataFrame) -> pd.DataFrame:
    """
    Build a single text field per movie combining title, genres and description.
    """
    movies = movies.copy()
    movies["genres"] = movies["genres"].fillna("")
    movies["description"] = movies["description"].fillna("")
    movies["text"] = (
        movies["title"].fillna("") + " " +
        movies["genres"] + " " +
        movies["description"]
    )
    return movies
