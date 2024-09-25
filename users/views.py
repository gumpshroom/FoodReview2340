import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt

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
@csrf_exempt
def add_to_favorites_view(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated.'}, status=403)

        try:
            data = json.loads(request.body)
            place_id = data.get('place_id')
            name = data.get('name')
            rating = data.get('rating')
#            user_ratings_total = data.get('user_ratings_total')

            # Save to UserFavorite model
            user_favorite = Favorite.objects.create(
                user=request.user,
                place_id=place_id,
                name=name,
                rating=rating,
#                user_ratings_total=user_ratings_total
            )

            return JsonResponse({'message': 'Favorite added successfully!'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def favorites_list_view(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        return render(request, 'users/favorites.html', {'favorites': favorites})
    return redirect('login')  # Redirect to login if not authenticated