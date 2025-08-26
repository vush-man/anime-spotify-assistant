import os
from pathlib import Path
from dotenv import load_dotenv

APP_TITLE = "Anime Spotify Assistant"
IMG_FILE = "assets/anime_girl.png"
SCOPES = "user-read-playback-state user-modify-playback-state"
REDIRECT_URI_DEFAULT = "http://127.0.0.1:8080/callback"

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", REDIRECT_URI_DEFAULT)

CACHE_PATH = str(Path.cwd() / ".cache")

VOICE_VOLUME = 3.0