# Generated by Django 5.1.4 on 2024-12-15 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_genre_alter_movie_overview_movie_genres_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='genres',
            field=models.ManyToManyField(blank=True, to='movies.genre'),
        ),
    ]