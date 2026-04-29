import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="CineAI – Movie Intelligence", page_icon="🎬", layout="wide", initial_sidebar_state="collapsed")

# ── Load & compute similarity ONCE (cached forever per session) ───────────────
@st.cache_resource(show_spinner=False)
def load_data():
    with open("movie_dict.pkl", "rb") as f:
        movies = pd.DataFrame(pickle.load(f))
    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(movies["tag"]).toarray()
    similarity = cosine_similarity(vectors)
    title_to_idx = {title: i for i, title in enumerate(movies["title"])}
    return movies, similarity, title_to_idx

with st.spinner("🧠 Building recommendation engine… (only once!)"):
    movies, similarity, title_to_idx = load_data()

# ── Recommendation logic ──────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def recommend(movie_title: str, n: int = 8):
    idx = title_to_idx[movie_title]
    sim_row = similarity[idx]
    top_indices = np.argpartition(sim_row, -(n + 1))[-(n + 1):]
    top_indices = top_indices[np.argsort(sim_row[top_indices])[::-1]]
    top_indices = [i for i in top_indices if i != idx][:n]
    return [
        {
            "title": movies.iloc[i]["title"],
            "similarity": round(float(sim_row[i]) * 100, 1),
            "rank": rank + 1,
        }
        for rank, i in enumerate(top_indices)
    ]

COLORS = ["#e94560","#f97316","#a855f7","#3b82f6","#10b981","#f59e0b","#ec4899","#06b6d4"]

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Space+Mono:wght@400;700&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'Outfit',sans-serif;background:#07070f;color:#e8e8f0}
.stApp{background:#07070f}.block-container{padding-top:0!important;max-width:1100px}
#MainMenu,footer,header{visibility:hidden}
.hero{text-align:center;padding:3.5rem 1rem 2rem}
.hero-badge{display:inline-block;background:linear-gradient(135deg,#e94560,#c62a47);color:#fff;font-size:.68rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;padding:.35rem 1.1rem;border-radius:100px;margin-bottom:1.1rem;font-family:'Space Mono',monospace}
.hero-title{font-size:clamp(2.8rem,6vw,4.8rem);font-weight:800;line-height:1.05;background:linear-gradient(135deg,#ffffff 20%,#e94560 90%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:.6rem}
.hero-sub{font-size:1rem;color:#666688;font-weight:300;letter-spacing:.04em;margin-bottom:2.5rem}
.glow-line{height:1px;background:linear-gradient(90deg,transparent,#e94560,transparent);border:none;margin:0 auto 2.5rem;width:50%;max-width:400px}
.stats-row{display:flex;gap:.8rem;margin:1rem 0 2rem;flex-wrap:wrap}
.stat-pill{background:#0f0f20;border:1px solid #1e1e38;border-radius:100px;padding:.45rem 1.1rem;font-size:.82rem;color:#666688;display:flex;align-items:center;gap:.4rem}
.stat-pill strong{color:#c8c8e0}
div[data-baseweb="select"]>div{background:#0f0f20!important;border:1.5px solid #1e1e38!important;border-radius:14px!important;font-size:1rem!important;color:#e8e8f0!important;transition:border-color .25s!important}
div[data-baseweb="select"]>div:hover,div[data-baseweb="select"]>div:focus-within{border-color:#e94560!important;box-shadow:0 0 0 3px rgba(233,69,96,.12)!important}
[data-baseweb="menu"]{background:#0f0f20!important;border:1px solid #1e1e38!important;border-radius:12px!important}
[role="option"]{color:#e8e8f0!important}[role="option"]:hover{background:#1a1a30!important}
.stButton>button{background:linear-gradient(135deg,#e94560,#c62a47)!important;color:#fff!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:1rem!important;letter-spacing:.04em!important;padding:.65rem 2rem!important;transition:all .25s!important;font-family:'Outfit',sans-serif!important;width:100%}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 28px rgba(233,69,96,.38)!important}
.selected-banner{background:linear-gradient(135deg,#0f0f20,#18182e);border:1.5px solid #e94560;border-radius:18px;padding:1.2rem 1.6rem;margin-bottom:2rem;display:flex;align-items:center;gap:1rem}
.dot{width:10px;height:10px;background:#e94560;border-radius:50%;box-shadow:0 0 10px #e94560;flex-shrink:0}
.banner-label{font-size:.7rem;font-family:'Space Mono',monospace;color:#e94560;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.2rem}
.banner-title{font-size:1.25rem;font-weight:700;color:#fff}
.section-heading{font-size:1.3rem;font-weight:700;color:#fff;margin:0 0 1.2rem;display:flex;align-items:center;gap:.5rem}
.section-heading .accent{color:#e94560}
.movie-card{background:#0f0f20;border:1px solid #1e1e38;border-radius:18px;padding:1.4rem 1.3rem 1.2rem;height:100%;transition:all .3s ease;position:relative;overflow:hidden}
.movie-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--accent);border-radius:18px 18px 0 0}
.movie-card:hover{transform:translateY(-5px);border-color:var(--accent);box-shadow:0 12px 36px rgba(0,0,0,.5)}
.card-rank{font-family:'Space Mono',monospace;font-size:.65rem;font-weight:700;color:var(--accent);letter-spacing:.1em;text-transform:uppercase;margin-bottom:.7rem;opacity:.8}
.card-title{font-size:1.05rem;font-weight:700;color:#e8e8f0;line-height:1.35;margin-bottom:1.1rem;min-height:2.7rem}
.sim-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:.4rem}
.sim-label{font-size:.72rem;color:#555577;font-family:'Space Mono',monospace;letter-spacing:.05em}
.sim-pct{font-family:'Space Mono',monospace;font-size:.82rem;color:var(--accent);font-weight:700}
.sim-bar-bg{background:#1a1a30;border-radius:100px;height:5px;width:100%}
.sim-bar-fill{background:var(--accent);border-radius:100px;height:5px;opacity:.85}
.empty-state{text-align:center;padding:4rem 0}
.empty-icon{font-size:3.5rem;margin-bottom:1rem;opacity:.4}
.empty-text{font-family:'Space Mono',monospace;font-size:.85rem;letter-spacing:.12em;color:#2a2a44;text-transform:uppercase}
.footer{text-align:center;padding:3rem 1rem 2rem;color:#333355;font-size:.78rem;font-family:'Space Mono',monospace;letter-spacing:.05em}
.footer a{color:#e94560;text-decoration:none}
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🎬 Powered by CineAI</div>
  <h1 class="hero-title">Discover Your<br>Next Obsession</h1>
  <p class="hero-sub">4,800+ films · cosine similarity · no pre-built model needed</p>
  <hr class="glow-line">
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="stats-row">
  <div class="stat-pill">🎥 <strong>{len(movies):,}</strong>&nbsp;movies</div>
  <div class="stat-pill">🧠 <strong>CountVectorizer + Cosine</strong></div>
  <div class="stat-pill">⚡ <strong>No similarity.pkl</strong>&nbsp;needed</div>
  <div class="stat-pill">📊 <strong>% match</strong>&nbsp;score</div>
</div>
""", unsafe_allow_html=True)

# ── SEARCH ────────────────────────────────────────────────────────────────────
col_sel, col_btn = st.columns([4, 1], gap="medium")
with col_sel:
    selected_movie = st.selectbox("Search", options=movies["title"].sort_values().tolist(), index=None, placeholder="🔍  Type or select a movie…", label_visibility="collapsed")
with col_btn:
    find_btn = st.button("✦  Recommend", use_container_width=True)

# ── RESULTS ───────────────────────────────────────────────────────────────────
if find_btn and selected_movie:
    st.markdown(f"""
<div class="selected-banner">
  <div class="dot"></div>
  <div>
    <div class="banner-label">Showing matches for</div>
    <div class="banner-title">{selected_movie}</div>
  </div>
</div>""", unsafe_allow_html=True)

    recs = recommend(selected_movie, n=8)

    st.markdown("""<div class="section-heading">✦ Top Recommendations <span class="accent">/ similarity score</span></div>""", unsafe_allow_html=True)

    for row_start in range(0, len(recs), 4):
        cols = st.columns(4, gap="medium")
        for col_idx, rec in enumerate(recs[row_start:row_start + 4]):
            color = COLORS[rec["rank"] - 1]
            with cols[col_idx]:
                st.markdown(f"""
<div class="movie-card" style="--accent:{color}">
  <div class="card-rank">#{rec['rank']} match</div>
  <div class="card-title">{rec['title']}</div>
  <div class="sim-row">
    <span class="sim-label">SIMILARITY</span>
    <span class="sim-pct">{rec['similarity']}%</span>
  </div>
  <div class="sim-bar-bg">
    <div class="sim-bar-fill" style="width:{rec['similarity']}%"></div>
  </div>
</div>""", unsafe_allow_html=True)

elif find_btn:
    st.warning("Please select a movie first.")
else:
    st.markdown("""
<div class="empty-state">
  <div class="empty-icon">🎞️</div>
  <div class="empty-text">Select a movie above and hit recommend</div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  Built with ❤️ &nbsp;·&nbsp; <strong>CineAI</strong> &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; sklearn &nbsp;·&nbsp; No .pkl model required<br>
  <a href="https://github.com" target="_blank">GitHub</a>
</div>""", unsafe_allow_html=True)
