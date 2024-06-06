from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import models

class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    other_facilities = models.CharField(max_length=255)
    description = models.TextField()
    parking_available = models.BooleanField(default=False)
    bachelors_allowed = models.BooleanField(default=False)
    contact = models.CharField(max_length=255)
    rent = models.DecimalField(max_digits=10, decimal_places=2)

class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_pictures/')



