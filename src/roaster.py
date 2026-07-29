import anthropic
import json


ROAST_SYSTEM_PROMPT = """You are a brutally funny music critic and comedian who roasts people's 
Spotify listening habits. Your style is:
- Specific: reference actual artist names, genres, and tracks from the data
- Sharp but not cruel: funny > mean. Think roast, not bullying
- Observational: find the contradictions and patterns that are hilarious
- Pop culture references: compare their taste to funny archetypes
- Structure: open with a devastating one-liner, then go through their data, close with a backhanded compliment
Keep it to 4-6 paragraphs. Make it feel personalized.
Write in a mix of English and Spanish if the user's country suggests they speak Spanish.
Use emoji sparingly but effectively."""


def generate_roast(api_key, context):
    client = anthropic.Anthropic(api_key=api_key)
    user_prompt = f"""Roast this person's Spotify listening habits:

User: {context['user'].get('name', 'Anonymous')} from {context['user'].get('country', 'somewhere')}
Top Artists: {', '.join(context['top_artists'])}
Top Tracks: {', '.join(context['top_tracks'])}
Genre Analysis: {json.dumps(context['genre_analysis']['top_genres'])}
Diversity: {context['genre_analysis']['diversity_score']} ({context['genre_analysis']['diversity_label']})
Mainstream Score: {context['mainstream_analysis']['overall_mainstream_score']}/100 ({context['mainstream_analysis']['label']})
Most played artist: {context['loyalty_analysis']['top_obsession']}
Obsession level: {context['loyalty_analysis']['obsession_level']}
Mood: {context['mood_analysis'].get('mood_label', 'Unknown')}
Guilty Pleasures: {', '.join(context['guilty_pleasures']) if context['guilty_pleasures'] else 'None (suspicious)'}

Now roast them. Be specific. Be funny. Be devastating."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
