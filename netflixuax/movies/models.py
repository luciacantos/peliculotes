from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title

class Series(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.CharField(max_length=200, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    tmdb_id = models.IntegerField(unique=True, null=True)
    category = models.CharField(max_length=50, null=True, blank=True)


# paara crear lista de peliculitas favoritas
class FavouriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class FavouriteSeries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'series')

class ViewedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    liked = models.BooleanField(null=True, blank=True)  # Agregar este campo para "me gusta" o "no me gusta"

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - Liked: {self.liked}"

class ViewedSeries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    series = models.ForeignKey('Series', on_delete=models.CASCADE)
    liked = models.BooleanField(null=True, blank=True)  # Opcional para series

    def __str__(self):
        return f"{self.user.username} - {self.series.title} - Liked: {self.liked}"
