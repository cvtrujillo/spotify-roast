import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_auth_manager(client_id, client_secret, redirect_uri, cache_path=".spotify_cache"):
    scopes = ["user-top-read", "user-read-recently-played", "user-library-read"]
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=" ".join(scopes),
        cache_path=cache_path,
        show_dialog=True,
    )


def fetch_top_artists(sp, limit=20, time_range="medium_term"):
    results = sp.current_user_top_artists(limit=limit, time_range=time_range)
    return [
        {
            "name": a["name"],
            "genres": a.get("genres", []),
            "popularity": a.get("popularity", 0),
            "image": a["images"][0]["url"] if a.get("images") else None,
        }
        for a in results.get("items", [])
    ]


def fetch_top_tracks(sp, limit=30, time_range="medium_term"):
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    return [
        {
            "name": t["name"],
            "artist": t["artists"][0]["name"] if t.get("artists") else "Unknown",
            "album": t.get("album", {}).get("name", "Unknown"),
            "popularity": t.get("popularity", 0),
            "id": t["id"],
        }
        for t in results.get("items", [])
    ]


def fetch_recently_played(sp, limit=50):
    results = sp.current_user_recently_played(limit=limit)
    return [
        {
            "name": item["track"]["name"],
            "artist": item["track"]["artists"][0]["name"],
            "played_at": item["played_at"],
        }
        for item in results.get("items", [])
    ]


def fetch_audio_features(sp, track_ids):
    if not track_ids:
        return []
    features = []
    for i in range(0, len(track_ids), 100):
        batch = sp.audio_features(track_ids[i:i + 100])
        features.extend([f for f in batch if f is not None])
    return features


def get_user_profile(sp):
    user = sp.current_user()
    return {
        "name": user.get("display_name", "Mystery Listener"),
        "country": user.get("country", "Unknown"),
        "followers": user.get("followers", {}).get("total", 0),
        "image": user["images"][0]["url"] if user.get("images") else None,
    }
