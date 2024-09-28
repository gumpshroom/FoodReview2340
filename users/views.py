import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from users.forms import CustomUserCreationForm
from users.models import Favorite


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('/foodFind/')
    else:
        form = CustomUserCreationForm()
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
@csrf_protect
def add_to_favorites_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            place_id = data.get('place_id')
            name = data.get('name')
            rating = data.get('rating')
            address = data.get('address')

            # Debugging log
            # print(f"Received place_id: {place_id}")
            # print(f"name: {name}")

            # Check if this place is already in the user's favorites
            favorite_exists = Favorite.objects.filter(user=request.user, place_id=place_id).exists()
            # print(f"Favorite exists: {favorite_exists}")  # Debugging log

            if favorite_exists:
                return JsonResponse({'success': False, 'message': f'{name} is already in your favorites.'}, status=200)

            # Save to Favorite model
            user_favorite = Favorite.objects.create(
                user=request.user,
                place_id=place_id,
                name=name,
                address=address,
                rating=rating,
            )

            return JsonResponse({'success': True, 'message': 'Favorite added successfully!'}, status=201)

        except Exception as e:
            print(f"Error: {e}")  # Debugging log
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
@csrf_protect
def remove_from_favorites_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            place_id = data.get('place_id')

            # Debugging log
            # print(f"Received place_id: {place_id}")

            # Check if the favorite exists for the user
            favorite_exists = Favorite.objects.filter(user=request.user, place_id=place_id).exists()

            if not favorite_exists:
                return JsonResponse({'success': False, 'message': 'Favorite not found.'}, status=404)

            # Remove the favorite from the database
            Favorite.objects.filter(user=request.user, place_id=place_id).delete()

            return JsonResponse({'success': True, 'message': 'Favorite removed successfully!'}, status=200)

        except Exception as e:
            print(f"Error: {e}")  # Debugging log
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
@csrf_protect
def remove_all_favorites_view(request):
    if request.method == 'POST':
        try:
            # Remove all favorites for the current user
            Favorite.objects.filter(user=request.user).delete()

            return JsonResponse({'success': True, 'message': 'All favorites removed successfully!'}, status=200)

        except Exception as e:
            print(f"Error: {e}")  # Debugging log
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def favorites_list_view(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        return render(request, 'users/favorites.html', {'favorites': favorites})
    return redirect('login')