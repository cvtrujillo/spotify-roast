from collections import Counter


def analyze_genres(artists):
    all_genres = []
    for artist in artists:
        all_genres.extend(artist.get("genres", []))
    genre_counts = Counter(all_genres)
    total = len(all_genres) or 1
    unique = len(genre_counts)
    diversity_score = round(min(unique / max(total * 0.5, 1), 1.0), 2)
    top_genres = genre_counts.most_common(5)
    label = "Dangerously one-dimensional"
    if diversity_score >= 0.85: label = "Musical chaos agent"
    elif diversity_score >= 0.65: label = "Genre explorer"
    elif diversity_score >= 0.45: label = "Reasonably adventurous"
    elif diversity_score >= 0.25: label = "Comfort zone dweller"
    return {
        "top_genres": [{"genre": g, "count": c} for g, c in top_genres],
        "unique_genres": unique,
        "diversity_score": diversity_score,
        "diversity_label": label,
    }


def analyze_mainstream(artists, tracks):
    artist_pops = [a["popularity"] for a in artists if "popularity" in a]
    track_pops = [t["popularity"] for t in tracks if "popularity" in t]
    avg_artist = round(sum(artist_pops) / max(len(artist_pops), 1), 1)
    avg_track = round(sum(track_pops) / max(len(track_pops), 1), 1)
    overall = round((avg_artist + avg_track) / 2, 1)
    label = "Balanced between basic and interesting"
    if overall > 80: label = "Walking Billboard Hot 100"
    elif overall > 65: label = "Mainstream with occasional indie detours"
    elif overall <= 25: label = "Listening to things that don't technically exist yet"
    elif overall <= 45: label = "Suspiciously underground"
    return {
        "avg_artist_popularity": avg_artist,
        "avg_track_popularity": avg_track,
        "overall_mainstream_score": overall,
        "label": label,
    }


def analyze_loyalty(artists, tracks):
    artist_in_tracks = Counter(t["artist"] for t in tracks)
    top_obsession = artist_in_tracks.most_common(1)
    repeated = [a for a, c in artist_in_tracks.items() if c >= 3]
    ratio = len(repeated) / max(len(tracks), 1)
    level = "Healthy appreciation"
    if ratio > 0.3: level = "Restraining order territory"
    elif ratio > 0.15: level = "Dedicated superfan"
    elif ratio < 0.05: level = "Commitment issues with artists too"
    return {
        "top_obsession": top_obsession[0] if top_obsession else ("Nobody", 0),
        "artists_with_3plus_tracks": repeated,
        "obsession_level": level,
    }


def analyze_mood(audio_features):
    if not audio_features:
        return {"label": "Too mysterious to analyze", "details": {}}
    avg = lambda key: round(sum(f.get(key, 0) for f in audio_features) / len(audio_features), 3)
    valence = avg("valence")
    energy = avg("energy")
    danceability = avg("danceability")
    acousticness = avg("acousticness")
    tempo_avg = round(avg("tempo"), 1)
    if valence > 0.6 and energy > 0.6: mood_label = "Aggressively happy - possibly concerning"
    elif valence > 0.6: mood_label = "Chill and content - suspiciously well-adjusted"
    elif valence <= 0.4 and energy > 0.6: mood_label = "Angry sad - gym breakup energy"
    elif valence <= 0.4 and energy <= 0.4: mood_label = "Are you okay? Genuinely asking"
    else: mood_label = "Emotionally ambiguous - even Spotify is confused"
    return {
        "valence": valence, "energy": energy, "danceability": danceability,
        "acousticness": acousticness, "avg_tempo_bpm": tempo_avg, "mood_label": mood_label,
    }


def analyze_guilty_pleasures(tracks, artists):
    avg_pop = sum(a["popularity"] for a in artists) / max(len(artists), 1)
    guilty = []
    for t in tracks:
        if t["popularity"] > avg_pop + 25:
            guilty.append(f"{t['name']} by {t['artist']}")
    return guilty[:5]


def build_roast_context(profile, artists, tracks, audio_features):
    genres = analyze_genres(artists)
    mainstream = analyze_mainstream(artists, tracks)
    loyalty = analyze_loyalty(artists, tracks)
    mood = analyze_mood(audio_features)
    guilty = analyze_guilty_pleasures(tracks, artists)
    return {
        "user": profile,
        "top_artists": [a["name"] for a in artists[:10]],
        "top_tracks": [f"{t['name']} - {t['artist']}" for t in tracks[:10]],
        "genre_analysis": genres,
        "mainstream_analysis": mainstream,
        "loyalty_analysis": loyalty,
        "mood_analysis": mood,
        "guilty_pleasures": guilty,
    }
