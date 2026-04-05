# Content-Based-Movie-Recommender
This is a Content-Based Movie Recommendation System developed as part of my BCA 5th-semester curriculum. The system analyzes a dataset of 5,000 movies to provide personalized recommendations based on the user's interests.

# Movie Recommendation System 🎬
A Machine Learning-based movie recommender system built using **Python** and **Streamlit**.

## 🚀 Overview
This project suggests the top 5 similar movies based on a user's selection. It uses the **TMDB 5000 Movies Dataset** and applies Content-Based Filtering techniques.

## 🛠️ Tech Stack
* **Language:** Python
* **Frontend:** Streamlit
* **Libraries:** Pandas, NumPy, Scikit-learn, Pickle

## 🧠 How it Works
1. **Data Preprocessing**: Merged datasets and handled missing values.
2. **Text Vectorization**: Used `CountVectorizer` to convert movie tags into vectors.
3. **Similarity**: Calculated `Cosine Similarity` to find the distance between movies.
4. **Recommendation**: Fetches the closest 5 movies for any given input.

## 💻 Installation
1. Clone the repo: `git clone <your-repo-link>`
2. Install requirements: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
