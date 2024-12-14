from django.urls import path
from .views import register, home_view, my_list, add_movie, remove_favorite, series_view, movies_view, remove_favorite_series, add_series, mark_as_viewed_movie, mark_as_viewed_series, viewed_list, movie_detail
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('movies/', views.movies_view, name='movies'),
    path('series/', views.series_view, name='series'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='movies/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my_list/', views.my_list, name='my_list'),
    path('add_movie/<int:movie_id>/', views.add_movie, name='add_movie'),
    path('remove_favorite/<int:movie_id>/', views.remove_favorite, name='remove_favorite'),
    path('add_series/<int:series_id>/', views.add_series, name='add_series'),
    path('remove_favorite_series/<int:series_id>/', views.remove_favorite_series, name='remove_favorite_series'),
    path('mark_as_viewed_movie/<int:movie_id>/', views.mark_as_viewed_movie, name='mark_as_viewed_movie'),
    path('mark_as_viewed_series/<int:series_id>/', views.mark_as_viewed_series, name='mark_as_viewed_series'),
    path('viewed_list/', views.viewed_list, name='viewed_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),
    path('movie/<int:movie_id>/like/', views.like_movie, name='like_movie'),
    path('movie/<int:movie_id>/dislike/', views.dislike_movie, name='dislike_movie'),
    path('series/<int:series_id>/like/', views.like_series, name='like_series'),
    path('series/<int:series_id>/dislike/', views.dislike_series, name='dislike_series'),
]
