from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    place_id = models.CharField(max_length=255, unique=True)
    vicinity = models.CharField(max_length=255, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
##    user_ratings_total = models.IntegerField(null=True, blank=True)
    cuisine = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"