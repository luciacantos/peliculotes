from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, FavouriteMovie
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm

# Vista principal
def home(request):
    movies = Movie.objects.all()
    return render(request, 'movies/home.html', {'movies': movies})

# Vista de registro
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'movies/register.html', {'form': form})

# Vista de inicio de sesión
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

# Vista de cierre de sesión
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# Añadir una película a favoritos
@login_required
def add_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    FavouriteMovie.objects.get_or_create(user=request.user, movie=movie)
    return redirect('home')

# Eliminar una película de favoritos
@login_required
def remove_favorite(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    FavouriteMovie.objects.filter(user=request.user, movie=movie).delete()
    return redirect('home')
