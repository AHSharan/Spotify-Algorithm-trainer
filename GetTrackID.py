
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
# Replace these with your client ID and client secret
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'



scope = "user-read-playback-state user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

def get_album_track_ids(album_name, artist_name):
    """Retrieve track IDs from an album by its name and artist."""
    results = sp.search(q=f'album:{album_name} artist:{artist_name}', type='album', limit=1)
    if results['albums']['items']:
        album_id = results['albums']['items'][0]['id']
        album_tracks = sp.album_tracks(album_id)
        track_ids = [track['id'] for track in album_tracks['items']]
        return track_ids
    else:
        print(f"No album found with name '{album_name}' by '{artist_name}'")
        return []

def get_song_track_ids(song_name, artist_name):
    """Retrieve track IDs from a song by its name and artist."""
    results = sp.search(q=f'track:{song_name} artist:{artist_name}', type='track', limit=1)
    if results['tracks']['items']:
        track_id = results['tracks']['items'][0]['id']
        return [track_id]
    else:
        print(f"No track found with name '{song_name}' by '{artist_name}'")
        return []

def parse_line(line):
    """Parse a line in the format 'Name - Artist'."""
    parts = line.split(' - ')
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    else:
        print(f"Invalid format: {line}")
        return None, None

def remove_empty_lines(filename):
    """Remove empty lines from the file."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    with open(filename, 'w') as f:
        for line in lines:
            if line.strip():
                f.write(line)

def create_file_if_not_exists(filename):
    """Create a file if it does not exist."""
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            pass  # Just create an empty file

def main():
    albums_file = 'albums.txt'
    songs_file = 'songs.txt'
    output_file = 'tracks.txt'

    # Ensure the files exist
    create_file_if_not_exists(albums_file)
    create_file_if_not_exists(songs_file)
    create_file_if_not_exists(output_file)

    with open(albums_file, 'r') as f:
        albums = [parse_line(line) for line in f.readlines() if line.strip()]

    with open(songs_file, 'r') as f:
        songs = [parse_line(line) for line in f.readlines() if line.strip()]

    with open(output_file, 'a') as f_out:
        for album_name, artist_name in albums:
            if album_name and artist_name:
                track_ids = get_album_track_ids(album_name, artist_name)
                if track_ids:
                    f_out.write(f"Track IDs for '{album_name}' - '{artist_name}':\n")
                    for track_id in track_ids:
                        f_out.write(f"{track_id}\n")
                    f_out.write("\n")
        
        for song_name, artist_name in songs:
            if song_name and artist_name:
                track_ids = get_song_track_ids(song_name, artist_name)
                if track_ids:
                    f_out.write(f"Track IDs for '{song_name}' - '{artist_name}':\n")
                    for track_id in track_ids:
                        f_out.write(f"{track_id}\n")
                    f_out.write("\n")

    # Remove empty lines from the output file
    remove_empty_lines(output_file)

if __name__ == "__main__":
    main()
