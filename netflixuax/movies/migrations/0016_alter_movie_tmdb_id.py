# Generated by Django 5.1.4 on 2024-12-16 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_movie_is_featured_movie_rating_alter_movie_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='tmdb_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]