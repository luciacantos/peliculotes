from django.core.management.base import BaseCommand
from movies.models import Movie
import requests
from django.conf import settings

class Command(BaseCommand):
    help = 'Poblar la base de datos con películas de diferentes categorías desde TMDb'

    def fetch_movies_from_tmdb(self, category, page=1):
        """
        Realiza la solicitud a la API de TMDb para obtener películas de una categoría específica.
        """
        api_key = settings.TMDB_API_KEY
        base_url = "https://api.themoviedb.org/3"
        endpoint = f"/movie/{category}"
        url = f"{base_url}{endpoint}?api_key={api_key}&language=es-ES&page={page}"
        
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            self.stdout.write(self.style.ERROR(f"Error al cargar películas de la categoría {category}: {response.status_code}"))
            return []

    def handle(self, *args, **kwargs):
        """
        Poblar la base de datos con películas de diferentes categorías.
        """
        categories = {
            "popular": "Populares",
            "top_rated": "Mejor Valoradas",
            "upcoming": "Próximamente",
            "now_playing": "En Cines",
        }
        
        for category, category_name in categories.items():
            self.stdout.write(self.style.WARNING(f"Cargando películas de la categoría: {category_name}..."))
            for page in range(1, 3):  # Traer películas de las primeras 2 páginas
                movies_list = self.fetch_movies_from_tmdb(category, page)
                for movie_data in movies_list:
                    Movie.objects.update_or_create(
                        tmdb_id=movie_data['id'],
                        defaults={
                            'title': movie_data['title'],
                            'overview': movie_data.get('overview'),
                            'release_date': movie_data.get('release_date'),
                            'poster_path': movie_data.get('poster_path'),
                            'category': category_name,  # Nueva columna para clasificar por categoría
                        },
                    )
            self.stdout.write(self.style.SUCCESS(f"Películas de la categoría {category_name} almacenadas correctamente."))

