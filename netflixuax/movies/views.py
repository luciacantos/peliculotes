from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, FavouriteMovie, Series, FavouriteSeries, ViewedMovie, ViewedSeries, UserProfile
from movies.models import Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import CustomUserCreationForm, UpdateUsernameForm, UserGenresForm, UserCreationForm
from django.db.models import Q


def home_view(request):
    if request.user.is_authenticated:
        suggestions = Movie.objects.all()[:10]
        context = {"suggestions": suggestions}
    else:
        all_movies = Movie.objects.all()[:30]
        column1_movies = all_movies[0::3]  # Cada 3ra película empieza en 0
        column2_movies = all_movies[1::3]  # Cada 3ra película empieza en 1
        column3_movies = all_movies[2::3]  # Cada 3ra película empieza en 2

        context = {
            "column1_movies": column1_movies,
            "column2_movies": column2_movies,
            "column3_movies": column3_movies
        }

    return render(request, 'movies/home.html', context)

def movies_view(request):
    genre_id = request.GET.get('genre')
    genre_selected = None
    movies_query = Movie.objects.all()


    if genre_id:
        try:
            genre_selected = Genre.objects.get(id=genre_id)
            movies_query = movies_query.filter(genres=genre_selected)
        except Genre.DoesNotExist:
            genre_selected = None


    categorized_movies = None
    if not genre_selected:
        categorized_movies = {
            "Populares": movies_query.filter(category="Populares"),
            "Mejor Valoradas": movies_query.filter(category="Mejor Valoradas"),
            "Próximamente": movies_query.filter(category="Próximamente"),
            "En Cines": movies_query.filter(category="En Cines"),
        }


    context = {
        "genres": Genre.objects.all(),
        "genre_selected": genre_selected,
        "categorized_movies": categorized_movies,
        "movies": movies_query if genre_selected else None,
    }

    return render(request, 'movies/movies.html', context)

def series_view(request):
    genre_id = request.GET.get('genre')
    genre_selected = None
    series_query = Series.objects.all()

    if genre_id:
        try:
            genre_selected = Genre.objects.get(id=genre_id)
            series_query = series_query.filter(genres=genre_selected)
        except Genre.DoesNotExist:
            genre_selected = None


    categorized_series = None
    if not genre_selected:
        categorized_series = {
            "Populares": series_query.filter(category="Populares"),
            "Mejor Valoradas": series_query.filter(category="Mejor Valoradas"),
            "Próximamente": series_query.filter(category="Próximamente"),
            "En Emisión": series_query.filter(category="En Emisión"),
        }

    context = {
        "genres": Genre.objects.all(),
        "genre_selected": genre_selected,
        "categorized_series": categorized_series,
        "series": series_query if genre_selected else None,
    }

    return render(request, 'movies/series.html', context)
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

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,  # Incluye el objeto película completo en el contexto
    })

def series_detail(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    return render(request, 'movies/series_detail.html', {'series': series})


def home_view(request):
    if request.user.is_authenticated:
        liked_movies = ViewedMovie.objects.filter(user=request.user, liked=True).values_list('movie_id', flat=True)
        suggestions = Movie.objects.filter(~Q(id__in=liked_movies))[:10]  # Excluir películas ya vistas
    else:
        suggestions = Movie.objects.all()[:10]  # Mostrar cualquier película para usuarios no autenticados
    return render(request, 'movies/home.html', {'suggestions': suggestions})


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
def user_settings(request):
    user = request.user

    # Asegurarse de que el perfil exista
    if not hasattr(user, 'profile'):
        UserProfile.objects.create(user=user)

    username_form = UpdateUsernameForm(instance=user)
    password_form = PasswordChangeForm(user)
    genres_form = UserGenresForm(instance=user.profile)

    if request.method == 'POST':
        if 'update_username' in request.POST:
            username_form = UpdateUsernameForm(request.POST, instance=user)
            if username_form.is_valid():
                username_form.save()
                return redirect('user_settings')
        elif 'update_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('user_settings')
        elif 'update_genres' in request.POST:
            genres_form = UserGenresForm(request.POST, instance=user.profile)
            if genres_form.is_valid():
                genres_form.save()
                return redirect('user_settings')

    context = {
        'username_form': username_form,
        'password_form': password_form,
        'genres_form': genres_form,
    }
    return render(request, 'movies/settings.html', context)


@login_required
def user_favorites(request):
    user = request.user
    favorite_movies = Movie.objects.filter(liked_by=user)
    favorite_series = Series.objects.filter(liked_by=user)

    context = {
        'favorite_movies': favorite_movies,
        'favorite_series': favorite_series,
    }
    return render(request, 'movies/favorites.html', context)


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


# peliculinchis y series que ya hs visto

@login_required
def mark_as_viewed_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    ViewedMovie.objects.get_or_create(user=request.user, movie=movie)
    # Eliminar de la lista de favoritos
    FavouriteMovie.objects.filter(user=request.user, movie=movie).delete()
    return redirect('viewed_list')
@login_required
def mark_as_viewed_series(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    # Eliminar de favoritos y agregar a vistas
    FavouriteSeries.objects.filter(user=request.user, series=series).delete()
    ViewedSeries.objects.get_or_create(user=request.user, series=series)
    return redirect('viewed_list')

@login_required
def viewed_list(request):
    viewed_movies = ViewedMovie.objects.filter(user=request.user)
    viewed_series = ViewedSeries.objects.filter(user=request.user)
    return render(request, 'movies/viewed_list.html', {
        'viewed_movies': viewed_movies,
        'viewed_series': viewed_series
    })

@login_required
def like_movie(request, movie_id):
    viewed_movie = ViewedMovie.objects.filter(user=request.user, movie_id=movie_id).first()
    if viewed_movie:
        viewed_movie.liked = True
        viewed_movie.save()
    return redirect('viewed_list')

@login_required
def dislike_movie(request, movie_id):
    viewed_movie = ViewedMovie.objects.filter(user=request.user, movie_id=movie_id).first()
    if viewed_movie:
        viewed_movie.liked = False
        viewed_movie.save()
    return redirect('viewed_list')


@login_required
def like_series(request, series_id):
    viewed_series = ViewedSeries.objects.filter(user=request.user, series_id=series_id).first()
    if viewed_series:
        viewed_series.liked = True
        viewed_series.save()
    return redirect('viewed_list')


@login_required
def dislike_series(request, series_id):
    viewed_series = ViewedSeries.objects.filter(user=request.user, series_id=series_id).first()
    if viewed_series:
        viewed_series.liked = False
        viewed_series.save()
    return redirect('viewed_list')
