# Generated by Django 5.1.4 on 2024-12-13 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_favouriteseries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='overview',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='poster_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
