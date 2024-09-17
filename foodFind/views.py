from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'FoodReview2340/homepage.html')
def map(request):
    return render(request, 'FoodReview2340/mapTest.html')
def loggedInHome(request):
    return render(request, 'FoodReview2340/loggedInHP.html')