import os
import requests
import base64
import random
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_SEARCH_URL = 'https://api.spotify.com/v1/search'

# Map moods to genres and audio feature parameters for more musical variety
MOOD_TO_GENRES = {
    "Energetic / Passionate": {
        "genres": ["rock", "electronic", "dance", "hip-hop"],
        "params": {"min_energy": 0.7, "min_tempo": 120}
    },
    "Calm / Sad": {
        "genres": ["classical", "ambient", "piano", "acoustic"],
        "params": {"max_energy": 0.4, "max_valence": 0.4}
    },
    "Happy / Cheerful": {
        "genres": ["pop", "disco", "funk", "tropical"],
        "params": {"min_valence": 0.7}
    },
    "Relaxed / Peaceful": {
        "genres": ["jazz", "ambient", "acoustic", "indie"],
        "params": {"max_energy": 0.5, "min_valence": 0.4, "max_tempo": 100}
    },
    "Moody / Melancholic": {
        "genres": ["blues", "soul", "indie", "alternative"],
        "params": {"max_valence": 0.4, "min_acousticness": 0.5}
    },
    "Uplifting / Hopeful": {
        "genres": ["pop", "edm", "country", "gospel"],
        "params": {"min_valence": 0.6, "min_energy": 0.5}
    },
    "Mysterious / Playful": {
        "genres": ["indie-pop", "electronic", "alternative", "soundtrack"],
        "params": {"max_valence": 0.6, "min_energy": 0.5}
    }
}

def get_spotify_token():
    """Authenticates with Spotify to get an access token."""
    if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
        raise ValueError("Spotify Client ID or Secret not found in .env file.")

    auth_header = base64.b64encode(f'{SPOTIPY_CLIENT_ID}:{SPOTIPY_CLIENT_SECRET}'.encode('ascii')).decode('ascii')
    headers = {'Authorization': f'Basic {auth_header}', 'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': 'client_credentials'}

    try:
        response = requests.post(SPOTIFY_AUTH_URL, headers=headers, data=payload)
        response.raise_for_status()
        token_info = response.json()
        token = token_info.get('access_token')
        if not token:
            raise ValueError("No access token in Spotify response")
        return token
    except Exception as e:
        print(f"Error getting Spotify token: {str(e)}")
        return None

def get_spotify_recommendations(mood, genre=None):
    """Uses Spotify search with genre focus for better music variety."""
    token = get_spotify_token()
    if not token:
        return {'error': 'Failed to authenticate with Spotify. Check your credentials.'}

    headers = {'Authorization': f'Bearer {token}'}
    
    # Get genre options for the detected mood
    mood_data = MOOD_TO_GENRES.get(mood, MOOD_TO_GENRES["Happy / Cheerful"])
    
    # If user specified a genre, prioritize that, otherwise pick randomly from mood genres
    if genre:
        search_genre = genre
    else:
        search_genre = random.choice(mood_data["genres"])
    
    # Construct query with genre for more specific results
    search_query = f"genre:{search_genre}"
    
    # Add any additional audio feature parameters
    additional_params = {}
    if mood_data.get("params"):
        additional_params = {k: v for k, v in mood_data["params"].items()}
    
    # Use the search endpoint with genre focus
    params = {
        'q': search_query,
        'type': 'track',
        'limit': 50  # Get more results for variety
    }
    
    # Add any audio feature filters
    for param, value in additional_params.items():
        params[param] = value

    try:
        response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params)
        
        # Handle token expiration
        if response.status_code == 401:
            token = get_spotify_token()
            if not token:
                return {'error': 'Failed to refresh Spotify token.'}
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params)
        
        # If genre search fails, try a more generic approach
        if response.status_code != 200 or 'error' in response.json():
            # Try simpler search without audio feature parameters
            simplified_params = {
                'q': f"genre:{search_genre}",
                'type': 'track',
                'limit': 20
            }
            response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=simplified_params)
            
            # If still failing, try most basic genre search
            if response.status_code != 200:
                # Fall back to simple genre search
                basic_params = {
                    'q': search_genre,
                    'type': 'track',
                    'limit': 20
                }
                response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=basic_params)
                
                # Ultimate fallback to any music
                if response.status_code != 200:
                    backup_params = {'q': 'music', 'type': 'track', 'limit': 10}
                    response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=backup_params)
        
        response.raise_for_status()
        search_results = response.json()

        if search_results.get('tracks', {}).get('items', []):
            # Pick a random track from the results for variety
            tracks = search_results['tracks']['items']
            # If we have multiple results, pick from the top half for quality
            if len(tracks) > 5:
                track = random.choice(tracks[:len(tracks)//2])
            else:
                track = random.choice(tracks)
                
            return {
                'title': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'spotify_link': track['external_urls']['spotify'],
                'genre': search_genre  # Include the genre we searched for
            }
        else:
            return {'error': f'No songs found for genre: {search_genre}'}
            
    except Exception as e:
        print(f"Error in Spotify search: {str(e)}")
        return {'error': f'Error finding songs: {str(e)}'}