import difflib, spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SCOPES, CACHE_PATH

class SpotifyClient:
    def __init__(self):
        if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
            raise RuntimeError("Missing Spotify credentials. Set them in .env")
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SCOPES,
            open_browser=True,
            cache_path=CACHE_PATH
        ))

    def ensure_device(self):
        devices = self.sp.devices().get('devices', [])
        if not devices:
            return None
        active = [d for d in devices if d.get('is_active')]
        return (active[0] if active else devices[0])['id']

    def search_track_uri(self, query: str):
        results = self.sp.search(q=query, type='track', limit=5)
        items = results.get('tracks', {}).get('items', [])
        if not items:
            return None, None

        best = max(items, key=lambda t: difflib.SequenceMatcher(
            None, query.lower(), (t['name'] + " " + " ".join(a['name'] for a in t['artists'])).lower()
        ).ratio())

        name = best['name']
        artists = ", ".join(a['name'] for a in best['artists'])
        return best['uri'], f"{name} — {artists}"

    def play_track(self, track_uri: str):
        device_id = self.ensure_device()
        if not device_id:
            raise RuntimeError("No active Spotify devices found. Open Spotify first.")
        self.sp.start_playback(device_id=device_id, uris=[track_uri])