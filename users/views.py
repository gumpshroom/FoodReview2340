from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Favorite
import json

from users.forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('/foodFind/')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/foodFind/')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/foodFind/')

@login_required
@csrf_exempt
def add_to_favorites_view(request):
    if request.method == 'POST':
        data = request.json()
        place_id = data.get('place_id')
        name = data.get('name')
        vicinity = data.get('vicinity')
        rating = data.get('rating')
    #    user_ratings_total = data.get('user_ratings_total')
        cuisine = data.get('cuisine')

        # Check if the restaurant is already in the user's favorites
        if not Favorite.objects.filter(user=request.user, place_id=place_id).exists():
            # Create and save the restaurant as a favorite
            favorite = Favorite.objects.create(
                user=request.user,
                place_id=place_id,
                name=name,
                vicinity=vicinity,
                rating=rating,
    #            user_ratings_total=user_ratings_total,
                cuisine=cuisine,
            )
            return JsonResponse({'success': True, 'message': 'Restaurant added to favorites!'})
        else:
            return JsonResponse({'success': False, 'message': 'Restaurant is already in your favorites!'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def favorites_list_view(request):
    favorites = Favorite.objects.filter(user=request.user)

    return render(request, 'users/favorites.html', {'favorites': favorites})