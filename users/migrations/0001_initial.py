# Generated by Django 5.1.1 on 2024-09-26 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

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
                ('place_id', models.CharField(max_length=255, unique=True)),
                ('vicinity', models.CharField(blank=True, max_length=255, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('cuisine', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
