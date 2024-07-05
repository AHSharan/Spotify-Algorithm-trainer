import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import os

# Load environment variables
SPOTIPY_CLIENT_ID = 'SPOTIPY_CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'SPOTIPY_CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'SPOTIPY_REDIRECT_URI'

scope = "user-read-playback-state user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

def play_track(track_uri):
    """Play a specific track by its URI."""
    sp.start_playback(uris=[track_uri])

def pause_playback():
    """Pause the current playback."""
    sp.pause_playback()

def resume_playback():
    """Resume the current playback."""
    sp.start_playback()

def skip_next():
    """Skip to the next track."""
    sp.next_track()

def get_track_info():
    """Retrieve and print the current track information."""
    current_track = sp.current_playback()
    if current_track and current_track['is_playing']:
        track_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        track_duration_ms = current_track['item']['duration_ms']
        progress_ms = current_track['progress_ms']
        progress_s = progress_ms / 1000
        remaining_ms = track_duration_ms - progress_ms
        print(f"Current Track: {track_name} by {artist_name}")
        print(f"Track Duration: {track_duration_ms} ms")
        print(f"Progress: {progress_ms} ms")
        print(f"Remaining: {remaining_ms} ms")
        return progress_s

if __name__ == "__main__":
    with open("tracks.txt", 'r') as f:
        track_uris = [line.strip() for line in f.readlines() if line.strip()]

    for track_uri in track_uris:
        play_track("spotify:track:" + track_uri)
        time.sleep(2)
        s = get_track_info()
        time.sleep(s)
