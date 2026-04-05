import streamlit as st
import pickle
import pandas as pd
import requests

# --- 1. Page Config (Sabse upar hona zaroori hai) ---
st.set_page_config(page_title="Movie Recommender Pro", page_icon="🍿", layout="wide")

# --- 2. Custom CSS for "Pro" Look ---
st.markdown("""
<style>
    /* Streamlit ka default upar wala menu aur neeche ka watermark hatane ke liye */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Movie Title styling - Taki sab titles ek barabar height mein aayen */
    .movie-title {
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        height: 50px; 
        overflow: hidden;
        color: #E0E0E0;
    }
    
    /* Main Header styling (Netflix jaisa red color) */
    .main-header {
        font-size: 55px;
        font-weight: 800;
        color: #E50914; 
        text-align: center;
        margin-bottom: 5px;
        font-family: 'Arial Black', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Poster Fetch Karne Ka Function ---
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750/1f1f1f/ffffff?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750/1f1f1f/ffffff?text=Poster+Blocked"

# --- 4. Movie Recommend Karne Ka Function ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id 
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        
    return recommended_movies, recommended_movies_posters

# --- 5. Pickle Files Load Karna (Saath mein caching taaki app fast chale) ---
@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movie_dict.pkl','rb'))
    movies_df = pd.DataFrame(movies_dict) 
    sim = pickle.load(open('similarity.pkl','rb'))
    return movies_df, sim

try:
    movies, similarity = load_data()
except FileNotFoundError:
    st.error("Error: 'movie_dict.pkl' ya 'similarity.pkl' nahi mili.")
    st.stop()

# --- 6. Streamlit Website UI (The Pro Layout) ---

# Custom Header
st.markdown('<div class="main-header">CineMatch Pro</div>', unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #888; margin-bottom: 40px;'>Discover your next favorite movie</h4>", unsafe_allow_html=True)

# Search Bar ko center mein laane ke liye empty columns use kiye hain
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    selected_movie_name = st.selectbox(
        '🔍 Type or select a movie you like:',
        movies['title'].values
    )
    
    # Button ko poori width di hai
    recommend_button = st.button('✨ Get Recommendations', use_container_width=True)

st.write("---") # Ek line divider

# Jab button click ho
if recommend_button:
    # Loading animation
    with st.spinner('🎬 Finding the best movies for you...'):
        names, posters = recommend(selected_movie_name)
    
    st.subheader("🎯 We think you'll love these:")
    st.write("") # Thodi spacing
    
    # 5 Movies ko line se dikhane ka layout
    poster_columns = st.columns(5)
    
    for idx, col in enumerate(poster_columns):
        with col:
            st.image(posters[idx], use_container_width=True)
            # Custom HTML titles lagaye hain taaki sab ek barabar dikhein
            st.markdown(f'<div class="movie-title">{names[idx]}</div>', unsafe_allow_html=True)