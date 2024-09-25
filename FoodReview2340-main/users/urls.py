from django.urls import path
from django.contrib.auth import views as auth_views

from users import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('favorites/', views.favorites_list_view, name='favorites'),
    path('addFavorites/', views.add_to_favorites_view, name='add-to-favorites'),
]