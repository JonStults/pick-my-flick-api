# Generated by Django 3.2.6 on 2021-09-28 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flicks', '0008_remove_movie_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='watched',
        ),
    ]
