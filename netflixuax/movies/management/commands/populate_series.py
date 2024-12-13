from django.core.management.base import BaseCommand
from movies.models import Series
from movies.utils import fetch_series_from_tmdb

class Command(BaseCommand):
    help = 'Poblar la base de datos con series populares desde TMDb'

    def handle(self, *args, **kwargs):
        series_list = fetch_series_from_tmdb()
        for series_data in series_list:
            Series.objects.get_or_create(
                tmdb_id=series_data['id'],
                defaults={
                    'title': series_data['name'],
                    'overview': series_data.get('overview'),
                    'release_date': series_data.get('first_air_date'),
                    'poster_path': series_data.get('poster_path'),
                },
            )
        self.stdout.write(self.style.SUCCESS('Series populares almacenadas correctamente.'))

