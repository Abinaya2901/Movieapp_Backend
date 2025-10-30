from flask import Blueprint, request, jsonify
import requests
from utils.industry import get_industry

movies_bp = Blueprint('movies', __name__)

TMDB_API_KEY = '468c96cd6229cdf95d40b1e691395cd2'
TMDB_BASE = 'https://api.themoviedb.org/3'

industry_map = {
    "Hollywood": "en-US",
    "Bollywood": "hi-IN",
    "Kollywood": "ta-IN",
    "Tollywood": "te-IN",
    "Korean": "ko-KR",
    # Add more as needed
}

@movies_bp.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(list(industry_map.keys()))

@movies_bp.route('/genres/<industry>', methods=['GET'])
def get_genres(industry):
    # Fetch TMDB genres list
    url = f"{TMDB_BASE}/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        genres = resp.json().get('genres', [])
        # Customize or filter genres as needed per industry
        return jsonify([g['name'] for g in genres])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching genres: {e}")
        # Fallback to common genres if TMDB is unavailable
        fallback_genres = [
            "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
            "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
            "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"
        ]
        return jsonify(fallback_genres)

@movies_bp.route('/movies', methods=['POST'])
def movies_list():
    data = request.json
    industry = data.get('industry')
    genre = data.get('genre')
    # Query TMDB discover endpoint with genre and language filter
    language = industry_map.get(industry, 'en-US')

    # Find genre_id by genre name
    genre_id = None
    url = f"{TMDB_BASE}/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    try:
        genres_resp = requests.get(url, timeout=10).json()
        for g in genres_resp.get('genres', []):
            if g['name'].lower() == genre.lower():
                genre_id = g['id']
                break
    except requests.exceptions.RequestException as e:
        print(f"Error fetching genre ID: {e}")
        # Fallback genre IDs for common genres
        fallback_genre_ids = {
            "action": 28, "adventure": 12, "animation": 16, "comedy": 35, "crime": 80,
            "documentary": 99, "drama": 18, "family": 10751, "fantasy": 14, "history": 36,
            "horror": 27, "music": 10402, "mystery": 9648, "romance": 10749,
            "science fiction": 878, "tv movie": 10770, "thriller": 53, "war": 10752, "western": 37
        }
        genre_id = fallback_genre_ids.get(genre.lower())

    if genre_id is None:
        return jsonify({'error': f'Genre "{genre}" not found'}), 400

    params = {
        'api_key': TMDB_API_KEY,
        'with_genres': genre_id,
        'language': language,
        'sort_by': 'vote_average.desc',
        'vote_count.gte': 50,  # filter out unpopular
        'page': 1
    }
    discover_url = f"{TMDB_BASE}/discover/movie"
    try:
        resp = requests.get(discover_url, params=params, timeout=10)
        resp.raise_for_status()
        movies = resp.json().get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movies: {e}")
        # Fallback to sample movies if TMDB is unavailable
        sample_movies = [
            {
                "id": 1,
                "title": f"Sample {genre} Movie 1",
                "poster_path": "https://via.placeholder.com/300x450?text=No+Image",
                "vote_average": 8.5,
                "vote_count": 1000,
                "release_date": "2023-01-01",
                "original_language": language.split('-')[0],
                "production_countries": [{"iso_3166_1": language.split('-')[1] if '-' in language else "US"}]
            },
            {
                "id": 2,
                "title": f"Sample {genre} Movie 2",
                "poster_path": "https://via.placeholder.com/300x450?text=No+Image",
                "vote_average": 7.8,
                "vote_count": 800,
                "release_date": "2023-02-01",
                "original_language": language.split('-')[0],
                "production_countries": [{"iso_3166_1": language.split('-')[1] if '-' in language else "US"}]
            }
        ]
        return jsonify(sample_movies)

    # Return movies directly since language parameter already filters by industry
    return jsonify(movies[:20])
