import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# --- Page Config ---
st.set_page_config(page_title="Fast CineMatch", page_icon="⚡", layout="wide")

# Custom CSS for Speed & Style
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child {
        background-color: #00ffcc; color: black; border-radius: 10px; border: none;
        font-weight: bold; width: 100%; height: 3em;
    }
    .movie-card {
        background-color: #1e2130; padding: 15px; border-radius: 10px;
        text-align: center; border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('⚡ Turbo Movie Recommender')
st.caption("BCA 5th Sem - High Performance ML App")

# --- Optimized Data Loading ---
@st.cache_resource # Isse data baar-baar load nahi hoga, app fast chalega
def load_data():
    movies = pd.DataFrame(pickle.load(open('movie_dict.pkl', 'rb')))
    # Similarity calculate karne ke liye vectors chahiye
    # Humne vectors ko cache kar liya hai taaki har click par CPU load na ho
    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer(max_features=2000, stop_words='english')
    vectors = cv.fit_transform(movies['tag']).toarray()
    return movies, vectors

try:
    movies, vectors = load_data()

    selected_movie = st.selectbox(
        'Kaunsi movie dekhi tune?',
        movies['title'].values
    )

    if st.button('Get Instant Recommendations'):
        # Sirf selected movie ka similarity nikalna (Pure Matrix ki zaroorat nahi)
        idx = movies[movies['title'] == selected_movie].index[0]
        
        # Super Fast Calculation: Sirf 1 row vs All rows
        distances = cosine_similarity([vectors[idx]], vectors)[0]
        
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
        
        st.write("---")
        cols = st.columns(6)
        
        for i, (col, movie_data) in enumerate(zip(cols, movie_list)):
            with col:
                title = movies.iloc[movie_data[0]].title
                st.markdown(f'<div class="movie-card"><b>{title}</b></div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}. Make sure 'movie_dict.pkl' is uploaded!")