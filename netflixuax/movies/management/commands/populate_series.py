from django.core.management.base import BaseCommand
from movies.models import Series, Genre
import requests
from django.conf import settings


class Command(BaseCommand):
    help = 'Poblar la base de datos con series y sus géneros desde TMDb'

    def fetch_genres(self):
        """
        Obtiene la lista de géneros de series desde TMDb y los guarda en la base de datos.
        """
        api_key = settings.TMDB_API_KEY
        url = f"https://api.themoviedb.org/3/genre/tv/list?api_key={api_key}&language=es-ES"

        response = requests.get(url)
        if response.status_code == 200:
            genres_data = response.json().get("genres", [])
            for genre in genres_data:
                Genre.objects.update_or_create(id=genre['id'], defaults={'name': genre['name']})
        else:
            self.stdout.write(self.style.ERROR(f"Error al cargar géneros: {response.status_code}"))

    def fetch_series_from_tmdb(self, category, page=1):
        """
        Obtiene las series de una categoría específica desde la API de TMDb.
        """
        api_key = settings.TMDB_API_KEY
        base_url = "https://api.themoviedb.org/3"
        endpoint = f"/tv/{category}"
        url = f"{base_url}{endpoint}?api_key={api_key}&language=es-ES&page={page}"

        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            self.stdout.write(self.style.ERROR(f"Error al cargar series de la categoría {category}: {response.status_code}"))
            return []

    def handle(self, *args, **kwargs):
        """
        Pobla la base de datos con series y géneros.
        """
        # Primero, cargar los géneros
        self.stdout.write(self.style.WARNING("Cargando géneros de series..."))
        self.fetch_genres()
        self.stdout.write(self.style.SUCCESS("Géneros cargados correctamente."))

        categories = {
            "popular": "Populares",
            "top_rated": "Mejor Valoradas",
            "on_the_air": "En Emisión",
        }

        for category, category_name in categories.items():
            self.stdout.write(self.style.WARNING(f"Cargando series de la categoría: {category_name}..."))
            for page in range(1, 3):  # Traer series de las primeras 2 páginas
                series_list = self.fetch_series_from_tmdb(category, page)
                for series_data in series_list:
                    # Crear o actualizar la serie
                    series, created = Series.objects.update_or_create(
                        tmdb_id=series_data['id'],
                        defaults={
                            'title': series_data['name'],
                            'overview': series_data.get('overview'),
                            'release_date': series_data.get('first_air_date'),
                            'poster_path': series_data.get('poster_path'),
                            'category': category_name,
                        },
                    )

                    # Asignar géneros
                    genre_ids = series_data.get('genre_ids', [])
                    genres = Genre.objects.filter(id__in=genre_ids)
                    series.genres.set(genres)  # Asignar géneros a la serie

            self.stdout.write(self.style.SUCCESS(f"Series de la categoría {category_name} almacenadas correctamente."))


