# CineMatch – Hybrid Movie Recommendation Engine 🎬

CineMatch is a small end‑to‑end movie recommendation system built for learning and portfolio use.
It combines a **content‑based recommender** (using TF‑IDF on movie metadata) with a simple
**collaborative‑filtering style** component based on user ratings.

## Features

- Loads a small synthetic movie + ratings dataset
- Builds TF‑IDF embeddings from movie genres + description text
- Computes user preference profiles from their ratings
- Recommends top‑N movies for a given user
- Finds movies similar to a selected movie
- Simple Streamlit UI (`app/app.py`) to explore recommendations

## Project Structure

```text
cinematch/
├─ app/
│  └─ app.py           # Streamlit front‑end
├─ api/
│  └─ main.py          # Minimal FastAPI example (optional)
├─ src/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ data_prep.py
│  ├─ content_model.py
│  ├─ cf_model.py
│  ├─ hybrid_recommender.py
│  └─ eval_metrics.py
├─ data/
│  └─ raw/
│     ├─ movies.csv
│     └─ ratings.csv
├─ models/             # (not heavily used in this minimal version)
├─ requirements.txt
└─ README.md
```

## How to Run

```bash
# create and activate a virtualenv (optional but recommended)

pip install -r requirements.txt

# from the project root (where README.md is)
streamlit run app/app.py
```

Then open the URL shown in the terminal (usually http://localhost:8501).

## Notes

- The dataset is **synthetic**, generated for demonstration only.
- Everything runs locally on CPU and does **not** require a GPU.
- You can replace `data/raw/movies.csv` and `data/raw/ratings.csv` with a real dataset
  (e.g. MovieLens) as long as you keep the same column names.
