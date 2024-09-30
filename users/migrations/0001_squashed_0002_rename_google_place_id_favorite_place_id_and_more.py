# Generated by Django 4.2.15 on 2024-09-30 02:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('users', '0001_initial'), ('users', '0002_rename_google_place_id_favorite_place_id_and_more')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=500)),
                ('google_place_id', models.CharField(max_length=255, unique=True)),
                ('vicinity', models.CharField(blank=True, max_length=255, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('cuisine', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
