from django.shortcuts import render, redirect
from .models import Movie, FavouriteMovie
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

# Create your views here.def home(request):
def home(request):
    if not request.user.is_authenticated:

        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('home')
        else:
            form = AuthenticationForm()
        return render(request, 'movies/login.html', {'form': form})

    movies = Movie.objects.all()
    return render(request, 'movies/home.html', {'movies': movies})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'movies/register.html', {'form': form})


@login_required
def add_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    FavoriteMovie.objects.get_or_create(user=request.user, movie=movie)
    return redirect('home')

@login_required
def remove_favorite(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    FavoriteMovie.objects.filter(user=request.user, movie=movie).delete()
    return redirect('home')

@login_required
def remove_favorite(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    FavoriteMovie.objects.filter(user=request.user, movie=movie).delete()
    return redirect('home')
