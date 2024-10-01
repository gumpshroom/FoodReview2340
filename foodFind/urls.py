from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('map/', views.map, name='map'),
    path('generateDescription/', views.generateDescription, name='generateDescription'),
    path('summarizeComments/', views.summarizeComments, name='summarizeComments')
]