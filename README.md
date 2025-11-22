# 🎬 CineMatch – Real-Time Movie Recommendation Engine  
### Powered by OMDb API | Built with Streamlit

CineMatch is a real-time **movie recommendation web application** that fetches live movie data  
(posters, IMDb ratings, genres, plots, languages, and release years) from the **OMDb API**.  
It requires **no training**, no datasets, and works fully online.

Users choose their preferences (genres, language, rating, year range), and CineMatch instantly  
recommends movies tailored to their taste.

---

## 🌟 Features

### ✨ 1. Personalized Movie Discovery  
Customize your recommendations by selecting:
- 🎭 **Genres** (Action, Thriller, Romance, Sci-Fi, etc.)  
- 🌍 **Preferred language** (English, Hindi, Tamil, Japanese, etc.)  
- ⭐ **Minimum IMDb rating filter**  
- 📅 **Year range**  
- 🎬 **Number of recommendations to display**

CineMatch fetches real movies that match your preferences and displays detailed movie cards.

---

### ✨ 2. Search Any Movie  
Search for a movie by name and see:
- Poster  
- IMDb rating  
- Release year  
- Genre  
- Plot summary  
- Language  

---

### ✨ 3. Dynamic, Modern UI  
- Clean layout with tabs  
- Movie card design  
- Responsive and interactive  
- Powered by Streamlit  

---

## 🛠️ Tech Stack

| Component          | Technology        |
|-------------------|-------------------|
| Frontend UI       | Streamlit         |
| Movie Data Source | OMDb API          |
| Backend Logic     | Python            |
| HTTP Requests     | requests library  |

---

## 📁 Project Structure

cinematch/
├── app/
│ └── app.py # Streamlit application
├── src/ # (future backend modules if needed)
├── requirements.txt
└── README.md



**2. Install dependencies**
pip install -r requirements.txt



**3. Insert your OMDb API Key**

Get your free key from: https://www.omdbapi.com/apikey.aspx

Open app/app.py and replace:

API_KEY = "YOUR_OMDB_API_KEY"



**4. Run the application**
streamlit run app/app.py




**Sample Run**


<img width="1886" height="958" alt="image" src="https://github.com/user-attachments/assets/d4f2be05-abdc-4f4f-95b8-dd1b28dfc2a0" />



**🔮 Future Improvements**

Add trending movies section

Add actor/director-based recommendations

Add Watchlist feature

Add TMDb support (more powerful search)

Deploy on Streamlit Cloud

Add dark mode

**👨‍💻 Author**

Jagadeesh Raj M
AI & Data Science Enthusiast
