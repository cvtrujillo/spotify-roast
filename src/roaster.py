"""
Listening pattern analyzer — finds the embarrassing truths in your Spotify data.
"""

from collections import Counter


def analyze_genres(artists: list[dict]) -> dict:
    """Analyze genre distribution and diversity."""
    all_genres = []
    for artist in artists:
        all_genres.extend(artist.get("genres", []))

    genre_counts = Counter(all_genres)
    total = len(all_genres) or 1
    unique = len(genre_counts)

    # Genre diversity: unique genres / total genre tags (0-1)
    diversity_score = round(min(unique / max(total * 0.5, 1), 1.0), 2)

    top_genres = genre_counts.most_common(5)

    return {
        "top_genres": [{"genre": g, "count": c} for g, c in top_genres],
        "unique_genres": unique,
        "total_genre_tags": total,
        "diversity_score": diversity_score,
        "diversity_label": _diversity_label(diversity_score),
    }


def _diversity_label(score: float) -> str:
    if score < 0.25:
        return "Dangerously one-dimensional"
    if score < 0.45:
        return "Comfort zone dweller"
    if score < 0.65:
        return "Reasonably adventurous"
    if score < 0.85:
        return "Genre explorer"
    return "Musical chaos agent"


def analyze_mainstream(artists: list[dict], tracks: list[dict]) -> dict:
    """How mainstream vs. niche is this person?"""
    artist_pops = [a["popularity"] for a in artists if "popularity" in a]
    track_pops = [t["popularity"] for t in tracks if "popularity" in t]

    avg_artist = round(sum(artist_pops) / max(len(artist_pops), 1), 1)
    avg_track = round(sum(track_pops) / max(len(track_pops), 1), 1)
    overall = round((avg_artist + avg_track) / 2, 1)

    return {
        "avg_artist_popularity": avg_artist,
        "avg_track_popularity": avg_track,
        "overall_mainstream_score": overall,
        "label": _mainstream_label(overall),
    }


def _mainstream_label(score: float) -> str:
    if score > 80:
        return "Walking Billboard Hot 100"
    if score > 65:
        return "Mainstream with occasional indie detours"
    if score > 45:
        return "Balanced between basic and interesting"
    if score > 25:
        return "Suspiciously underground"
    return "Listening to things that don't technically exist yet"


def analyze_loyalty(artists: list[dict], tracks: list[dict]) -> dict:
    """How obsessed are they with specific artists?"""
    artist_in_tracks = Counter(t["artist"] for t in tracks)
    top_obsession = artist_in_tracks.most_common(1)

    repeated = [a for a, c in artist_in_tracks.items() if c >= 3]

    return {
        "top_obsession": top_obsession[0] if top_obsession else ("Nobody", 0),
        "artists_with_3plus_tracks": repeated,
        "obsession_level": _obsession_label(len(repeated), len(tracks)),
    }


def _obsession_label(repeated_count: int, total_tracks: int) -> str:
    ratio = repeated_count / max(total_tracks, 1)
    if ratio > 0.3:
        return "Restraining order territory"
    if ratio > 0.15:
        return "Dedicated superfan"
    if ratio > 0.05:
        return "Healthy appreciation"
    return "Commitment issues with artists too"


def analyze_mood(audio_features: list[dict]) -> dict:
    """Analyze the emotional vibe of their music."""
    if not audio_features:
        return {"label": "Too mysterious to analyze", "details": {}}

    avg = lambda key: round(
        sum(f.get(key, 0) for f in audio_features) / len(audio_features), 3
    )

    valence = avg("valence")       # happiness (0=sad, 1=happy)
    energy = avg("energy")         # intensity
    danceability = avg("danceability")
    acousticness = avg("acousticness")
    tempo_avg = round(avg("tempo"), 1)

    mood_label = _mood_label(valence, energy)

    return {
        "valence": valence,
        "energy": energy,
        "danceability": danceability,
        "acousticness": acousticness,
        "avg_tempo_bpm": tempo_avg,
        "mood_label": mood_label,
    }


def _mood_label(valence: float, energy: float) -> str:
    if valence > 0.6 and energy > 0.6:
        return "Aggressively happy — possibly concerning"
    if valence > 0.6 and energy <= 0.6:
        return "Chill and content — suspiciously well-adjusted"
    if valence <= 0.4 and energy > 0.6:
        return "Angry sad — gym breakup energy"
    if valence <= 0.4 and energy <= 0.4:
        return "Are you okay? Genuinely asking"
    return "Emotionally ambiguous — even Spotify is confused"


def analyze_guilty_pleasures(tracks: list[dict], artists: list[dict]) -> list[str]:
    """Find tracks/artists that don't fit the overall vibe."""
    # Artists with very high popularity in an otherwise low-pop library
    avg_pop = sum(a["popularity"] for a in artists) / max(len(artists), 1)

    guilty = []
    for t in tracks:
        if t["popularity"] > avg_pop + 25:
            guilty.append(f"{t['name']} by {t['artist']}")

    return guilty[:5]  # top 5 guilty pleasures


def build_roast_context(
    profile: dict,
    artists: list[dict],
    tracks: list[dict],
    audio_features: list[dict],
) -> dict:
    """Compile all analyses into a single context object for the roaster."""
    genres = analyze_genres(artists)
    mainstream = analyze_mainstream(artists, tracks)
    loyalty = analyze_loyalty(artists, tracks)
    mood = analyze_mood(audio_features)
    guilty = analyze_guilty_pleasures(tracks, artists)

    return {
        "user": profile,
        "top_artists": [a["name"] for a in artists[:10]],
        "top_tracks": [f"{t['name']} — {t['artist']}" for t in tracks[:10]],
        "genre_analysis": genres,
        "mainstream_analysis": mainstream,
        "loyalty_analysis": loyalty,
        "mood_analysis": mood,
        "guilty_pleasures": guilty,
    }
