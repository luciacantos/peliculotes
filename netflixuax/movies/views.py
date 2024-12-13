from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, FavouriteMovie, Series, FavouriteSeries
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm


def home(request):
    movies = Movie.objects.all()
    return render(request, 'movies/home.html', {'movies': movies})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'movies/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'movies/login.html', {'form': form})


def series_view(request):
    series = Series.objects.all()
    return render(request, 'movies/series.html', {'series': series})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def my_list(request):
    favourite_movies = FavouriteMovie.objects.filter(user=request.user)
    favourite_series = FavouriteSeries.objects.filter(user=request.user)
    return render(request, 'movies/my_list.html', {
        'favourite_movies': favourite_movies,
        'favourite_series': favourite_series
    })

@login_required
def add_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    FavouriteMovie.objects.get_or_create(user=request.user, movie=movie)
    return redirect('my_list')

@login_required
def remove_favorite(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    FavouriteMovie.objects.filter(user=request.user, movie=movie).delete()
    return redirect('my_list')


# para añadir las series a la lista
@login_required
def add_series(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    FavouriteSeries.objects.get_or_create(user=request.user, series=series)
    return redirect('my_list')

@login_required
def remove_favorite_series(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    FavouriteSeries.objects.filter(user=request.user, series=series).delete()
    return redirect('my_list')
