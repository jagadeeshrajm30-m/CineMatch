import streamlit as st
import requests

st.set_page_config(
    page_title="CineSuggest – Real-Time Movie Recs",
    page_icon="🎬",
    layout="wide",
)

# 🔴 Put your OMDb API key here
API_KEY = "28cfb0c6"
BASE_URL = "http://www.omdbapi.com/"


# ---------------- API helpers ---------------- #

def search_movies(query, page=1):
    params = {"apikey": API_KEY, "s": query, "type": "movie", "page": page}
    r = requests.get(BASE_URL, params=params, timeout=10)
    data = r.json()
    return data.get("Search", [])


def get_movie_details(imdb_id):
    params = {"apikey": API_KEY, "i": imdb_id, "plot": "short"}
    r = requests.get(BASE_URL, params=params, timeout=10)
    return r.json()


# ------------- recommendation logic ----------- #

def discover_movies(preferences, max_results=20):
    """
    Very simple discovery engine using OMDb search + filters.
    preferences = {
        "genres": [...],
        "language": "English" / "Any",
        "min_rating": float,
        "year_range": (start, end)
    }
    """
    genres = preferences["genres"]
    language = preferences["language"]
    min_rating = preferences["min_rating"]
    year_start, year_end = preferences["year_range"]

    # if no genres selected, just use a generic query
    queries = genres or ["popular", "blockbuster", "movie"]

    seen_ids = set()
    candidates = []

    # try a few pages / queries to gather enough movies
    for q in queries:
        for page in range(1, 4):  # up to 3 pages per query
            results = search_movies(q, page=page)
            if not results:
                break
            for item in results:
                imdb_id = item.get("imdbID")
                if not imdb_id or imdb_id in seen_ids:
                    continue
                seen_ids.add(imdb_id)
                details = get_movie_details(imdb_id)

                # basic filtering
                try:
                    year_str = details.get("Year", "")
                    year = int(year_str.split("–")[0]) if year_str[:4].isdigit() else None
                except Exception:
                    year = None

                rating_str = details.get("imdbRating", "0")
                try:
                    rating = float(rating_str) if rating_str != "N/A" else 0.0
                except ValueError:
                    rating = 0.0

                movie_genres = details.get("Genre", "")
                movie_langs = details.get("Language", "")

                # filter by genres (all selected genres should appear)
                if genres:
                    if not all(g.lower() in movie_genres.lower() for g in genres):
                        continue

                # filter by language
                if language != "Any":
                    if language.lower() not in movie_langs.lower():
                        continue

                # filter by rating
                if rating < min_rating:
                    continue

                # filter by year
                if year is not None and not (year_start <= year <= year_end):
                    continue

                candidates.append((rating, details))

    # sort by rating desc and trim
    candidates.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in candidates[:max_results]]


# -------------------- UI --------------------- #

st.markdown(
    """
    <h1 style="text-align:center; margin-bottom:0;">🍿 CineSuggest</h1>
    <p style="text-align:center; font-size:16px; opacity:0.8; margin-top:4px;">
    Real-time movie suggestions powered by OMDb – no training, just live data.
    </p>
    """,
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["✨ Personalized Discovery", "🎯 Movie Details & Similar"])

# ------------- TAB 1 – Personalized Discovery --------- #

with tab1:
    st.subheader("Tell me what you like, I’ll find you movies 😌")

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("### 🎭 Genres you enjoy")
        all_genres = [
            "Action", "Adventure", "Animation", "Comedy", "Crime", "Drama",
            "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller"
        ]
        selected_genres = st.multiselect(
            "Pick a few (optional)", all_genres, default=["Action", "Drama"]
        )

        st.markdown("### 🌍 Preferred language")
        language = st.selectbox(
            "Language",
            ["Any", "English", "Hindi", "Tamil", "Telugu", "Japanese", "Korean", "French"],
            index=1,
        )

        st.markdown("### ⭐ Minimum IMDB rating")
        min_rating = st.slider("Min rating", 0.0, 9.0, 7.0, 0.1)

        st.markdown("### 📅 Year range")
        year_range = st.slider("Release year", 1980, 2024, (2000, 2024))

        max_results = st.slider("How many suggestions?", 5, 30, 12)

        go = st.button("🎬 Get movie suggestions")

    with col_right:
        if go:
            prefs = {
                "genres": selected_genres,
                "language": language,
                "min_rating": min_rating,
                "year_range": year_range,
            }
            with st.spinner("Looking for movies you'll vibe with..."):
                movies = discover_movies(prefs, max_results=max_results)

            if not movies:
                st.warning("Couldn't find movies matching all filters. Try relaxing rating/year filters.")
            else:
                st.markdown("### 🔥 Recommended for you")
                for m in movies:
                    poster = m.get("Poster")
                    title = m.get("Title")
                    year = m.get("Year")
                    rating = m.get("imdbRating")
                    genre = m.get("Genre")
                    plot = m.get("Plot")
                    lang = m.get("Language")

                    c1, c2 = st.columns([1, 3])
                    with c1:
                        if poster and poster != "N/A":
                            st.image(poster, use_container_width=True)
                    with c2:
                        st.markdown(f"**{title} ({year})**")
                        st.markdown(f"⭐ **IMDB:** {rating}  &nbsp;&nbsp; 🌍 **Language:** {lang}")
                        st.markdown(f"🎭 **Genre:** {genre}")
                        st.markdown(f"📝 {plot}")
                    st.markdown("---")
        else:
            st.info("Set your preferences on the left and click **Get movie suggestions**.")

# ------------- TAB 2 – Search + Manual Similar --------- #

with tab2:
    st.subheader("Search for any movie and see its details")

    query = st.text_input("Enter a movie name", "Harry Potter")

    if st.button("🔍 Search movie", key="search_btn"):
        results = search_movies(query)
        if not results:
            st.warning("No results found.")
        else:
            for item in results[:5]:
                details = get_movie_details(item["imdbID"])
                poster = details.get("Poster")
                title = details.get("Title")
                year = details.get("Year")
                rating = details.get("imdbRating")
                genre = details.get("Genre")
                plot = details.get("Plot")
                lang = details.get("Language")

                c1, c2 = st.columns([1, 3])
                with c1:
                    if poster and poster != "N/A":
                        st.image(poster, use_container_width=True)
                with c2:
                    st.markdown(f"**{title} ({year})**")
                    st.markdown(f"⭐ **IMDB:** {rating}  &nbsp;&nbsp; 🌍 **Language:** {lang}")
                    st.markdown(f"🎭 **Genre:** {genre}")
                    st.markdown(f"📝 {plot}")
                st.markdown("---")
