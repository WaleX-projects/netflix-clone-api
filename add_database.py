import os
import django
import requests
import time

# 1. Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Movie, Genre

# API Keys
TMDB_API_KEY = '14404d15392c60adb0bbbfb41d83a12e'

# TMDB Genre ID Mapping
TMDB_GENRES = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Sci-Fi & Fantasy", # Simplified for your frontend
    10770: "TV Movie", 53: "Horror & Thriller", 10752: "War", 37: "Western"
}

def get_kinocheck_video(tmdb_id):
    try:
        url = f"https://api.kinocheck.com/movies?tmdb_id={tmdb_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'trailer' in data and data['trailer']:
                video_id = data['trailer'].get('youtube_video_id')
                return f"https://www.youtube.com/embed/{video_id}?autoplay=1&enablejsapi=1"
    except Exception:
        pass
    return 'https://path-to-your-sample-video.mp4'

def fetch_and_save_movies():
    IMAGE_BASE = "https://image.tmdb.org/t/p/original"
    TMDB_URL = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
    
    response = requests.get(TMDB_URL).json()

    for item in response['results']:
        tmdb_id = item['id']
        title = item['title']

        # 1. Fetch Video from KinoCheck
        video_url = get_kinocheck_video(tmdb_id)

        # 2. Create or Update Movie
        movie, created = Movie.objects.update_or_create(
            title=title,
            defaults={
                'description': item['overview'],
                'release_date': item['release_date'] if item['release_date'] else '2024-01-01',
                'thumbnail': f"{IMAGE_BASE}{item['poster_path']}",
                'video_file': video_url,
            }
        )

        # 3. Handle Genres (The Missing Part)
        genre_ids = item.get('genre_ids', [])
        for g_id in genre_ids:
            genre_name = TMDB_GENRES.get(g_id)
            if genre_name:
                # Get or create the genre in YOUR database
                genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
                # Add the relationship to the movie
                movie.genres.add(genre_obj)

        if created:
            print(f"✅ Created Movie & Linked Genres: {movie.title}")
        else:
            print(f"🔄 Updated: {movie.title}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    fetch_and_save_movies()