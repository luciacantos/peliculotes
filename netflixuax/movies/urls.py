from django.urls import path
from .views import register, home, my_list, add_movie, remove_favorite, series_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('series/', series_view, name='series'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='movies/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my_list/', my_list, name='my_list'),
    path('add_movie/<int:movie_id>/', add_movie, name='add_movie'),
    path('remove_favorite/<int:movie_id>/', remove_favorite, name='remove_favorite'),
]
