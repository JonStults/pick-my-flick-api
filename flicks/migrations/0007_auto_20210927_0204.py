# Generated by Django 3.2.6 on 2021-09-27 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flicks', '0006_userflick_watched'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genre_ids',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='overview',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='poster_path',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='release_date',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
