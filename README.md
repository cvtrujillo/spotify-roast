"""
🎵 Spotify Roast AI — Drop your Spotify. Get destroyed by AI.
"""

import os
import streamlit as st
from dotenv import load_dotenv
import spotipy

from src.spotify_client import (
    get_auth_manager,
    fetch_top_artists,
    fetch_top_tracks,
    fetch_audio_features,
    get_user_profile,
)
from src.analyzer import build_roast_context
from src.roaster import generate_roast, generate_roast_title

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
S
