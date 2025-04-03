# Image Mood Song Recommender

This web application analyzes uploaded images to detect dominant colors and mood, then recommends songs from Spotify that match the detected mood.

## Features

- Image upload and processing
- Color extraction using K-means clustering
- Mood detection based on color psychology
- Genre-based song recommendations from Spotify
- Interactive web interface

## How It Works

1. Upload an image through the web interface
2. The app extracts the dominant colors using K-means clustering
3. The most dominant color is mapped to a mood based on color psychology
4. The detected mood is matched with appropriate music genres
5. A song recommendation is fetched from Spotify based on the mood and genre

## Technologies Used

- Python
- Flask (web framework)
- OpenCV (image processing)
- scikit-learn (K-means clustering)
- Spotify Web API (music recommendations)
- HTML/CSS/JavaScript (frontend)

## Project Structure

```
├── app.py                # Main Flask application
├── image_analysis.py     # Image processing and mood detection
├── spotify_integration.py # Spotify API integration
├── templates/
│   └── index.html        # Web interface
├── requirements.txt      # Python dependencies
├── Procfile              # For cloud deployment
└── README.md
```

## Local Setup

To run this application locally:

1. Clone this repository
   ```
   git clone https://github.com/Capski/image-mood-song-recommender.git
   cd image-mood-song-recommender
   ```

2. Create a virtual environment (optional but recommended)
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your Spotify API credentials:
   ```
   SPOTIPY_CLIENT_ID='your_spotify_client_id'
   SPOTIPY_CLIENT_SECRET='your_spotify_client_secret'
   ```

5. Run the app
   ```
   python app.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000/`

## Getting Spotify API Credentials

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Create a new app
4. Copy the Client ID and Client Secret to your `.env` file

## Deployment

The application is ready for deployment on platforms like Heroku or Render.

### Deploying to Heroku

1. Install the Heroku CLI and log in
2. In the project directory:
   ```
   heroku create
   git push heroku main
   ```
3. Set environment variables on Heroku:
   ```
   heroku config:set SPOTIPY_CLIENT_ID=your_spotify_client_id
   heroku config:set SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   ```

### Deploying to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set Build Command: `pip install -r requirements.txt`
4. Set Start Command: `gunicorn app:app`
5. Add environment variables for the Spotify credentials

## Mood to Genre Mapping

- **Energetic / Passionate**: rock, electronic, dance, hip-hop
- **Calm / Sad**: classical, ambient, piano, acoustic
- **Happy / Cheerful**: pop, disco, funk, tropical
- **Relaxed / Peaceful**: jazz, ambient, acoustic, indie
- **Moody / Melancholic**: blues, soul, indie, alternative
- **Uplifting / Hopeful**: pop, edm, country, gospel
- **Mysterious / Playful**: indie-pop, electronic, alternative, soundtrack

## Future Improvements

- Add user accounts to save favorite recommendations
- Implement more sophisticated color-to-mood mapping
- Support for music from multiple providers (not just Spotify)
- Add ability to filter by specific genres
- Improve mobile UI/UX

## License

MIT