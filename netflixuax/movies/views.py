from django.shortcuts import render, redirect
from .models import Movie
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
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
