"""
Spotify API client — fetches user's top tracks, artists, and recent listening data.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import Optional


def get_auth_manager(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    cache_path: str = ".spotify_cache",
) -> SpotifyOAuth:
    """Create Spotify OAuth manager with required scopes."""
    scopes = [
        "user-top-read",
        "user-read-recently-played",
        "user-library-read",
    ]
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=" ".join(scopes),
        cache_path=cache_path,
        show_dialog=True,
    )


def fetch_top_artists(sp: spotipy.Spotify, limit: int = 20, time_range: str = "medium_term") -> list[dict]:
    """Fetch user's top artists with genres and popularity."""
    results = sp.current_user_top_artists(limit=limit, time_range=time_range)
    return [
        {
            "name": a["name"],
            "genres": a.get("genres", []),
            "popularity": a["popularity"],
            "image": a["images"][0]["url"] if a.get("images") else None,
        }
        for a in results.get("items", [])
    ]


def fetch_top_tracks(sp: spotipy.Spotify, limit: int = 30, time_range: str = "medium_term") -> list[dict]:
    """Fetch user's top tracks with audio features context."""
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    tracks = []
    for t in results.get("items", []):
        tracks.append({
            "name": t["name"],
            "artist": t["artists"][0]["name"] if t.get("artists") else "Unknown",
            "album": t.get("album", {}).get("name", "Unknown"),
            "popularity": t["popularity"],
            "id": t["id"],
        })
    return tracks


def fetch_recently_played(sp: spotipy.Spotify, limit: int = 50) -> list[dict]:
    """Fetch recently played tracks."""
    results = sp.current_user_recently_played(limit=limit)
    return [
        {
            "name": item["track"]["name"],
            "artist": item["track"]["artists"][0]["name"],
            "played_at": item["played_at"],
        }
        for item in results.get("items", [])
    ]


def fetch_audio_features(sp: spotipy.Spotify, track_ids: list[str]) -> list[dict]:
    """Fetch audio features (energy, danceability, valence, etc.) for tracks."""
    if not track_ids:
        return []
    # Spotify API allows max 100 IDs per request
    features = []
    for i in range(0, len(track_ids), 100):
        batch = sp.audio_features(track_ids[i : i + 100])
        features.extend([f for f in batch if f is not None])
    return features


def get_user_profile(sp: spotipy.Spotify) -> dict:
    """Fetch basic user profile info."""
    user = sp.current_user()
    return {
        "name": user.get("display_name", "Mystery Listener"),
        "country": user.get("country", "Unknown"),
        "followers": user.get("followers", {}).get("total", 0),
        "image": user["images"][0]["url"] if user.get("images") else None,
    }
