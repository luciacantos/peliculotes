from django.core.management.base import BaseCommand
from movies.models import Series
import requests
from django.conf import settings

class Command(BaseCommand):
    help = 'Poblar la base de datos con series de diferentes categorías desde TMDb'

    def fetch_series_from_tmdb(self, category, page=1):
        """
        Realiza la solicitud a la API de TMDb para obtener series de una categoría específica.
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
        Poblar la base de datos con series de diferentes categorías.
        """
        categories = {
            "popular": "Populares",
            "top_rated": "Mejor Valoradas",
            "on_the_air": "En Emisión",
            "airing_today": "Transmitiéndose Hoy",
        }
        
        for category, category_name in categories.items():
            self.stdout.write(self.style.WARNING(f"Cargando series de la categoría: {category_name}..."))
            for page in range(1, 3):  # Traer series de las primeras 2 páginas
                series_list = self.fetch_series_from_tmdb(category, page)
                for series_data in series_list:
                    Series.objects.update_or_create(
                        tmdb_id=series_data['id'],
                        defaults={
                            'title': series_data['name'],
                            'overview': series_data.get('overview'),
                            'release_date': series_data.get('first_air_date'),
                            'poster_path': series_data.get('poster_path'),
                            'category': category_name,  # Nueva columna para clasificar por categoría
                        },
                    )
            self.stdout.write(self.style.SUCCESS(f"Series de la categoría {category_name} almacenadas correctamente."))


