from django.core.management.base import BaseCommand
from movies.models import Movie
from movies.utils import fetch_movies_from_tmdb

class Command(BaseCommand):
    help = 'Poblar la base de datos con películas populares desde TMDb'

    def handle(self, *args, **kwargs):
        movies = fetch_movies_from_tmdb()
        for movie_data in movies:
            Movie.objects.get_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data['title'],
                    'overview': movie_data['overview'],
                    'release_date': movie_data.get('release_date'),
                    'poster_path': movie_data.get('poster_path'),
                },
            )
        self.stdout.write(self.style.SUCCESS('Películas populares almacenadas correctamente.'))
