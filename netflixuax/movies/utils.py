import requests
from django.conf import settings

def fetch_movies_from_tmdb():
    """Obtiene películas populares de TMDb."""
    url = 'https://api.themoviedb.org/3/movie/popular'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'es-ES',
        'page': 1,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        raise Exception(f"Error en la solicitud: {response.status_code}")