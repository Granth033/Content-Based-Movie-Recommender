# 🎬 CineAI — Movie Recommendation System

A content-based movie recommender built with Python and Streamlit.
Just select a movie and get 8 similar movies with match percentage instantly.

---

## 🗂️ Files in this Repo

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit app |
| `movie_dict.pkl` | Movie dataset (4,800 movies) |
| `requirements.txt` | Required Python libraries |

> `similarity.pkl` is NOT needed — the app builds it automatically on startup.

---

## ▶️ How to Run

**Step 1** — Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/cineai-recommender.git
cd cineai-recommender
```

**Step 2** — Install libraries
```bash
pip install -r requirements.txt
```

**Step 3** — Run the app
```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

> First launch takes about 3 seconds to build the model. After that it's instant.

---

## 🧠 How It Works

1. Movie tags (genre, cast, keywords) are converted to vectors using **CountVectorizer**
2. **Cosine Similarity** finds how close each movie is to another
3. Top 8 most similar movies are shown with a match % score

---

## 🛠️ Built With

- Python
- Streamlit
- Scikit-learn
- Pandas & NumPy

---

Made with ❤️ — give it a ⭐ if you liked it!
