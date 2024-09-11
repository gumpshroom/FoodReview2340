from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, f'Your account has been created!')
            return redirect('home')  # Redirect to home or another page
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})