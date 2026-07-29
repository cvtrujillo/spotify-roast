import os
import streamlit as st
from dotenv import load_dotenv
import spotipy
from src.spotify_client import get_auth_manager, fetch_top_artists, fetch_top_tracks, fetch_audio_features, get_user_profile
from src.analyzer import build_roast_context
from src.roaster import generate_roast, generate_roast_title

load_dotenv()

SPOTIFY_CLIENT_ID = st.secrets.get("SPOTIFY_CLIENT_ID", os.getenv("SPOTIFY_CLIENT_ID", ""))
SPOTIFY_CLIENT_SECRET = st.secrets.get("SPOTIFY_CLIENT_SECRET", os.getenv("SPOTIFY_CLIENT_SECRET", ""))
SPOTIFY_REDIRECT_URI = st.secrets.get("SPOTIFY_REDIRECT_URI", os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8501/callback"))
ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY", ""))

st.set_page_config(page_title="Spotify Roast AI", page_icon="🎵", layout="centered")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
.main,.stApp{background-color:#0B0D10}
.hero-title{font-family:'Space Grotesk',sans-serif;font-size:3rem;font-weight:700;background:linear-gradient(135deg,#1DB954,#3EEBC0);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center;margin-bottom:.5rem}
.hero-sub{text-align:center;color:#7D8290;font-size:1.1rem;margin-bottom:2rem}
.roast-box{background:#14171C;border:1px solid #252830;border-radius:16px;padding:2rem;color:#D8DAE0;line-height:1.8;font-size:1.05rem}
.stat-row{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin:1.5rem 0}
.stat-pill{background:#14171C;border:1px solid #252830;border-radius:12px;padding:12px 20px;text-align:center;min-width:140px}
.stat-pill .number{font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:700;color:#3EEBC0}
.stat-pill .label{font-size:.8rem;color:#7D8290}
</style>""", unsafe_allow_html=True)


def main():
    st.markdown('<div class="hero-title">🎵 Spotify Roast AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Connect your Spotify. Get emotionally destroyed by AI.</div>', unsafe_allow_html=True)
    if not all([SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, ANTHROPIC_API_KEY]):
        st.error("Missing API keys. Check your .env file or Streamlit Secrets.")
        return
    auth_manager = get_auth_manager(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, cache_path="/tmp/.spotify_cache")
    query_params = st.query_params
    auth_code = query_params.get("code")
    if auth_code and "token_info" not in st.session_state:
        try:
            token_info = auth_manager.get_access_token(auth_code, as_dict=True)
            st.session_state["token_info"] = token_info
            st.query_params.clear()
            st.rerun()
        except Exception:
            st.error("Auth failed. Please try connecting again.")
            st.query_params.clear()
            return
    if "token_info" not in st.session_state:
        auth_url = auth_manager.get_authorize_url()
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.link_button("🔗 Connect Spotify & Get Roasted", auth_url, use_container_width=True)
        st.markdown('<p style="text-align:center;color:#7D8290;font-size:.85rem;">We only read your top tracks and artists. We don\'t store anything.</p>', unsafe_allow_html=True)
        return
    sp = spotipy.Spotify(auth=st.session_state["token_info"]["access_token"])
    with st.spinner("🔍 Analyzing your questionable music taste..."):
        profile = get_user_profile(sp)
        artists = fetch_top_artists(sp)
        tracks = fetch_top_tracks(sp)
        track_ids = [t["id"] for t in tracks if t.get("id")]
        try:
            audio_features = fetch_audio_features(sp, track_ids)
        except Exception:
            audio_features = []
    context = build_roast_context(profile, artists, tracks, audio_features)
    st.markdown(f"### Hey, {profile['name']} 👋")
    stats_html = f'<div class="stat-row"><div class="stat-pill"><div class="number">{context["mainstream_analysis"]["overall_mainstream_score"]}</div><div class="label">Mainstream Score</div></div><div class="stat-pill"><div class="number">{context["genre_analysis"]["diversity_score"]}</div><div class="label">Genre Diversity</div></div><div class="stat-pill"><div class="number">{context["mood_analysis"].get("valence", "N/A")}</div><div class="label">Happiness Index</div></div><div class="stat-pill"><div class="number">{len(context["guilty_pleasures"])}</div><div class="label">Guilty Pleasures</div></div></div>'
    st.markdown(stats_html, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🎤 Your Top Artists**")
        for i, a in enumerate(context["top_artists"][:5], 1):
            st.markdown(f"`{i}.` {a}")
    with col2:
        st.markdown("**🎵 Your Top Tracks**")
        for i, t in enumerate(context["top_tracks"][:5], 1):
            st.markdown(f"`{i}.` {t}")
    st.markdown("---")
    for label in [f"🎭 **Genre vibe:** {context['genre_analysis']['diversity_label']}", f"📊 **Mainstream level:** {context['mainstream_analysis']['label']}", f"💚 **Artist loyalty:** {context['loyalty_analysis']['obsession_level']}", f"😶 **Mood:** {context['mood_analysis'].get('mood_label', 'Unknown')}"]:
        st.markdown(label)
    st.markdown("---")
    if st.button("🔥 Roast Me", use_container_width=True, type="primary"):
        with st.spinner("🧠 Claude is judging your entire personality..."):
            roast_title = generate_roast_title(context)
            roast_text = generate_roast(ANTHROPIC_API_KEY, context)
        st.markdown(f"## {roast_title}")
        st.markdown(f'<div class="roast-box">{roast_text}</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<p style="text-align:center;color:#7D8290;">Screenshot this and share it. Your followers deserve to know.</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p style="text-align:center;color:#7D8290;font-size:.8rem;">Built with Python, Streamlit, Spotify API & Claude AI</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
