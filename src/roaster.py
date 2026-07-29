import anthropic
import json


ROAST_SYSTEM_PROMPT = """You are a brutally funny music critic and comedian who roasts people's Spotify listening habits. Your style is:
- Specific: reference actual artist names, genres, and tracks from the data
- Sharp but not cruel: funny > mean. Think roast, not bullying
- Observational: find the contradictions and patterns that are hilarious
- Structure: open with a devastating one-liner, then go through their data, close with a backhanded compliment
Keep it to 4-6 paragraphs. Make it feel personalized.
Write in a mix of English and Spanish if the user's country suggests they speak Spanish."""


def generate_roast(api_key, context):
    client = anthropic.Anthropic(api_key=api_key)
    prompt = "Roast this person's Spotify listening habits:\n"
    prompt += f"User: {context['user'].get('name', 'Anonymous')} from {context['user'].get('country', 'somewhere')}\n"
    prompt += f"Top Artists: {', '.join(context['top_artists'])}\n"
    prompt += f"Top Tracks: {', '.join(context['top_tracks'])}\n"
    prompt += f"Genre Analysis: {json.dumps(context['genre_analysis']['top_genres'])}\n"
    prompt += f"Diversity: {context['genre_analysis']['diversity_score']} ({context['genre_analysis']['diversity_label']})\n"
    prompt += f"Mainstream Score: {context['mainstream_analysis']['overall_mainstream_score']}/100 ({context['mainstream_analysis']['label']})\n"
    prompt += f"Most played artist: {context['loyalty_analysis']['top_obsession']}\n"
    prompt += f"Obsession level: {context['loyalty_analysis']['obsession_level']}\n"
    prompt += f"Mood: {context['mood_analysis'].get('mood_label', 'Unknown')}\n"
    guilty = ', '.join(context['guilty_pleasures']) if context['guilty_pleasures'] else 'None (suspicious)'
    prompt += f"Guilty Pleasures: {guilty}\n"
    prompt += "Now roast them. Be specific. Be funny. Be devastating."
    message = client.messages.create(model="claude-sonnet-4-6", max_tokens=1200, system=ROAST_SYSTEM_PROMPT, messages=[{"role": "user", "content": prompt}])
    return message.content[0].text


def generate_roast_title(context):
    top_genre = context["genre_analysis"]["top_genres"][0]["genre"] if context["genre_analysis"]["top_genres"] else "music"
    titles = {"pop": "Certified Basic", "rock": "Still Stuck in a Guitar Solo", "hip hop": "Rapper Adjacent", "reggaeton": "Perreo Intenso", "latin": "Latino Heat", "indie": "Too Cool for Spotify", "electronic": "DJ Nobody Asked For", "k-pop": "Stan Account Detected"}
    for key, title in titles.items():
        if key in top_genre.lower():
            return f"🎵 {title}: A Roast"
    return f"🎵 Your Taste in {top_genre.title()}: A Roast"
