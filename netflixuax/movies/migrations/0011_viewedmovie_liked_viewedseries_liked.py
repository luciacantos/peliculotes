# Generated by Django 5.1.4 on 2024-12-13 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_series_tmdb_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewedmovie',
            name='liked',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='viewedseries',
            name='liked',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
