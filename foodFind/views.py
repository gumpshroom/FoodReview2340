from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'FoodReview2340/home.html')
def map(request):
    return render(request, 'FoodReview2340/mapTest.html')