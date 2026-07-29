# 🎵 Spotify Roast AI

**Drop your Spotify data. Get emotionally destroyed by AI.**

A Python app that analyzes your Spotify listening history and uses Claude AI to generate a brutally funny, personalized roast of your music taste.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit&logoColor=white)
![Claude API](https://img.shields.io/badge/Claude-API-blueviolet?logo=anthropic&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify-API-1DB954?logo=spotify&logoColor=white)

---

## 🔥 What it does

1. **Connects to your Spotify** via the Spotify Web API
2. **Analyzes your listening patterns**: top artists, genres, tracks, how basic or niche you are
3. **Sends it all to Claude AI** with a carefully crafted prompt
4. **Generates a personalized roast** that's funny, specific, and painfully accurate

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- A [Spotify Developer](https://developer.spotify.com/dashboard) app (free)
- An [Anthropic API key](https://console.anthropic.com/) for Claude

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/spotify-roast.git
cd spotify-roast

# Install dependencies
pip install -r requirements.txt

# Copy env template and add your keys
cp .env.example .env
# Edit .env with your API keys

# Run the app
streamlit run app.py
```

### Environment Variables

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8501/callback
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 🏗️ Project Structure

```
spotify-roast/
├── app.py                  # Streamlit UI
├── src/
│   ├── spotify_client.py   # Spotify API integration
│   ├── analyzer.py         # Data analysis & pattern detection
│   └── roaster.py          # Claude AI roast generation
├── requirements.txt
├── .env.example
└── README.md
```

## 🧠 How the roast works

The analyzer detects patterns like:

- **Genre diversity score**: are you exploring or stuck in a loop?
- **Mainstream vs. niche ratio**: how basic are you, really?
- **Artist loyalty**: do you have mass-stalking tendencies?
- **Mood patterns**: are you okay? Like, actually?
- **Guilty pleasures**: that one artist you hoped nobody would notice

Then Claude receives all of this context with a prompt designed to generate a roast that's specific, funny, and just mean enough to be shareable.

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core language |
| **Streamlit** | Web UI |
| **Spotify Web API** | Fetch listening data |
| **Claude API (Anthropic)** | Generate the roast |
| **spotipy** | Spotify API wrapper |

## 📄 License

MIT — roast responsibly.

---

Built by [Carol Vanessa Trujillo Medina](https://www.linkedin.com/in/vanessa-trujillo-70bb83319/) ✨
