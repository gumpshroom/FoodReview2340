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
            address = data.get('address')
            vicinity = data.get('vicinity', None)  # Optional field
            rating = data.get('rating', None)  # Optional field
            cuisine = data.get('cuisine', None)  # Optional field

            # Check if this place is already in the user's favorites
            favorite_exists = Favorite.objects.filter(user=request.user, place_id=place_id).exists()

            if favorite_exists:
                return JsonResponse({'success': False, 'message': f'{name} is already in your favorites.'}, status=200)

            # Save to Favorite model
            user_favorite = Favorite.objects.create(
                user=request.user,
                place_id=place_id,
                name=name,
                address=address,
                vicinity=vicinity,
                rating=rating,
                cuisine=cuisine
            )

            return JsonResponse({'success': True, 'message': 'Favorite added successfully!'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def favorites_list_view(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        return render(request, 'users/favorites.html', {'favorites': favorites})
    return redirect('login')