# Generated by Django 3.1.7 on 2021-03-04 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flicks', '0004_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFlick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flicks.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flicks.user')),
            ],
        ),
    ]